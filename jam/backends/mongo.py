from pymongo import MongoClient

from jam import settings
from jam import exceptions
from jam.backends import query as queries
from jam.backends.base import Backend
from jam.backends.util import QueryCommand


def sanitize(data):
    def keys(dict_obj):
        for key, value in dict_obj.items():
            yield key
            if not isinstance(value, (tuple, list)):
                value = [value]
            for sub in value:
                if isinstance(sub, dict):
                    yield from keys(sub)
    for key in keys(data):
        if '.' in key or key.startswith('$'):
            raise exceptions.MalformedData()


class MongoBackend(Backend):

    DEFAULT_CONNECTION = MongoClient(settings.MONGO_URI)

    @classmethod
    def settings_for(cls, namespace_id, collection_id, type_):
        return {
            'database': settings.MONGO_DATABASE_NAME,
            'collection': '{}-{}-{}'.format(type_, namespace_id, collection_id),
        }

    def __init__(self, database, collection, connection=None):
        self._connection = connection or MongoBackend.DEFAULT_CONNECTION
        self._database = self._connection[database]
        self._collection = self._database[collection]

    def get(self, key):
        ret = self._collection.find_one({'_id': key})
        if ret is None:
            raise exceptions.NotFound(key)
        return ret

    def keys(self):
        return (x['_id'] for x in self._collection.find(projection=['_id']))

    def list(self, order=None):
        if order:
            order = [(order.key, order.order)]
        return self._collection.find(sort=order)

    def set(self, key, data):
        data = {**data, '_id': key}
        sanitize(data)
        self._collection.update({'_id': key}, data, upsert=True)

    def unset(self, key):
        self._collection.remove({'_id': key})

    def query(self, query, order=None, limit=None, skip=None):
        if order:
            order = [(order.key, order.order)]
        if query is None:
            query = {}
        else:
            query = self._translate_query(query)

        return self._collection.find(query, sort=order, limit=limit or 0, skip=skip or 0)

    def count(self, query):
        if query is None:
            query = {}
        else:
            query = self._translate_query(query)

        return self._collection.count(query)

    def unset_all(self):
        self._collection.remove()

    def _translate_query(self, query):
        if isinstance(query, queries.CompoundQuery):
            return {{
                queries.Or: '$or',
                queries.And: '$and'
            }[query.__class__]: [
                self._translate_query(q)
                for q in query.queries
            ]}

        return {
            query.key: {{
                queries.In: '$in',
                queries.Equal: '$eq',
                queries.NotEqual: '$ne',
            }[query.__class__]: query.value}
        }
