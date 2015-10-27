from iodm.core import Snapshot


class EphemeralSnapshot(Snapshot):

    def __init__(self):
        self._cache = {}
        super().__init__()

    def read(self, key):
        return self._cache[key]['data_ref']

    def serialize(self):
        return self._cache

    def list(self):
        return list(self._cache.keys())

    def load(self, serialized):
        self._cache = serialized

    def _create(self, log, data_object):
        self._cache[log.record_id] = {'ref': log.data_ref, 'data': data_object.data}

    def _delete(self, log, data_object):
        del self._cache[log.record_id]

    def _rename(self, log, data_object):
        self._cache[log.record_id] = self._cache.pop(log.operation_parameters['from'])
