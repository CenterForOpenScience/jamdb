import abc
import enum
import time
import collections

import bson


DataObject = collections.namedtuple('DataObject', [
    'ref',
    'data'
])


Log = collections.namedtuple('Log', [
    'ref',
    'version',
    'data_ref',
    'operation',
    'record_id',
    'timestamp',
    'operation_parameters',
])


class Operations(enum.IntEnum):
    CREATE = 0
    UPDATE = 1
    REPLACE = 2
    DELETE = 3
    SNAPSHOT = 4
    RENAME = 5


class Storage(abc.ABC):

    @abc.abstractmethod
    def create(data):
        raise NotImplementedError

    @abc.abstractmethod
    def read(key):
        raise NotImplementedError


class Logger(abc.ABC):

    __version__ = '0.0.0'

    @abc.abstractmethod
    def create(self, operation, key, ref, **operation_params):
        return Log(
            ref=str(bson.ObjectId()),
            data_ref=ref,
            record_id=key,
            operation=operation,
            timestamp=time.time(),
            version=self.__version__,
            operation_parameters=operation_params
        )

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError


class Snapshot(abc.ABC):

    @abc.abstractmethod
    def read(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        pass

    @abc.abstractmethod
    def serialize(self):
        pass

    @abc.abstractmethod
    def _create(self, log, data_object):
        pass

    @abc.abstractmethod
    def _rename(self, log, data_object):
        pass

    @abc.abstractmethod
    def _delete(self, log, data_object):
        pass

    def _replace(self, log, data_object):
        return self._create(log, data_object)

    def _update(self, log, data_object):
        return self._create(log, data_object)

    def apply(self, log, data_object):
        try:
            return {
                Operations.CREATE: self._create,
                Operations.DELETE: self._delete,
                Operations.RENAME: self._rename,
                Operations.REPLACE: self._replace,
                Operations.UPDATE: self._update,
            }[log.operation](log, data_object)
        except KeyError:
            raise Exception('Unknown operation {}'.format(log.operation))


class Collection:

    def __init__(self, storage, logger, snapshot, regenerate=True):
        self._logger = logger
        self._storage = storage
        self._snapshot = snapshot
        if regenerate:
            # Oddity with regenerate + snapshot
            self.regenerate()

    def regenerate(self):
        self._snapshot.clear()

        log, snapshot = self._lastest_snapshot()
        if log:
            self.load_snapshot(snapshot)
            logs = self._logger.after(log.timestamp)
        else:
            logs = self._logger.list(order=1)  # Ascending

        for log in logs:
            self._snapshot.apply(log)

        return True

    def _lastest_snapshot(self):
        try:
            # Maybe moved into logs
            # logger.get_snapshot
            # logger.get_by_operation
            log = self._logger.first(lambda l: l.operation == Operations.SNAPSHOT)
        except StopIteration:
            return None, []

        return log, self._storage.load(log.data_ref).data

    def list(self):
        return self._snapshot.list()

    def create(self, key, data):
        data_object = self._storage.create(data)
        log = self._logger.create(Operations.CREATE, key, data_object.ref)
        return self._snapshot.apply(log, data_object)

    def read(self, key):
        return self._storage.read(self._snapshot.read(key))

    def update(self, key, data, merger):
        original = self._snapshot.read(key)
        data_object = self._storage.create(merger(original, data))
        log = self._logger.create(Operations.UPDATE, key, data_object.ref)
        return self._snapshot.apply(log, data_object)

    def replace(self, key, data):
        data_object = self._storage.create(data)
        log = self._logger.create(Operations.REPLACE, key, data_object.ref)
        return self._snapshot.apply(log, data_object)

    def delete(self, key):
        log = self._logger.create(Operations.DELETE, key, None)
        return self._snapshot.apply(log, None)

    def rename(self, key, new_key):
        ref = self._snapshot.read_ref(key)
        log = self._logger.create(Operations.RENAME, new_key, ref, **{'from': key, 'to': new_key})
        return self._snapshot.apply(log, None)

    def snapshot(self):
        data_object = self._storage.create(self._snapshot.serialize())
        log = self._logger.create(Operations.SNAPSHOT, None, data_object.ref)
        return log
