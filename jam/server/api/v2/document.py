from jam import Q
from jam import exceptions
from jam.auth import Permissions
from jam.server.api.v2.base import View
from jam.server.api.v2.base import Serializer
from jam.server.api.v2.collection import CollectionView


class DocumentSerializer(Serializer):
    type = 'documents'

    @classmethod
    def attributes(cls, inst):
        return inst.data


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

    def create(self, id, attributes, user, **relationships):
        return self._collection.create(id, attributes, user.uid)

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
