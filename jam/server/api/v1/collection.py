import operator
import functools

from jam import Q
from jam import exceptions
from jam.auth import Permissions
from jam.server.api.v1.base import View
from jam.server.api.v1.base import Serializer
from jam.server.api.v1.base import Relationship
from jam.server.api.v1.namespace import NamespaceView
from jam.server.api.v1.namespace import NamespaceSerializer


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
        self._collection = resource

    def get_permissions(self, request):
        if request.method == 'GET' and self.resource is None:
            return Permissions.NONE
        return super().get_permissions(request)

    def do_create(self, id, attributes, user):
        return self._namespace.create_collection(id, user.uid, **attributes).document

    def read(self, user):
        return self._collection.document

    def update(self, patch, user):
        return self._namespace.update(self.resource.ref, patch, user.uid)

    def delete(self, user):
        return self._namespace.delete(self.resource.name, user.uid)

    def list(self, filter, sort, page, page_size, user):
        if not user.permissions & Permissions.ADMIN:
            if not user.uid:
                raise exceptions.Unauthorized()

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

        return super().list(filter, sort, page, page_size, user)


class NamespaceRelationship(Relationship):

    @classmethod
    def view(cls, namespace, collection):
        return NamespaceView(namespace)

    @classmethod
    def serializer(cls):
        return NamespaceSerializer

    @classmethod
    def self_link(cls, request, inst, namespace):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/namespaces/{}'.format(request.protocol, request.host, namespace.ref)
        return '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace.ref)

    @classmethod
    def related_link(cls, request, inst, namespace):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/namespaces/{}'.format(request.protocol, request.host, namespace.ref)
        return '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace.ref)


class DocumentsRelationship(Relationship):

    @classmethod
    def view(cls, namespace, collection):
        from jam.server.api.v1.document import DocumentView
        return DocumentView(namespace, collection)

    @classmethod
    def serializer(cls):
        from jam.server.api.v1.document import DocumentSerializer
        return DocumentSerializer

    @classmethod
    def self_link(cls, request, collection, namespace):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/collections/{}/documents'.format(request.protocol, request.host, '.'.join((namespace.ref, collection.ref)))
        return '{}://{}/v1/namespaces/{}/collections/{}/documents'.format(request.protocol, request.host, namespace.ref, collection.ref)

    @classmethod
    def related_link(cls, request, collection, namespace):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/collections/{}/documents'.format(request.protocol, request.host, '.'.join((namespace.ref, collection.ref)))
        return '{}://{}/v1/namespaces/{}/collections/{}/documents'.format(request.protocol, request.host, namespace.ref, collection.ref)


class CollectionSerializer(Serializer):
    type = 'collections'

    plugins = {
        'user': 'user',
        '_search': 'search',
    }

    relations = {
        'namespace': NamespaceRelationship,
        'documents': DocumentsRelationship,
    }

    @classmethod
    def attributes(cls, inst):
        return {
            'name': inst.ref,
            'schema': inst.data.get('schema'),
            'permissions': {
                sel: Permissions(perm).name
                for sel, perm in inst.data['permissions'].items()
            }
        }
