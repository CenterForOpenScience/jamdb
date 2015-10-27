import json

from iodm.core import Log
from iodm.core import Logger
from iodm.core import Storage
from iodm.core import Snapshot
from iodm.json import JSONDataObject


class RedisStorage(Storage):

    def __init__(self, prefix, connection):
        self._prefix = prefix or ''
        self._connection = connection

    def create(self, data):
        data_object = JSONDataObject.create(data)
        self._connection.set(self._prefix + data_object.id, json.dumps(data_object.to_json()))
        return data_object.id

    def read(self, key):
        return JSONDataObject(
            **json.loads(
                self._connection.get(
                    self._prefix + key
                ).decode()
            )
        )

    def __iter__(self):
        return iter(x.decode().replace(self._prefix, '', 1) for x in self._connection.keys(self._prefix + '*'))


class RedisLogger(Logger):

    def __init__(self, prefix, conneciton):
        self._storage = RedisStorage(prefix, conneciton)

    def create(self, operation, key, ref, **operation_params):
        log = super().create(operation, key, ref, **operation_params)
        self._storage.create(log._asdict())

        return log

    def __iter__(self):
        return iter(sorted((
            Log(**self._storage.read(x).data)
            for x in self._storage),
            reverse=True,
            key=lambda l: l.timestamp,
        ))

    def first(self, condition):
        return next(log for log in self if condition(log))

    def after(self, timestamp):
        for log in self:
            if log.timestamp > timestamp:
                yield log


class RedisSnapshot(Snapshot):

    def __init__(self, connection):
        self._connection = connection

    def read(self, key):
        return json.loads(self._connection.hmget(key, 'data')[0].decode())

    def read_ref(self, key):
        return self._connection.hmget(key, 'ref')[0].decode()

    def list(self):
        return (x.decode() for x in self._connection.keys('*'))

    def load(self, serialized):
        pass

    def serialize(self):
        pass

    def _create(self, log, data_object):
        self._connection.hmset(log.record_id, {'ref': log.data_ref, 'data': json.dumps(data_object.data)})

    def _rename(self, log, data_object):
        self._connection.rename(log.operation_parameters['from'], log.record_id)

    def _delete(self, log, data_object):
        self._connection.delete(log.record_id)
