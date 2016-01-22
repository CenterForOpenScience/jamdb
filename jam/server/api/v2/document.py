from itertools import zip_longest

import bson

from jam import Q
from jam import exceptions
from jam.auth import Permissions
from jam.server.api.v2.base import View
from jam.server.api.v2.base import Serializer
from jam.server.api.v2.base import Relationship
from jam.server.api.v2.collection import CollectionView


class DocumentView(View):

    name = 'document'
    plural = 'documents'
    parent = CollectionView

    @classmethod
    def load(self, id, namespace, collection):
        return collection.read(id)

    def __init__(self, namespace, collection, resource=None):
        super().__init__(namespace, collection, resource=resource)
        self._document = resource
        self._namespace = namespace
        self._collection = collection

    def get_permissions(self, request):
        if request.method == 'GET' and self.resource is None:
            return Permissions.NONE
        return super().get_permissions(request)

    def create(self, payload, user):
        *parent_ids, id = payload.get('id', str(bson.ObjectId())).split('.')
        if parent_ids:
            for (parent, pid) in zip_longest(self.parents, parent_ids):
                assert parent.name == pid
        try:
            return self._collection.create(id, payload['attributes'], user.uid)
        except KeyError:
            raise exceptions.MalformedData()

    def update(self):
        pass

    def delete(self, user):
        self._collection.delete(self.resource.ref, user.uid)

    def replace(self, attributes, user):
        return self._collection.update(self._document.ref, attributes, user.uid, merger=None)

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
        from jam.server.api.v2.history import HistoryView
        return HistoryView(namespace, collection, document)

    @classmethod
    def serializer(cls):
        from jam.server.api.v2.history import HistorySerializer
        return HistorySerializer

    @classmethod
    def self_link(cls, request, document, namespace, collection):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}/collections/{}/documents/{}/history'.format(request.protocol, request.host, namespace.name, collection.name, document.ref)
        return '{}://{}/v2/documents/{}/history'.format(request.protocol, request.host, document.ref)

    @classmethod
    def related_link(cls, request, document, namespace, collection):
        if 'v1' in request.path:
            return '{}://{}/v1/namespaces/{}/collections/{}/documents/{}/history'.format(request.protocol, request.host, namespace.name, collection.name, document.ref)
        return '{}://{}/v2/documents/{}/history'.format(request.protocol, request.host, document.ref)


class DocumentSerializer(Serializer):
    type = 'documents'

    relations = {
        'history': HistoryRelationship
    }

    @classmethod
    def attributes(cls, inst):
        return inst.data
