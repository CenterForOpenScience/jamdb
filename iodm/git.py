import os
import json

from iodm.core import Log
from iodm.core import Logger
from iodm.core import Storage
from iodm.core import DataObject
from iodm.json import JSONDataObject


class FileStorage(Storage):

    def __init__(self, location):
        self.location = location
        os.makedirs(location, exist_ok=True)

    def create(self, data_object):
        prefix, postfix = data_object.ref[:2], data_object.ref[2:]

        path = os.path.join(self.location, prefix)
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, postfix)

        with open(path, 'w') as fileobj:
            fileobj.write(json.dumps(data_object._asdict()))
        return data_object

    def read(self, key):
        path = os.path.join(self.location, key[:2], key[2:])

        with open(path) as fileobj:
            return DataObject(**json.load(fileobj))

    def keys(self):
        files = list(os.scandir(self.location))
        while files:
            cur = files.pop(0)
            if cur.is_file():
                yield ''.join(cur.path.split('/')[-2:])
            else:
                files.extend(list(os.scandir(cur.path)))


class GitStorage(FileStorage):

    def create(self, data):
        return super().create(JSONDataObject.create(data))

    def read(self, key):
        data_object = super().read(key)
        return JSONDataObject(**data_object._asdict())


class GitLogger(Logger):

    def __init__(self, location):
        self._storage = FileStorage(location)

    def create(self, operation, key, ref, **operation_params):
        log = super().create(operation, key, ref, **operation_params)
        self._storage.create(DataObject(ref=log.ref, data=log._asdict()))

        return log

    def __iter__(self):
        return reversed([Log(**self._storage.read(x).data) for x in self._storage.keys()])

    def first(self, condition):
        return next(log for log in self if condition(log))

    def after(self, timestamp):
        for log in self:
            if log.timestamp > timestamp:
                yield log
