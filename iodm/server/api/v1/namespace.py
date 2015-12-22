import datetime
import operator
import functools

from iodm import O
from iodm import Q
from iodm import NamespaceManager
from iodm.auth import Permissions
from iodm.server.api.v1.base import APIResource


manager = NamespaceManager()


class NamespaceResource(APIResource):

    PAGE_SIZE = 10

    @classmethod
    def serialize(cls, namespace, request):
        return {
            'id': namespace.ref,
            'type': 'namespace',
            'attributes': {
                'name': namespace.ref,
                'permissions': namespace.data['permissions'],
                'state': namespace.data['state']['backend'],
                'logger': namespace.data['logger']['backend'],
                'storage': namespace.data['storage']['backend'],
                'created-on': datetime.datetime.fromtimestamp(namespace.created_on).isoformat()
            },
            'relationships': {
                'collections': {
                    'links': {
                        'self': '{}://{}/v1/namespaces/{}/relationships/collections/'.format(request.protocol, request.host, namespace.ref),
                        'related': '{}://{}/v1/namespaces/{}/collections/'.format(request.protocol, request.host, namespace.ref),
                    }
                }
            }
        }

    @property
    def namespace(self):
        return self.resource

    def __init__(self):
        super().__init__('namespace')

    def get_permissions(self, request):
        if self.resource:
            return Permissions.ADMIN
        return Permissions.NONE

    def load(self, namespace_id, request):
        return super().load(manager.get_namespace(namespace_id))

    def list(self, user, page=0, filter=None):
        selector = manager.select().order_by(O.Ascending('ref')).page(page, self.PAGE_SIZE)

        # TODO These should technically be bitwise...
        query = functools.reduce(operator.or_, [
            Q('data.permissions.*', 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-*'.format(user), 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-{0.provider}-*'.format(user), 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-{0.provider}-{0.id}'.format(user), 'eq', Permissions.ADMIN),
        ])

        # TODO Test me
        if filter:
            query = functools.reduce(operator.and_, [
                Q(key, 'eq', value)
                for key, value in
                filter.items()
            ])

        return selector.where(query)

    def create(self, data, user):
        return manager.read(manager.create_namespace(data['id'], user.uid).name)

    def read(self, user):
        # TODO find a better way to handle this
        # Serialize expects a document but an actual Namespace object has not reference to its document
        return manager.read(self.namespace.name)
