import time

import bson

from iodm import Q
from iodm import O
from iodm.base import Log
from iodm.base import LogSchema
from iodm.base import Operation
from iodm.backends.translation import TranslatingBackend


class Logger:

    __version__ = '0.0.0'

    def __init__(self, backend):
        self._backend = TranslatingBackend(Log, LogSchema, backend)

    def create(self, operation, key, data_ref, **operation_parameters):
        log = Log(
            ref=str(bson.ObjectId()),
            record_id=key,
            data_ref=data_ref,
            timestamp=time.time(),
            version=self.__version__,
            operation=Operation(operation),
            operation_parameters=operation_parameters
        )

        self._backend.set(log.ref, log)
        return log

    def get(self, ref):
        return self._backend.get(ref)

    def latest_snapshot(self):
        try:
            return self._backend.first(Q('operation', 'eq', 1))
        except Exception:
            return None

    def after(self, timestamp):
        return self._backend.query(Q('timestamp', 'gt', timestamp))

    def history(self, record_id):
        return self._backend.query(Q('record_id', 'eq', record_id), O('timestamp', -1))

    def list(self, order=None):
        return self._backend.list(order)