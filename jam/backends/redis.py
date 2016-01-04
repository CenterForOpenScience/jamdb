# from redis import Redis

from iodm.backends.base import Backend


class RedisBackend(Backend):

    def __init__(self, connection=None, database=0):
        self._connection = connection or Redis(decode_responses=True, db=database)

    def get(self, key):
        t = self._connection.type(key)
        if t == 'string':
            return self._connection.get(key)
        elif t == 'hash':
            data = self._connection.hgetall(key)
            # Redis does not support nested hashmaps, "unembed" all nested dicts
            # {'a.b': 'c'} -> {'a': {'b': 'c'}}
            for key in (k for k in data.keys() if '.' in k):
                outer, inner = key.split('.')
                data.setdefault(outer, {})[inner] = data.pop(key)
            return data

    def keys(self):
        return self._connection.scan_iter()

    def set(self, key, data):
        if isinstance(data, dict):
            # Redis does not support nested hashmaps, "embed" all nested dicts
            # {'a': {'b': 'c'}} -> {'a.b': 'c'}
            for dk, val in list(data.items()):
                if isinstance(val, dict):
                    for k, v in data.pop(dk).items():
                        data['{}.{}'.format(dk, k)] = v
            self._connection.hmset(key, data)
        else:
            self._connection.set(key, data)

    def unset(self, key):
        self._connection.delete(key)

    def query(self, query):
        return filter(query.as_lambda(), self.values())

    def unset_all(self):
        self._connection.flushdb()
