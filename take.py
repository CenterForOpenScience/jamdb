import uuid
import time
import enum
import hashlib
import msgpack


class StorageEngine:

    def __init__(self, file_loc):
        self.file_loc = file_loc

    def write(self, key, data):
        with open(self.file_loc, 'ab') as fileobj:
            fileobj.write(key.encode('utf-8'))
            fileobj.write(b'\t')
            fileobj.write(msgpack.packb(data, use_bin_type=True))
            fileobj.write(b'\n')

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
                    if line.startswith(key):
                        return msgpack.unpackb(line[len(key) + 1:-1], encoding='utf-8')
                    line = fileobj.readline()
        except FileNotFoundError:
            return None


class DataObject:
    file_loc = 'objects.dat'
    # TODO Mutex

    @classmethod
    def create(cls, data, alg='sha1'):
        hasher = hashlib.new('sha1')
        hasher.update(data.encode('utf-8'))
        return cls(hasher.hexdigest(), alg, data)

    @classmethod
    def load(cls, key):
        return cls(key, **StorageEngine(cls.file_loc).read(key))

    def __init__(self, key, alg, data):
        self.key = key
        self.alg = alg
        self.data = data

    def save(self):
        existing = StorageEngine(self.file_loc).read(self.key)
        if existing:
            return self.__class__.load(self.key)
        StorageEngine(self.file_loc).write(self.key, {'alg': self.alg, 'data': self.data})
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

    @classmethod
    def list(cls):
        for key in StorageEngine(cls.file_loc):
            yield cls.load(key)

    @classmethod
    def create(cls, operation, record_id, data_ref, collection, operation_parameters):
        return cls(
            str(uuid.uuid4()),
            time.time(),
            operation,
            record_id,
            data_ref,
            collection,
            operation_parameters
        )

    @classmethod
    def load(cls, key):
        return cls(key, **StorageEngine(cls.file_loc).read(key))

    def __init__(self, id, ts, op, r, d, c, op_p):
        self.id = id
        self.timestamp = ts
        self.operation = Operations(op)
        self.record_id = r
        self.data_ref = d
        self.collection_ref = c
        self.operation_parameters = op_p

    def save(self):
        StorageEngine(self.file_loc).write(self.id, {
            'ts': self.timestamp,
            'op': self.operation,
            'r': self.record_id,
            'd': self.data_ref,
            'c': self.collection_ref,
            'op_p': self.operation_parameters
        })
        return self


class Collection:

    @classmethod
    def load(cls, id):
        collection = cls(id)
        collection.apply(*(log for log in OpLog.list() if log.collection_ref == collection.id))
        return collection

    def __init__(self, id):
        self.id = id
        self.snapshot = {}

    def read(self, key):
        return self.snapshot[key]

    def list(self):
        return list(self.snapshot.keys())

    def create(self, key, data):
        dobj = DataObject.create(data).save()
        log = OpLog.create(Operations.CREATE, key, dobj.key, self.id, {}).save()
        self.snapshot[key] = {**log.__dict__, 'data': data}
        return self.snapshot[key]

    def read(self, key):
        return self.snapshot[key]

    def update(self, key):
        raise NotImplementedError

    def replace(self, key, data):
        dobj = DataObject.create(key, data).save()
        log = OpLog.create(Operations.REPLACE, key, dobj.key, self.id, {}).save()
        self.snapshot[key] = {**log.__dict__, 'data': data}
        return self.snapshot[key]

    def delete(self, key):
        del self.snapshot[key]
        OpLog.create(Operations.DELETE, key, None, self.id, {}).save()

    def rename(self, key, name):
        old = self.read(key)
        log = OpLog.create(Operations.RENAME, name, old['data_ref'], self.id, {'src': key}).save()
        self.snapshot[name] = {**log.__dict__, 'data': self.snapshot.pop(key)['data']}
        return self.snapshot[name]

    def apply(self, *logs):
        for log in logs:
            if log.operation == Operations.CREATE:
                self.snapshot[log.record_id] = {**log.__dict__, 'data': DataObject.load(log.data_ref).data}
            elif log.operation == Operations.RENAME:
                del self.snapshot[log.operation_parameters['src']]
                self.snapshot[log.record_id] = {**log.__dict__, 'data': DataObject.load(log.data_ref).data}
            elif log.operation == Operations.UPDATE:
                self.snapshot[log.record_id] = {**log.__dict__, 'data': DataObject.load(log.data_ref).data}
            elif log.operation == Operations.DELETE:
                del self.snapshot[log.record_id]
            elif log.operation == Operations.REPLACE:
                self.snapshot[log.record_id] = {**log.__dict__, 'data': DataObject.load(log.data_ref).data}
            else:
                raise Exception('Unknown operation {}'.format(log.operation))
