import bson

from iodm import Q
from iodm.base import Operation
from iodm.server.api.base import BaseAPIHandler
from iodm.server.api.base import TimeMachineAPIHandler


class DocumentsHandler(TimeMachineAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/documents/?'

    def get(self, *args, **kwargs):
        data = {}
        data_refs = []

        for log in self.collection.list():
            data_refs.append(log.record_id)
            data[log.data_ref] = {
                'id': log.record_id,
                # 'attributes': self.collection.read(log.record_id).data
            }

        for data_object in self.collection._storage._backend.query(Q('ref', 'in', data_refs)):
            data[data_object.ref]['attributes'] = data_object.data

        self.write({'data': list(data.values())})

    def post(self, *args, **kwargs):
        data = self.json['data']

        log = self.collection.create(
            data.get('id') or str(bson.ObjectId()),
            data['attributes']
        )

        self.set_status(201)
        self.write({
            'data': {
                'id': log.record_id,
                'attributes': data['attributes']
            }
        })


class DocumentHandler(BaseAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/documents/(?P<document_id>\w+)/?'

    def initialize(self, namespacer):
        self.namespacer = namespacer

    def prepare(self):
        self.collection = self.namespacer.get_collection(self.path_kwargs['collection_id'])

    def get(self, collection_id, record_id):
        document = self.collection.read(record_id)
        self.write({'data': document.data})

    def delete(self, collection_id, document_id):
        self.collection.delete(document_id)
        self.set_status(204)


class HistoryHandler(BaseAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/documents/(?P<record_id>\w+)/history(?:/(?P<history_id>\w+))?/?'

    def initialize(self, namespacer):
        self.namespacer = namespacer

    def prepare(self):
        self.collection = self.namespacer.get_collection(self.path_kwargs['collection_id'])

    def get(self, collection_id, record_id, history_id=None):
        if history_id:
            log = self.collection._logger.get(history_id)
            return self.write({
                'data': {
                    'id': history_id,
                    'attributes': self.collection._storage.get(log.data_ref).data
                }
            })

        data = []

        for log in self.collection.history(record_id):
            data.append({
                'id': log.ref,
                'attributes': {
                    'data_ref': log.data_ref,
                    'timestamp': log.timestamp,
                    'parameters': log.operation_parameters,
                    'operation': Operation(log.operation).name.lower(),
                }
            })

        self.write({'data': data})
