import elasticsearch_dsl

from jam import exceptions
from jam.auth import Permissions
from jam.plugins.base import Plugin
from jam.backends.util import get_backend


# Suggested ES Settings
# script.file: off
# script.indexed: off
# script.inline: off


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


class SearchPlugin(Plugin):
    NAME = 'search'
    EXPLICIT = False
    SCHEMA = {
        'type': 'object',
        'properties': {},
        'additionalProperties': False,
    }

    def get_required_permissions(self, request):
        if request.method == 'POST':
            return Permissions.ADMIN
        return Permissions.READ

    def prerequisite_check(self):
        super().prerequisite_check()
        if not isinstance(self.collection._state._backend.raw_backend(), get_backend('elasticsearch')):
            raise exceptions.BadRequest(detail='This collection does not support searching')

    def get_serializer(self):
        from jam.server.api.v1.document import DocumentSerializer

        # Super hacky but can't seem to avoid the circular imports
        class SearchSerializer(DocumentSerializer):

            def meta(self):
                return {
                    'score': self._instance._score,
                    **super().meta()
                }
        return SearchSerializer

    def get(self, handler):
        # Rip the search object out of the elasticsearch backend
        sort = handler.sort
        search = self.collection._state._backend.raw_backend().search

        if handler.request.query_arguments.get('q'):
            search = search.query(elasticsearch_dsl.Q('query_string', query=handler.request.query_arguments['q'][-1].decode('utf-8')))
        else:
            # This should technically be elsewhere but the search object
            # does not provide a nice way to figure out if there is a query or not.
            search = search.sort({'ref': {
                'order': 'asc',
                'unmapped_type': 'string'
            }})

        if handler.request.query_arguments.get('sort'):
            search = search.sort({sort.key: {
                'order': 'asc' if sort.order == 1 else 'desc',
                'unmapped_type': 'string'
            }})

        # Hacking into the serializer
        handler._serializer = self.get_serializer()
        handler._view.parents = handler._view.parents + (self.collection,)

        start = handler.page * handler.page_size
        wrapper = SearchResultWrapper(search[start:start + handler.page_size])
        return handler.write({
            'meta': {
                'total': wrapper.count(),
                'perPage': handler.page_size
            },
            # TODO
            'links': {},
            'data': [handler.serialize(resource) for resource in wrapper]
        })
