import operator
import functools

from jam import Q
from jam.auth import Permissions
from jam.server.api.v2.base import View
from jam.server.api.v2.base import Serializer
from jam.server.api.v2.namespace import NamespaceView


class CollectionSerializer(Serializer):
    type = 'collections'

    @classmethod
    def attributes(cls, inst):
        return {
            'name': inst.ref,
            'permissions': inst.data['permissions'],
        }


class CollectionView(View):

    name = 'collection'
    plural = 'collections'
    parent = NamespaceView

    @classmethod
    def load(self, id, namespace):
        return namespace.get_collection(id)

    def __init__(self, namespace, resource=None):
        super().__init__(namespace, resource=resource)
        self._namespace = namespace

    # def get_permissions(self, request):
    #     if self.resource:
    #         if request.method == 'GET':
    #             return Permissions.ADMIN

    #     return Permissions.NONE

    def create(self, id, attributes, user):
        # TODO Better validation
        if set(attributes.keys()) - {'logger', 'storage', 'state', 'permissions'}:
            raise Exception()
        attributes['name'] = id
        id = id.lower()
        self._namespace.create_collection(id, user.uid, **attributes)
        return self._namespace.read(id)

    def read(self, user):
        return self._namespace.read(self.resource.name)

    def list(self, filter, sort, page, page_size, user):
        # TODO These should technically be bitwise...
        query = functools.reduce(operator.or_, [
            Q('data.permissions.*', 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-*'.format(user), 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-{0.provider}-*'.format(user), 'eq', Permissions.ADMIN),
            Q('data.permissions.{0.type}-{0.provider}-{0.id}'.format(user), 'eq', Permissions.ADMIN),
        ])

        return super().list((filter & query) if filter else query, sort, page, page_size, user)



# class CollectionRelationship(Relationship):
#     name = 'collections'

#     def list(self):
#         pass
