import bson

from jam import Q
from jam import exceptions
from jam.auth import Permissions
from jam.server.api.v1.base import View
from jam.server.api.v1.base import Serializer
from jam.server.api.v1.base import Relationship
from jam.server.api.v1.collection import CollectionView


class DocumentView(View):

    name = 'document'
    plural = 'documents'
    parent = CollectionView

    @classmethod
    def load(self, id, namespace, collection):
        return collection.read(id)
        # doc = collection.read(id)
        # doc.permissions = {doc.created_by: collection.creator_permissions}
        # return doc

    def __init__(self, namespace, collection, resource=None):
        super().__init__(namespace, collection, resource=resource)
        self._document = resource
        self._namespace = namespace
        self._collection = collection

    def get_required_permissions(self, request):
        if request.method == 'GET' and self.resource is None:
            return Permissions.NONE
        return super().get_required_permissions(request)

    def create(self, payload, user):
        id = self.validate_id(str(bson.ObjectId()) if payload.get('id') is None else payload['id'])
        creator = user.uid

        if 'user' in self._collection.plugins and self._collection.plugin('user').created_is_owner:
            creator = 'jam-{}:{}-{}'.format(self._namespace.ref, self._collection.ref, id)

        if 'meta' in payload:
            if (user.permissions & Permissions.ADMIN) != Permissions.ADMIN:
                raise exceptions.Forbidden('ADMIN permission is request to alter metadata')
            creator = payload['meta'].get('created-by', user.uid)

        try:
            return self._collection.create(id, payload['attributes'], creator)
        except KeyError:
            raise exceptions.MalformedData()

    def update(self, patches, user):
        return self._collection.update(self._document.ref, patches, user.uid)

    def delete(self, user):
        self._collection.delete(self.resource.ref, user.uid)

    def replace(self, attributes, user):
        return self._collection.replace(self._document.ref, attributes, user.uid, merger=None)

    def list(self, filter, sort, page, page_size, user):
        if not user.permissions & Permissions.READ:
            if not user.uid:
                raise exceptions.Unauthorized()
            if filter:
                filter &= Q('created_by', 'eq', user.uid)
            else:
                filter = Q('created_by', 'eq', user.uid)

        return super().list(filter, sort, page, page_size, user)


class HistoryRelationship(Relationship):

    @classmethod
    def view(cls, namespace, collection, document):
        from jam.server.api.v1.history import HistoryView
        return HistoryView(namespace, collection, document)

    @classmethod
    def serializer(cls):
        from jam.server.api.v1.history import HistorySerializer
        return HistorySerializer

    @classmethod
    def self_link(cls, request, document, namespace, collection):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/documents/{}/history'.format(request.protocol, request.host, '.'.join((namespace.ref, collection.ref, document.ref)))
        return '{}://{}/v1/namespaces/{}/collections/{}/documents/{}/history'.format(request.protocol, request.host, namespace.ref, collection.ref, document.ref)

    @classmethod
    def related_link(cls, request, document, namespace, collection):
        if request.path.startswith('/v1/id'):
            return '{}://{}/v1/id/documents/{}/history'.format(request.protocol, request.host, '.'.join((namespace.ref, collection.ref, document.ref)))
        return '{}://{}/v1/namespaces/{}/collections/{}/documents/{}/history'.format(request.protocol, request.host, namespace.ref, collection.ref, document.ref)


class DocumentSerializer(Serializer):
    type = 'documents'

    relations = {
        'history': HistoryRelationship
    }

    def attributes(self):
        return self._instance.data
