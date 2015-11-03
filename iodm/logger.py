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
        return self._backend.first(Q('operation', 'eq', Operation.SNAPSHOT), O('timestamp', O.DESCENDING))

    def after(self, timestamp):
        return self._backend.query(Q('timestamp', 'gt', timestamp), O('timestamp', O.ASCENDING))

    def history(self, record_id):
        """Returns all logs pretaining to the specified record_id newest to oldest
            >>> self.history('myid')[0]  # Current state
            >>> self.history('myid')[-1]  # Initial value, generally a rename or create
        """
        return self._backend.query(Q('record_id', 'eq', record_id), O('timestamp', O.DESCENDING))

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
        super().__init__(ReadOnlyFilteredBackend(Q('timestamp', 'eq', timestamp), backend))
