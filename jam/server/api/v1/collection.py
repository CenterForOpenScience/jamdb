import calendar
import datetime
import functools
import operator

from dateutil.parser import parse

import jam
from jam.auth import Permissions
from jam.backends import EphemeralBackend
from jam.server.api.v1.base import APIResource
from jam.server.api.v1.namespace import NamespaceResource


class CollectionResource(APIResource):

    PAGE_SIZE = 50

    @classmethod
    def serialize(cls, collection_doc, request):
        # TODO Feel less bad about this
        namespace_id = request.path.split('/')[3]
        return {
            'id': collection_doc.ref,
            'type': 'collections',
            'attributes': {
                'name': collection_doc.ref,
                'permissions': collection_doc.data['permissions'],
            },
            'meta': {
                'created-by': collection_doc.created_by,
                'modified-by': collection_doc.modified_by,
                'created-on': datetime.datetime.fromtimestamp(collection_doc.created_on).isoformat(),
                'modified-on': datetime.datetime.fromtimestamp(collection_doc.created_on).isoformat()
            },
            'relationships': {
                'namespace': {
                    'links': {
                        'self': '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace_id),
                        'related': '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace_id),
                    }
                },
                'documents': {
                    'links': {
                        'self': '{}://{}/v1/namespaces/{}/collections/{}/documents'.format(request.protocol, request.host, namespace_id, collection_doc.ref),
                        'related': '{}://{}/v1/namespaces/{}/collections/{}/documents'.format(request.protocol, request.host, namespace_id, collection_doc.ref),
                    }
                }
            }
        }

    @property
    def namespace(self):
        return self.parent.resource

    @property
    def collection(self):
        return self.resource

    def __init__(self):
        super().__init__('collection', NamespaceResource)

    def get_permissions(self, request):
        if not self.resource:
            if request.method == 'GET':
                return Permissions.NONE
            return Permissions.ADMIN
        return super().get_permissions(request)

    def load(self, collection_id, request):
        collection = self.namespace.get_collection(collection_id)

        maybe_time = request.query_arguments.get('timemachine')
        if maybe_time:
            maybe_time = maybe_time[-1].decode('utf-8')
            try:
                timestamp = float(maybe_time)
            except ValueError:
                timestamp = calendar.timegm(parse(maybe_time).utctimetuple())

            collection = collection.at_time(
                timestamp,
                jam.State(EphemeralBackend()),
                regenerate=False
            )

            if collection.regenerate() > 200:
                collection.snapshot()

        return super().load(collection)

    def create(self, data, user):
        if set(data['attributes'].keys()) - {'logger', 'storage', 'state', 'permissions'}:
            raise Exception()
        self.namespace.create_collection(data['id'], user.uid, **data['attributes'])
        return self.namespace.read(data['id'])

    def list(self, user, filter=None):
        selector = self.namespace.select().order_by(
            jam.O.Ascending('ref')
        )

        if not filter:
            query = None
        else:
            query = functools.reduce(operator.and_, [
                jam.Q(key, 'eq', value)
                for key, value in
                filter.items()
            ])

        return selector.where(query)

    def read(self, user):
        return self.namespace.read(self.collection.name)
