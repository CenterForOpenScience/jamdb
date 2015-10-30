import json
import hashlib
import collections

from iodm.base import DataObject
from iodm.base import DataObjectSchema
from iodm.backends.ext import TranslatingBackend


class ReadOnlyStorage:

    def __init__(self, backend):
        self._backend = TranslatingBackend(DataObject, DataObjectSchema, backend)

    def get(self, key):
        return self._backend.get(key)


class Storage(ReadOnlyStorage):

    def create(self, data):
        if isinstance(data, dict):
            data = collections.OrderedDict(data)

        hasher = hashlib.new('sha1')
        hasher.update(json.dumps(data).encode('utf-8'))

        data_obj = DataObject(ref=hasher.hexdigest(), data=data)

        self._backend.set(data_obj.ref, data_obj)

        return data_obj
