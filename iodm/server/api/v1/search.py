import elasticsearch_dsl
from tornado.web import HTTPError

from iodm.auth import Permissions
from iodm.server.api.v1.base import APIResource
from iodm.server.api.v1.base import ResourceHandler
from iodm.server.api.v1.collection import CollectionResource


class SearchResource(APIResource):

    PAGE_SIZE = 50

    @classmethod
    def as_handler_entry(cls):
        inst = cls()
        return (inst.general_pattern, SearchHandler, {'resource': cls})

    @property
    def collection(self):
        return self.parent.resource

    @property
    def namespace(self):
        return self.parent.parent.resource

    def __init__(self):
        super().__init__('_search', CollectionResource, plural='_search')

    def load(self, _id, request):
        raise Exception

    def get_permissions(self, request):
        return Permissions.READ


class SearchHandler(ResourceHandler):

    def write_search_result(self, search):
        search = search.params(**{
            key: val[-1].decode('utf-8')
            for key, val in self.request.query_arguments.items()
            if key in ('pretty', 'search_type')
        })

        result = search.execute().to_dict()
        del result['_shards']

        for hit in result['hits']['hits']:
            del hit['_type']
            del hit['_index']
            del hit['_source']['ref']
            del hit['_source']['log_ref']
            del hit['_source']['data_ref']

        self.write(result)

    def get(self, *args, **kwargs):
        if self.resource.resource is not None:
            raise HTTPError(405)

        search = self.resource.collection._state._backend.raw_backend().search

        query = self.get_query_argument('q', default=None)
        if query:
            search = search.query(elasticsearch_dsl.Q('query_string', query=query))

        self.write_search_result(search)

    def post(self, *args, **kwargs):
        if self.resource.resource is not None:
            raise HTTPError(405)

        search = self.resource.collection._state._backend.raw_backend().search

        search.update_from_dict(self.json)

        self.write_search_result(search)

    def head(self, *args, **kwargs):
        raise HTTPError(405)

    def delete(self, *args, **kwargs):
        raise HTTPError(405)

    def patch(self, *args, **kwargs):
        raise HTTPError(405)

    def put(self, *args, **kwargs):
        raise HTTPError(405)
