from iodm.base import Operation
from iodm.models.document import Document
from iodm.backends.ext import TranslatingBackend


class State:

    def __init__(self, backend):
        self._backend = TranslatingBackend(Document, backend)

    def clear(self):
        self._backend.unset_all()

    def get(self, key):
        return self._backend.get(key)

    def list(self):
        return self._backend.list()

    def keys(self):
        return self._backend.keys()

    def _create(self, log, data, safe=True):
        doc = Document.create(log, data)
        self._backend.set(log.record_id, doc)
        return doc

    def _rename(self, log, data, safe=True):
        if 'to' in log.operation_parameters:
            self._backend.unset(log.record_id)
        else:
            doc = Document.create(log, data)
            self._backend.set(log.record_id, doc)
            return doc

    def _delete(self, log, data, safe=True):
        self._backend.unset(log.record_id)

    def _replace(self, log, data, safe=True):
        return self._create(log, data)

    def _update(self, log, data, safe=True):
        return self._create(log, data, safe=True)

    def apply(self, log, data, safe=True):
        # TODO implement safe
        # Snapshot logs may be out of order, which should not matter
        # Deleting a key that doesn't exist would cause an exception, safe would just swallow that failure
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
        return op(log, data, safe=safe)
