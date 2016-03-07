import operator
import functools

from jam import Q
from jam import NamespaceManager
from jam.auth import Permissions
from jam.server.api.v1.base import View
from jam.server.api.v1.base import Serializer
from jam.server.api.v1.base import Relationship


class NamespaceView(View):

    name = 'namespace'
    plural = 'namespaces'
    MANAGER = NamespaceManager()

    @classmethod
    def load(self, id):
        return self.MANAGER.get_namespace(id)

    def __init__(self, resource=None):
        super().__init__(resource=resource)
        self._namespace = resource

    def get_permissions(self, request):
        if request.method == 'GET' and self.resource is None:
            return Permissions.NONE
        return super().get_permissions(request)

    def read(self, user):
        return self._namespace.document

    def update(self, patch, user):
        return self.MANAGER.update(self._namespace.ref, patch, user.uid)

    def list(self, filter, sort, page, page_size, user):
        query = functools.reduce(operator.or_, [
            Q('data.permissions.*', 'and', Permissions.READ),
            Q('data.permissions.{0.type}-*'.format(user), 'and', Permissions.READ),
            Q('data.permissions.{0.type}-{0.provider}-*'.format(user), 'and', Permissions.READ),
            Q('data.permissions.{0.type}-{0.provider}-{0.id}'.format(user), 'and', Permissions.READ),
        ])

        if filter:
            filter &= query
        else:
            filter = query

        return self.MANAGER.select().where(filter).page(page, page_size).order_by(sort)


class CollectionRelationship(Relationship):

    @classmethod
    def view(cls, namespace):
        from jam.server.api.v1.collection import CollectionView
        return CollectionView(namespace)

    @classmethod
    def serializer(cls):
        from jam.server.api.v1.collection import CollectionSerializer
        return CollectionSerializer

    @classmethod
    def self_link(cls, request, namespace):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/namespaces/{}/collections'.format(request.protocol, request.host, namespace.ref)
        return '{}://{}/v1/namespaces/{}/collections'.format(request.protocol, request.host, namespace.ref)

    @classmethod
    def related_link(cls, request, namespace):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/namespaces/{}/collections'.format(request.protocol, request.host, namespace.ref)
        return '{}://{}/v1/namespaces/{}/collections'.format(request.protocol, request.host, namespace.ref)


class NamespaceSerializer(Serializer):
    type = 'namespaces'
    relations = {
        'collections': CollectionRelationship
    }

    @classmethod
    def attributes(cls, inst):
        return {
            'name': inst.ref,
            'permissions': {
                sel: Permissions(perm).name
                for sel, perm in inst.data['permissions'].items()
            }
        }
