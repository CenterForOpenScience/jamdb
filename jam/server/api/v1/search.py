import datetime

import elasticsearch_dsl
from tornado.web import HTTPError

from jam.auth import Permissions
from jam.server.api.v1.base import APIResource
from jam.server.api.v1.base import ResourceHandler
from jam.server.api.v1.collection import CollectionResource


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

    @property
    def collection_id(self):
        return self.request.path.split('/')[5]

    @property
    def namespace_id(self):
        return self.request.path.split('/')[3]

    @property
    def relationships(self):
        return {
            'namespace': {
                'links': {
                    'self': '{}://{}/v1/namespaces/{}'.format(self.request.protocol, self.request.host, self.namespace_id),
                    'related': '{}://{}/v1/namespaces/{}'.format(self.request.protocol, self.request.host, self.namespace_id),
                    }
                },
            'collection': {
                'links': {
                    'self': '{}://{}/v1/namespaces/{}/collections/{}'.format(self.request.protocol, self.request.host, self.namespace_id, self.collection_id),
                    'related': '{}://{}/v1/namespaces/{}/collections/{}'.format(self.request.protocol, self.request.host, self.namespace_id, self.collection_id),
                    }
                }
            }

    @property
    def start(self):
        return ((self.page - 1) * self.page_size)

    def write_search_result(self, search):
        search = search.params(**{
            key: val[-1].decode('utf-8')
            for key, val in self.request.query_arguments.items()
            if key in ('pretty', 'search_type')
        })

        search = search[self.start:self.start + self.page_size]

        result = search.execute().to_dict()
        json_api_results = []
        del result['_shards']

        for hit in result['hits']['hits']:
            json_api_results.append({
                'id': hit['_id'],
                'type': 'documents',
                'attributes': hit['_source']['data'],
                'meta': {
                    'score': hit['_score'],
                    'created-by': hit['_source']['created_by'],
                    'modified-by': hit['_source']['modified_by'],
                    'created-on': datetime.datetime.fromtimestamp(hit['_source']['created_on']).isoformat(),
                    'modified-on': datetime.datetime.fromtimestamp(hit['_source']['created_on']).isoformat()
                },
                'relationships': {
                    **self.relationships,
                    'history': {
                        'links': {
                            'self': self.relationships['collection']['links']['self'] + '/documents/{}/history'.format(hit['_id']),
                            'related': self.relationships['collection']['links']['self'] + '/documents/{}/history'.format(hit['_id']),
                        }
                    }
                }
            })

        self.write({
            'data': json_api_results,
            'meta': {
                'perPage': self.page_size,
                'total': result['hits']['total']
            }
        })

    def get(self, *args, **kwargs):
        if self.resource.resource is not None:
            raise HTTPError(405)

        search = self.resource.collection._state._backend.raw_backend().search

        query = self.get_query_argument('q', default=None)
        if query:
            search = search.query(elasticsearch_dsl.Q('query_string', query=query))
        else:
            # This should technically be elsewhere but the search object
            # does not provide a nice way to figure out if there is a query or not.
            search = search.sort({'ref': 'asc'})

        self.write_search_result(search)

    def post(self, *args, **kwargs):
        raise HTTPError(405)  # Disable for the moment
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
