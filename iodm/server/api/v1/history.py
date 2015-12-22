import operator
import functools
import datetime

import iodm
from iodm.base import Operation
from iodm.auth import Permissions
from iodm.server.api.v1.base import APIResource
from iodm.server.api.v1.document import DocumentResource


class HistoryResource(APIResource):

    PAGE_SIZE = 50

    @classmethod
    def serialize(self, log, request):
        return {
            'id': log.ref,
            'type': 'history',
            'attributes': {
                'record-id': log.record_id,
                'operation': str(log.operation),
                'parameters': log.operation_parameters,
            },
            'meta': {
                'created-by': log.created_by,
                'modified-by': log.modified_by,
                'created-on': datetime.datetime.fromtimestamp(log.created_on).isoformat(),
                'modified-on': datetime.datetime.fromtimestamp(log.created_on).isoformat()
            },
        }

    @property
    def document(self):
        return self.parent.resource

    @property
    def collection(self):
        return self.parent.parent.resource

    def __init__(self):
        super().__init__('history', DocumentResource, plural='history')

    def get_permissions(self, request):
        return Permissions.ADMIN

    def load(self, history_id, request):
        return super().load(self.collection._logger.read(history_id))

    def read(self, user):
        log = self.resource
        return {
            'id': log.ref,
            'attributes': self.collection._storage.get(log.data_ref).data,
            'meta': {
                'createdBy': log.created_by,
                'createdOn': log.created_on,
                'modifiedBy': log.modified_by,
                'modifiedOn': log.modified_on,
                'parameters': log.operation_parameters,
                'operation': Operation(log.operation).name.lower(),
            },
            'links': {}
        }

        return self.document.to_json_api()

    def list(self, user, page=0, filter=None):
        selector = self.collection._logger._backend.select().order_by(
            iodm.O.Ascending('ref')
        ).page(page, self.PAGE_SIZE)

        query = functools.reduce(operator.and_, [
            iodm.Q(key, 'eq', value)
            for key, value in
            (filter or {}).items()
        ], iodm.Q('record_id', 'eq', self.document.ref))

        return selector.where(query)
