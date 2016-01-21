import http.client

import elasticsearch_dsl
import tornado.web

from jam.auth import Permissions
from jam.server.api.v2.base import View
from jam.server.api.v2.base import Relationship


class DotDict:
    __slots__ = ('_inner', )

    def __init__(self, inner):
        self._inner = inner

    def __getattr__(self, key):
        return self._inner[key]


class SearchResultWrapper:

    def __init__(self, search):
        self._search = search
        self._result = search.execute().to_dict()

    def count(self):
        return self._result['hits']['total']

    def __iter__(self):
        for res in self._result['hits']['hits']:
            res['_source']['_score'] = res['_score']
            yield DotDict(res['_source'])


class SearchView(View):

    def get_permissions(self, request):
        # Hacky as everything
        self._request = request
        if request.method == 'POST':
            return Permissions.ADMIN
        return Permissions.READ

    def create(self):
        # TODO Post querys/aggs
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

    def read(self, user):
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

    def update(self, user):
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

    def delete(self, user):
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

    def list(self, filter, sort, page, page_size, user):
        # Rip the search object out of the elasticsearch backend
        try:
            search = self.parents[-1]._state._backend.raw_backend().search
        except AttributeError:
            print('Tried to search on an unsearchable collection')
            raise

        if self._request.query_arguments.get('q'):
            search = search.query(elasticsearch_dsl.Q('query_string', query=self._request.query_arguments['q']))
        else:
            # This should technically be elsewhere but the search object
            # does not provide a nice way to figure out if there is a query or not.
            search = search.sort({'ref': {
                'order': 'asc',
                'unmapped_type': 'string'
            }})

        start = page * page_size
        search = search[start:start+page_size]

        return SearchResultWrapper(search)


class SearchRelationship(Relationship):
    included = False

    @classmethod
    def view(cls, namespace, collection):
        return SearchView(namespace, collection)

    @classmethod
    def serializer(cls):
        from jam.server.api.v2.document import DocumentSerializer
        # TODO FIX ME

        class SearchSerializer(DocumentSerializer):

            @classmethod
            def meta(cls, inst):
                return {
                    'score': inst._score,
                    **super(SearchSerializer, cls).meta(inst)
                }
        return SearchSerializer
