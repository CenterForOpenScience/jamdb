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
        if self.resource:
            return Permissions.ADMIN
        return Permissions.NONE

    def read(self, user):
        # TODO Allow serializing of namespace objects
        return self.MANAGER.read(self.resource.name)

    def update(self, patch, user):
        return self.MANAGER.update(self._namespace.name, patch, user.uid)

    def list(self, filter, sort, page, page_size, user):
        # TODO These should technically be bitwise...
        query = functools.reduce(operator.or_, [
            Q('data.permissions.*', 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-*'.format(user), 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-{0.provider}-*'.format(user), 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-{0.provider}-{0.id}'.format(user), 'eq', Permissions.ADMIN),
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
    def self_link(cls, request, inst, *parents):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}/collections/'.format(request.protocol, request.host, inst.ref)
        return '{}://{}/v2/namespaces/{}/collections/'.format(request.protocol, request.host, inst.ref)

    @classmethod
    def related_link(cls, request, inst, *parents):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}/collections/'.format(request.protocol, request.host, inst.ref)
        return '{}://{}/v2/namespaces/{}/collections/'.format(request.protocol, request.host, inst.ref)


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
