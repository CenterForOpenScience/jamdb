from iodm import exceptions
from iodm.backends.base import Backend


class EphemeralBackend(Backend):

    def __init__(self):
        self._cache = {}

    def get(self, key):
        try:
            return self._cache[key]
        except KeyError:
            raise exceptions.NotFound(key)

    def set(self, key, value):
        self._cache[key] = value

    def unset(self, key):
        del self._cache[key]

    def keys(self):
        return self._cache.keys()

    def unset_all(self):
        self._cache = {}
