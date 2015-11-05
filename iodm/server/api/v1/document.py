import bson

from iodm.auth import User
from iodm.base import Operation
from iodm.auth import Permissions
from iodm.server.api.base import BaseAPIHandler
from iodm.server.api.base import TimeMachineAPIHandler


class DocumentsHandler(TimeMachineAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/documents/?'

    def prepare(self):
        super().prepare()
        self.permissions = Permissions.get_permissions(self.current_user, self.namespacer, self.collection)

        assert Permissions.from_method(self.request.method) & self.permissions

    def get(self, *args, **kwargs):
        self.write([
            document.to_json_api()
            for document in self.collection.list()
        ])

    def post(self, *args, **kwargs):
        data = self.json['data']

        document = self.collection.create(
            data.get('id') or str(bson.ObjectId()),
            data['attributes'],
            self.current_user.uid
        )

        self.set_status(201)
        self.write(document.to_json_api())


class DocumentHandler(TimeMachineAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/documents/(?P<document_id>\w+)/?'

    def prepare(self):
        super().prepare()

        self.permissions = Permissions.get_permissions(self.current_user, self.namespacer)
        assert Permissions.from_method(self.request.method) & self.permissions

        # self.collection = self.namespacer.get_collection(self.path_kwargs['collection_id'])
        self.permissions |= Permissions.get_permissions(self.current_user, self.collection)
        assert Permissions.from_method(self.request.method) & self.permissions

        self.document = self.collection.read(self.path_kwargs['document_id'])
        self.permissions |= Permissions.get_permissions(self.current_user, self.document)
        assert Permissions.from_method(self.request.method) & self.permissions

    def get(self, **kwargs):
        self.write(self.document.to_json_api())

    def delete(self, **kwargs):
        self.collection.delete(self.document.ref, self.current_user.uid)
        self.set_status(204)

    def put(self, **kwargs):
        new_doc = self.collection.update(self.document.ref, self.json['data']['attributes'], self.current_user.uid)
        self.set_status(200)
        self.write(new_doc.to_json_api())

    def patch(self, **kwargs):
        new_doc = self.collection.update(
            self.document.ref,
            self.json['data']['attributes'],
            self.current_user.uid,
            merger=lambda x, y: {**x, **y}
        )
        self.set_status(200)
        self.write(new_doc.to_json_api())


class HistoryHandler(TimeMachineAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/documents/(?P<document_id>\w+)/history(?:/(?P<history_id>\w+))?/?'

    def prepare(self):
        super().prepare()

        self.permissions = Permissions.get_permissions(self.current_user, self.namespacer)
        assert Permissions.from_method(self.request.method) & self.permissions

        # self.collection = self.namespacer.get_collection(self.path_kwargs['collection_id'])
        self.permissions |= Permissions.get_permissions(self.current_user, self.collection)
        assert Permissions.from_method(self.request.method) & self.permissions

        self.document = self.collection.read(self.path_kwargs['document_id'])
        self.permissions |= Permissions.get_permissions(self.current_user, self.document)
        assert Permissions.from_method(self.request.method) & self.permissions

    def get(self, collection_id, document_id, history_id=None):
        if history_id:
            log = self.collection._logger.get(history_id)
            return self.write({
                'id': log.ref,
                'attributes': self.collection._storage.get(log.data_ref).data,
                'meta': {
                    'createdBy': log.created_by,
                    'createdOn': log.created_on,
                    'modifiedBy': log.modified_by,
                    'modifiedOn': log.modified_on,
                    'parameters': log.operation_parameters,
                    'operation': Operation(log.operation).name.lower(),
                }
            })

        data = []
        for log in self.collection.history(document_id):
            data.append({
                'id': log.ref,
                'attributes': self.collection._storage.get(log.data_ref).data,
                'meta': {
                    'createdBy': log.created_by,
                    'createdOn': log.created_on,
                    'modifiedBy': log.modified_by,
                    'modifiedOn': log.modified_on,
                    'parameters': log.operation_parameters,
                    'operation': Operation(log.operation).name.lower(),
                }
            })
        self.write(data)
