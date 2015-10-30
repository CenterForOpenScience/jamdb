import time

import bson

from iodm import Q
from iodm import O
from iodm.base import Log
from iodm.base import LogSchema
from iodm.base import Operation
from iodm.backends.ext import TranslatingBackend
from iodm.backends.ext import ReadOnlyFilteredBackend


class ReadOnlyLogger:

    __version__ = '0.0.0'

    def __init__(self, backend):
        self._backend = TranslatingBackend(Log, LogSchema, backend)

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


class Logger(ReadOnlyLogger):

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

    def at_time(self, timestamp):
        return FrozenLogger(timestamp, self._backend._backend)


class FrozenLogger(ReadOnlyLogger):
    """A Read-only logger that limits access to logs before the given timestamp"""

    def __init__(self, timestamp, backend):
        super().__init__(backend)
        self._backend = ReadOnlyFilteredBackend(
            Q('timestamp', 'eq', timestamp),
            self._backend
        )
