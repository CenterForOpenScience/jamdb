import operator
import functools

from jam import Q
from jam.auth import Permissions
from jam.server.api.v2.base import View
from jam.server.api.v2.base import Serializer
from jam.server.api.v2.base import Relationship
from jam.server.api.v2.namespace import NamespaceView
from jam.server.api.v2.search import SearchRelationship
from jam.server.api.v2.namespace import NamespaceSerializer



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

    def get_permissions(self, request):
        if not self.resource:
            if request.method == 'GET':
                return Permissions.NONE
            return Permissions.ADMIN
        return super().get_permissions(request)

    def create(self, id, attributes, user):
        # TODO Better validation
        if set(attributes.keys()) - {'logger', 'storage', 'state', 'permissions'}:
            raise Exception()
        self._namespace.create_collection(id, user.uid, **attributes)
        return self._namespace.read(id)

    def read(self, user):
        return self._namespace.read(self.resource.name)

    # def list(self, filter, sort, page, page_size, user):
    #     import ipdb; ipdb.set_trace()
    #     # TODO These should technically be bitwise...
    #     query = functools.reduce(operator.or_, [
    #         Q('data.permissions.*', 'eq', Permissions.ADMIN),
    #         Q('data.permissions.{0.type}-*'.format(user), 'eq', Permissions.ADMIN),
    #         Q('data.permissions.{0.type}-{0.provider}-*'.format(user), 'eq', Permissions.ADMIN),
    #         Q('data.permissions.{0.type}-{0.provider}-{0.id}'.format(user), 'eq', Permissions.ADMIN),
    #     ])

    #     return super().list((filter & query) if filter else query, sort, page, page_size, user)


class NamespaceRelationship(Relationship):

    @classmethod
    def view(cls, namespace, collection):
        return NamespaceView(namespace)

    @classmethod
    def serializer(cls):
        return NamespaceSerializer

    @classmethod
    def self_link(cls, request, inst, namespace):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace.name)
        return '{}://{}/v2/namespaces/{}'.format(request.protocol, request.host, namespace.name)

    @classmethod
    def related_link(cls, request, inst, namespace):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace.name)
        return '{}://{}/v2/namespaces/{}'.format(request.protocol, request.host, namespace.name)


class DocumentsRelationship(Relationship):

    @classmethod
    def view(cls, namespace, collection):
        from jam.server.api.v2.document import DocumentView
        return DocumentView(namespace, collection)

    @classmethod
    def serializer(cls):
        from jam.server.api.v2.document import DocumentSerializer
        return DocumentSerializer

    @classmethod
    def self_link(cls, request, collection, namespace):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}/collections/{}/documents'.format(request.protocol, request.host, namespace.name, collection.ref)
        return '{}://{}/v2/collections/{}/documents'.format(request.protocol, request.host, collection.ref)

    @classmethod
    def related_link(cls, request, collection, namespace):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}/collections/{}/documents'.format(request.protocol, request.host, namespace.name, collection.ref)
        return '{}://{}/v2/collections/{}/documents'.format(request.protocol, request.host, collection.ref)


class CollectionSerializer(Serializer):
    type = 'collections'

    relations = {
        '_search': SearchRelationship,
        'namespace': NamespaceRelationship,
        'documents': DocumentsRelationship,
    }

    @classmethod
    def attributes(cls, inst):
        return {
            'name': inst.ref,
            'permissions': inst.data['permissions'],
        }
