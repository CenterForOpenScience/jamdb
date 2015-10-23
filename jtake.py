import json
from collections import OrderedDict

import take


class JSONDataObject(take.DataObject):

    @classmethod
    def create(cls, data, alg='sha1'):
        return super(JSONDataObject, cls).create(
            json.dumps(OrderedDict(data)),
            alg=alg
        )

    def __init__(self, key, alg, data):
        self.key = key
        self.alg = alg
        self.data = OrderedDict(json.loads(data))

    def save(self):
        existing = self.StorageEngineClass(self.file_loc).read(self.key)
        if existing:
            return self.__class__.load(self.key)
        self.StorageEngineClass(self.file_loc).write(self.key, {'alg': self.alg, 'data': json.dumps(self.data)})
        return self


class Snapshot(take.Snapshot):
    DataObjectClass = JSONDataObject


class Collection(take.Collection):
    SnapshotClass = Snapshot
    DataObjectClass = JSONDataObject

    def update(self, key, data):
        dobj = self.DataObjectClass.create({**self.read(key), **data}).save()
        return self.snapshot.apply(
            self.OperationLogClass.create(take.Operations.UPDATE, key, dobj.key, self.id, {}).save()
        )
