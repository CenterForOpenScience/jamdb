import time

import bson

from iodm import Q
from iodm import O
from iodm.models import Log
from iodm.base import Operation
from iodm.backends.ext import TranslatingBackend
from iodm.backends.ext import ReadOnlyFilteredBackend


class ReadOnlyLogger:

    __version__ = '0.0.0'

    def __init__(self, backend):
        self._backend = TranslatingBackend(Log, backend)

    def get(self, ref):
        return self._backend.get(ref)

    def latest_snapshot(self):
        return self._backend.first(Q('operation', 'eq', Operation.SNAPSHOT), O('modified_on', O.DESCENDING))

    def after(self, timestamp):
        return self._backend.query(Q('modified_on', 'gt', timestamp), O('modified_on', O.ASCENDING))

    def history(self, record_id):
        """Returns all logs pretaining to the specified record_id newest to oldest
            >>> self.history('myid')[0]  # Current state
            >>> self.history('myid')[-1]  # Initial value, generally a rename or create
        """
        return self._backend.query(Q('record_id', 'eq', record_id), O('modified_on', O.DESCENDING))

    def list(self, order=None):
        return self._backend.list(order)

    def bulk_read(self, keys):
        return self._backend.query(Q('ref', 'in', keys))

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self._backend)


class Logger(ReadOnlyLogger):

    def create(self, key, operation, data_ref, user, previous=None, operation_parameters=None):
        modified_on = time.time()

        if previous:
            created_by = previous.created_by
            created_on = previous.created_on
        else:
            created_by = user
            created_on = modified_on

        log = Log(
            ref=str(bson.ObjectId()),
            data_ref=data_ref,
            record_id=key,

            version=self.__version__,

            operation=operation,
            operation_parameters=operation_parameters or {},

            created_by=created_by,
            created_on=created_on,
            modified_by=user,
            modified_on=modified_on,
        )

        self._backend.set(log.ref, log)

        return log

    def at_time(self, timestamp):
        return FrozenLogger(timestamp, self._backend.raw_backend())


class FrozenLogger(ReadOnlyLogger):
    """A Read-only logger that limits access to logs before the given timestamp"""

    def __init__(self, timestamp, backend):
        self.timestamp = timestamp
        super().__init__(ReadOnlyFilteredBackend(Q('modified_on', 'lte', timestamp), backend))

    def create_snapshot(self, data_ref):
        log = Log(
            ref=str(bson.ObjectId()),
            data_ref=data_ref,
            record_id=None,

            version=self.__version__,

            operation=Operation.SNAPSHOT,
            operation_parameters={},

            created_by=None,
            created_on=self.timestamp,
            modified_by=None,
            modified_on=self.timestamp,
        )

        TranslatingBackend(Log, self._backend.raw_backend()).set(log.ref, log)
        return log
