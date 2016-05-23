from jam import settings
from jam import exceptions
from jam.backends.base import Backend


class EphemeralBackend(Backend):
    _cls_cache = {}

    @classmethod
    def is_connected(cls):
        return settings.EPHEMERAL['USE']

    @classmethod
    def settings_for(cls, namespace_id, collection_id, type_):
        return {
            'key': '{}-{}-{}'.format(type_, namespace_id, collection_id)
        }

    def __init__(self, key):
        self._key = key
        self._cache = EphemeralBackend._cls_cache.setdefault(key, {})

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
        EphemeralBackend._cls_cache.pop(self._key, None)
