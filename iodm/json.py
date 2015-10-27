import json
import hashlib

from iodm.core import DataObject


class JSONDataObject(DataObject):
    alg = 'sha1'

    @classmethod
    def create(cls, data):
        hasher = hashlib.new(cls.alg)
        hasher.update(json.dumps(data).encode('utf-8'))
        return cls(ref=hasher.hexdigest(), alg=cls.alg, data=data)

    def to_json(self):
        return {'ref': self.ref, 'alg': self.alg, 'data': self.data}
