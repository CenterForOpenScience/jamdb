import json
import hashlib
import collections

from iodm.base import DataObject
from iodm.base import DataObjectSchema
from iodm.backends.translation import TranslatingBackend


class Storage(TranslatingBackend):

    def __init__(self, backend):
        super().__init__(DataObject, DataObjectSchema, backend)

    def create(self, data):
        if isinstance(data, dict):
            data = collections.OrderedDict(data)

        hasher = hashlib.new('sha1')
        hasher.update(json.dumps(data).encode('utf-8'))

        data_obj = DataObject(ref=hasher.hexdigest(), data=data)

        self.set(data_obj.ref, data_obj)

        return data_obj
