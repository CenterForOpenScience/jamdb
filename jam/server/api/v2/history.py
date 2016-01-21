from jam import Q
from jam.auth import Permissions
from jam.server.api.v2.base import View
from jam.server.api.v2.base import Serializer
from jam.server.api.v2.document import DocumentView


class HistorySerializer(Serializer):
    type = 'history'

    @classmethod
    def attributes(cls, inst):
        return {
            'record-id': inst.record_id,
            'operation': str(inst.operation),
            'parameters': inst.operation_parameters,
        }


class HistoryView(View):

    name = 'history'
    plural = 'history'
    parent = DocumentView

    @classmethod
    def load(self, id, namespace, collection, document):
        return super().load(collection._logger.read(id))

    def __init__(self, namespace, collection, document, resource=None):
        super().__init__(namespace, collection, document, resource=resource)
        self._history = resource
        self._document = document
        self._namespace = namespace
        self._collection = collection

    def get_permissions(self, request):
        return Permissions.ADMIN  # TODO What should this really be?

    def create(self, id, attributes, user, **relationships):
        return self._collection.create(id, attributes, user.uid)

    def update(self):
        pass

    def delete(self, user):
        self._collection.delete(self.resource.ref, user.uid)

    def replace(self, attributes, user):
        return self._collection.update(self._document.ref, attributes, user.uid, merger=None)

    def list(self, filter, sort, page, page_size, user):
        selector = self._collection._logger._backend.select()
        if filter:
            filter &= Q('record_id', 'eq', self._document.ref)
        else:
            filter = Q('record_id', 'eq', self._document.ref)

        return selector.where(filter).page(page, page_size).order_by(sort)
