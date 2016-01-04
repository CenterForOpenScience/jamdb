from jam.backends.base import Backend


class TranslatingBackend(Backend):

    def __init__(self, obj, backend):
        self.obj = obj
        self._backend = backend

    def deserialize(self, data):
        return self.obj.deserialize(data)

    def serialize(self, obj):
        return self.obj.serialize(obj)

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

    def query(self, *args, **kwargs):
        for data in self._backend.query(*args, **kwargs):
            yield self.deserialize(data)

    def count(self, query):
        return self._backend.count(query)

    def list(self, order=None):
        for data in self._backend.list(order):
            yield self.deserialize(data)

    def raw_backend(self):
        return self._backend.raw_backend()
