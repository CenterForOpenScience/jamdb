from jam.backends.base import ReadOnlyBackend


class ReadOnlyFilteredBackend(ReadOnlyBackend):

    def __init__(self, query, backend):
        self._query = query
        self._backend = backend

    def get(self, key):
        obj = self._backend.get(key)
        if self._query.as_lambda()(obj):
            return obj

    def keys(self):
        raise NotImplementedError

    def query(self, query, *args, **kwargs):
        return self._backend.query(self._query & query, *args, **kwargs)

    def count(self, query):
        return self._backend.count(query)

    def list(self, order=None):
        return self._backend.query(self._query, order)

    def raw_backend(self):
        return self._backend.raw_backend()
