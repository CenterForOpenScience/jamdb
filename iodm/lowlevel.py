import abc
import enum
import collections


DataObject = collections.namedtuple('DataObject', [
    'id',
    'data'
])


Log = collections.namedtuple('Log', [
    'id',
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

    def __init__(self, collection):
        pass

    @abc.abstractmethod
    def create(self, operation, key, ref, **operation_params):
        raise NotImplementedError

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
    def _create(self, log):
        pass

    @abc.abstractmethod
    def _rename(self, log):
        pass

    @abc.abstractmethod
    def _delete(self, log):
        pass

    def _replace(self, log):
        return self._create(log)

    def _update(self, log):
        return self._create(log)

    def apply(self, log):
        try:
            return {
                Operations.CREATE: self._create,
                Operations.DELETE: self._delete,
                Operations.RENAME: self._rename,
                Operations.REPLACE: self._replace,
                Operations.UPDATE: self._update,
            }[log.operation](log)
        except KeyError:
            raise Exception('Unknown operation {}'.format(log.operation))


class Collection:

    @classmethod
    def load(cls, storage, logger, snapshot):
        snapshot_log = logger.first(lambda l: l.operation == Operations.SNAPSHOT)
        serialized_snapshot = storage.read(snapshot_log.data_ref)
        snapshot.load(serialized_snapshot.data)
        for log in logger.after(snapshot_log.timestamp):
            snapshot.apply(log)
        return cls(storage, logger, snapshot)

    def __init__(self, storage, logger, snapshot):
        self._logger = logger
        self._storage = storage
        self._snapshot = snapshot

    def list(self):
        return self._snapshot.list()

    def create(self, key, data):
        ref = self._storage.create(data)
        log = self._logger.create(Operations.CREATE, key, ref)
        return self._snapshot.apply(log)

    def read(self, key):
        return self._storage.read(self._snapshot.read(key))

    def update(self, key, data, merger):
        original = self._snapshot.read(key)
        ref = self._storage.create(merger(original, data))
        log = self._logger.create(Operations.UPDATE, key, ref)
        return self._snapshot.apply(log)

    def replace(self, key, data):
        ref = self._storage.create(data)
        log = self._logger.create(Operations.REPLACE, key, ref)
        return self._snapshot.apply(log)

    def delete(self, key):
        log = self._logger.create(Operations.DELETE, key, None)
        return self._snapshot.apply(log)

    def rename(self, key, new_key):
        ref = self._snapshot.read(key)
        log = self._logger.create(Operations.RENAME, new_key, ref, **{'from': key, 'to': new_key})
        return self._snapshot.apply(log)

    def snapshot(self):
        ref = self._storage.create(self._snapshot.serialize())
        log = self._logger.create(Operations.SNAPSHOT, None, ref)
        return log
