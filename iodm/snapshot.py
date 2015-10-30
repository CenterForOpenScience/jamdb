from iodm.base import Log
from iodm.base import LogSchema
from iodm.base import Operation
from iodm.backends.ext import TranslatingBackend


class Snapshot:

    def __init__(self, backend):
        self._backend = TranslatingBackend(Log, LogSchema, backend)

    def clear(self):
        self._backend.unset_all()

    def get(self, key):
        return self._backend.get(key)

    def list(self):
        return self._backend.list()

    def serialize(self):
        return []

    def _create(self, log, safe=True):
        self._backend.set(log.record_id, log)
        return log

    def _rename(self, log, safe=True):
        if 'to' in log.operation_parameters:
            self._backend.unset(log.record_id)
        else:
            self._backend.set(log.record_id, log)

    def _delete(self, log, safe=True):
        self._backend.unset(log.record_id)

    def _replace(self, log, safe=True):
        return self._create(log)

    def _update(self, log, safe=True):
        return self._create(log)

    def apply(self, log, safe=True):
        try:
            op = {
                Operation.CREATE: self._create,
                Operation.DELETE: self._delete,
                Operation.RENAME: self._rename,
                Operation.REPLACE: self._replace,
                Operation.UPDATE: self._update,
            }[log.operation]
        except KeyError:
            raise Exception('Unknown operation {}'.format(log.operation))
        return op(log, safe=True)
