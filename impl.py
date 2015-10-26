import os
import json
import time
import hashlib

import bson

from iodm import lowlevel


class JSONDataObject(lowlevel.DataObject):

    @classmethod
    def create(cls, data):
        hasher = hashlib.new('sha1')
        hasher.update(json.dumps(data).encode('utf-8'))
        return cls(id=hasher.hexdigest(), data=data)

    def to_json(self):
        return {'id': self.id, 'data': self.data}


class GitStorage(lowlevel.Storage):

    def __init__(self, location):
        os.makedirs(location, exist_ok=True)
        self.location = location
        super().__init__()

    def create(self, data):
        data_object = JSONDataObject.create(data)

        prefix, postfix = data_object.id[:2], data_object.id[2:]

        path = os.path.join(self.location, prefix)
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, postfix)

        with open(path, 'w') as fileobj:
            fileobj.write(json.dumps(data_object.to_json()))
        return data_object.id

    def read(self, key):
        path = os.path.join(self.location, key[:2], key[2:])

        with open(path) as fileobj:
            return JSONDataObject(**json.load(fileobj))

    def __iter__(self):
        files = list(os.scandir(self.location))
        while files:
            cur = files.pop(0)
            if cur.is_file():
                yield ''.join(cur.path.split('/')[-2:])
            else:
                files.extend(list(os.scandir(cur.path)))


class GitLogger(lowlevel.Logger):

    def __init__(self, location):
        self._storage = GitStorage(location)

    def create(self, operation, key, ref, **operation_params):
        log = lowlevel.Log(
            id=str(bson.ObjectId()),
            data_ref=ref,
            record_id=key,
            operation=operation,
            timestamp=time.time(),
            operation_parameters=operation_params
        )
        self._storage.create(log.__dict__)

        return log

    def __iter__(self):
        return iter(sorted((
            lowlevel.Log(**self._storage.read(x).data)
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


class EphemeralSnapshot(lowlevel.Snapshot):

    def __init__(self):
        self._cache = {}
        super().__init__()

    def read(self, key):
        return self._cache[key]

    def serialize(self):
        return self._cache

    def list(self):
        return list(self._cache.keys())

    def load(self, serialized):
        self._cache = serialized

    def _create(self, log):
        self._cache[log.record_id] = log.data_ref

    def _delete(self, log):
        del self._cache[log.record_id]

    def _rename(self, log):
        del self._cache[log.operation_params['from']]
        self._cache[log.record_id] = log.data_ref


if __name__ == '__main__':
    collection = lowlevel.Collection(
        GitStorage('data/data'),
        GitLogger('data/logs'),
        EphemeralSnapshot()
    )

    collection.create('key', {'val': 'ew'})
    assert collection.read('key').data == {'val': 'ew'}
    collection.snapshot()

    loaded = lowlevel.Collection.load(
        GitStorage('data/data'),
        GitLogger('data/logs'),
        EphemeralSnapshot()
    )

    assert loaded.read('key').data == {'val': 'ew'}
