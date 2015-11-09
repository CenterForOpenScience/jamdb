from pymongo import MongoClient

from iodm import exceptions
from iodm.backends.base import Backend
from iodm.backends.util import QueryCommand
from iodm.backends.util import CompoundQuery


class MongoBackend(Backend):

    DEFAULT_CONNECTION = MongoClient()

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
        self._collection.update({'_id': key}, {**data, '_id': key}, upsert=True)

    def unset(self, key):
        self._collection.remove({'_id': key})

    def query(self, query, order=None, limit=None, skip=None):
        if order:
            order = [(order.key, order.order)]
        if query is None:
            query = {}
        else:
            if isinstance(query, CompoundQuery):
                query = {
                    '$and': [
                        {q.key: {'$' + q.comparator: q.value}}
                        for q in query.queries
                    ]
                }
            else:
                query = {query.key: {'$' + query.comparator: query.value}}
        return self._collection.find(query, sort=order, limit=limit or 0, skip=skip or 0)

    def count(self, query):
        if query is None:
            query = {}
        else:
            if isinstance(query, CompoundQuery):
                query = {
                    '$and': [
                        {q.key: {'$' + q.comparator: q.value}}
                        for q in query.queries
                    ]
                }
            else:
                query = {query.key: {'$' + query.comparator: query.value}}
        return self._collection.count(query)

    def unset_all(self):
        self._collection.remove()
