from iodm.backends.base import Backend


class EphemeralBackend(Backend):

    def __init__(self):
        self._cache = {}

    def get(self, key):
        return self._cache[key]

    def set(self, key, value):
        self._cache[key] = value

    def unset(self, key):
        del self._cache[key]

    def keys(self):
        return self._cache.keys()

    def unset_all(self):
        self._cache = {}
