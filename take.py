import uuid
import time
import enum
import hashlib
import msgpack


class StorageEngine:

    def __init__(self, file_loc):
        self.file_loc = file_loc

    def write(self, key, data):
        assert b'\r\n' not in msgpack.packb(data, use_bin_type=True)
        with open(self.file_loc, 'ab') as fileobj:
            fileobj.write(key.encode('utf-8'))
            fileobj.write(b'\t')
            fileobj.write(msgpack.packb(data, use_bin_type=True))
            fileobj.write(b'\r\n')

    def __iter__(self):
        with open(self.file_loc, 'rb') as fileobj:
            line = fileobj.readline()
            while line:
                yield line.split(b'\t')[0].decode()
                line = fileobj.readline()

    def read(self, key):
        key = key.encode('utf-8')
        try:
            with open(self.file_loc, 'rb') as fileobj:
                line = fileobj.readline()
                while line:
                    if b'\r\n' not in line:
                        line += fileobj.readline()
                    if line.startswith(key):
                        return msgpack.unpackb(line[len(key) + 1:-2], encoding='utf-8')
                    line = fileobj.readline()
        except FileNotFoundError:
            return None


class DataObject:
    file_loc = 'objects.dat'
    StorageEngineClass = StorageEngine
    # TODO Mutex

    @classmethod
    def create(cls, data, alg='sha1'):
        hasher = hashlib.new('sha1')
        hasher.update(data.encode('utf-8'))
        return cls(hasher.hexdigest(), alg, data)

    @classmethod
    def load(cls, key):
        return cls(key, **cls.StorageEngineClass(cls.file_loc).read(key))

    def __init__(self, key, alg, data):
        self.key = key
        self.alg = alg
        self.data = data

    def save(self):
        existing = self.StorageEngineClass(self.file_loc).read(self.key)
        if existing:
            return self.__class__.load(self.key)
        self.StorageEngineClass(self.file_loc).write(self.key, {'alg': self.alg, 'data': self.data})
        return self


class Operations(enum.IntEnum):
    CREATE = 0
    UPDATE = 1
    REPLACE = 2
    DELETE = 3
    SNAPSHOT = 4
    RENAME = 5


class OpLog:
    file_loc = 'operations.dat'
    StorageEngineClass = StorageEngine

    @classmethod
    def list(cls):
        for key in cls.StorageEngineClass(cls.file_loc):
            yield cls.load(key)

    @classmethod
    def create(cls, operation, record_id, data_ref, collection, operation_parameters):
        return cls(
            str(uuid.uuid4()).replace('-', ''),
            time.time(),
            operation,
            record_id,
            data_ref,
            collection,
            operation_parameters
        )

    @classmethod
    def load(cls, key):
        return cls(key, **cls.StorageEngineClass(cls.file_loc).read(key))

    def __init__(self, id, ts, op, r, d, c, op_p):
        self.id = id
        self.timestamp = ts
        self.operation = Operations(op)
        self.record_id = r
        self.data_ref = d
        self.collection_ref = c
        self.operation_parameters = op_p

    def save(self):
        self.StorageEngineClass(self.file_loc).write(self.id, {
            'ts': self.timestamp,
            'op': self.operation,
            'r': self.record_id,
            'd': self.data_ref,
            'c': self.collection_ref,
            'op_p': self.operation_parameters
        })
        return self


class Snapshot(dict):
    DataObjectClass = DataObject

    def read(self, key):
        return self[key]

    def list(self):
        return list(self.keys())

    def apply(self, log):
        if log.operation in (Operations.CREATE, Operations.REPLACE, Operations.UPDATE):
            self[log.record_id] = {**log.__dict__, 'data': self.DataObjectClass.load(log.data_ref).data}
        elif log.operation == Operations.RENAME:
            del self[log.operation_parameters['src']]
            self[log.record_id] = {**log.__dict__, 'data': self.DataObjectClass.load(log.data_ref).data}
        elif log.operation == Operations.DELETE:
            del self[log.record_id]
        else:
            raise Exception('Unknown operation {}'.format(log.operation))
        return self.get(log.record_id)


class Collection:
    SnapshotClass = Snapshot
    DataObjectClass = DataObject
    OperationLogClass = OpLog

    @classmethod
    def load(cls, id):
        collection = cls(id)
        collection.apply(*list(log for log in cls.OperationLogClass.list() if log.collection_ref == collection.id))
        return collection

    def __init__(self, id, snapshot=None):
        self.id = id
        self.snapshot = snapshot or self.SnapshotClass()

    def read(self, key):
        return self.snapshot[key]

    def list(self):
        return self.snapshot.list()

    def create(self, key, data):
        dobj = self.DataObjectClass.create(data).save()
        return self.snapshot.apply(
            self.OperationLogClass.create(Operations.CREATE, key, dobj.key, self.id, {}).save()
        )

    def read(self, key):
        return self.snapshot.read(key)

    def update(self, key, data):
        raise NotImplementedError

    def replace(self, key, data):
        dobj = self.DataObjectClass.create(key, data).save()
        return self.snapshot.apply(
            self.OperationLogClass.create(Operations.REPLACE, key, dobj.key, self.id, {}).save()
        )

    def delete(self, key):
        return self.snapshot.apply(
            self.OperationLogClass.create(Operations.DELETE, key, None, self.id, {}).save()
        )

    def rename(self, key, name):
        return self.snapshot.apply(
            self.OperationLogClass.create(Operations.RENAME, name, self.read(key)['data_ref'], self.id, {'src': key}).save()
        )

    def apply(self, *logs):
        for log in sorted(logs, key=lambda x: x.timestamp):
            self.snapshot.apply(log)
