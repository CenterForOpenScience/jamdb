from iodm.backends.base import Backend


class TranslatingBackend(Backend):

    def __init__(self, obj, schema, backend):
        self.obj = obj
        self.schema = schema()
        self.backend = backend

    def deserialize(self, data):
        return self.obj(**self.schema.load(data).data)

    def serialize(self, obj):
        return self.schema.dump(obj._asdict()).data

    def get(self, key):
        return self.deserialize(self.backend.get(key))

    def set(self, key, obj):
        return self.backend.set(key, self.serialize(obj))

    def unset(self, key):
        return self.backend.unset(key)

    def unset_all(self):
        return self.backend.unset_all()

    def keys(self):
        return self.backend.keys()

    def query(self, query, order=None):
        for data in self.backend.query(query, order):
            yield self.deserialize(data)

    def list(self, order=None):
        for data in self.backend.list(order):
            yield self.deserialize(data)
