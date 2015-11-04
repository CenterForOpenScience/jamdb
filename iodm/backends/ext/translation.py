from iodm.backends.base import Backend


class TranslatingBackend(Backend):

    def __init__(self, obj, backend):
        self.obj = obj
        # self.schema = schema()
        self._backend = backend

    def deserialize(self, data):
        # Note: Bottle neck here, data marshalling is sloooow
        # TODO reimplement
        return self.obj.deserialize(data)
        # return self.obj(**self.schema.load(data).data)

    def serialize(self, obj):
        return self.obj.serialize(obj)
        # return self.schema.dump(obj._asdict()).data

    def get(self, key):
        return self.deserialize(self._backend.get(key))

    def set(self, key, obj):
        return self._backend.set(key, self.serialize(obj))

    def unset(self, key):
        return self._backend.unset(key)

    def unset_all(self):
        return self._backend.unset_all()

    def keys(self):
        return self._backend.keys()

    def query(self, query, order=None):
        for data in self._backend.query(query, order):
            yield self.deserialize(data)

    def list(self, order=None):
        for data in self._backend.list(order):
            yield self.deserialize(data)

    def raw_backend(self):
        return self._backend.raw_backend()
