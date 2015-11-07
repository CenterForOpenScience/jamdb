
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
        url = '{}://{}{}/'.format(self.request.protocol, self.request.host, self.request.path.rstrip('/'))

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
                },
                'links': {
                    'self': url + log.ref
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
                },
                'links': {
                    'self': url + log.ref
                }
            })
        self.write(data)
