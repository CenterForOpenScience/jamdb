from iodm.backends.base import ReadOnlyBackend


class ReadOnlyFilteredBackend(ReadOnlyBackend):

    def __init__(self, query, backend):
        self._query = query
        self._backend = backend

    def get(self, key):
        obj = self._backend.get(key)
        if self.query.as_lambda(obj):
            return obj

    def keys(self):
        raise NotImplementedError

    def query(self, query, order=None):
        return self._backend.query(self._query & query, order)

    def list(self, order=None):
        return self._backend.query(self._query, order)
