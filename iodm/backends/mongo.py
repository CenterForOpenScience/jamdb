from pymongo import MongoClient

from iodm.backends.base import Backend


class MongoBackend(Backend):

    def __init__(self, database, collection, connection=None):
        self._connection = connection or MongoClient()
        self._database = self._connection[database]
        self._collection = self._database[collection]

    def get(self, key):
        return self._collection.find_one({'_id': key})

    def keys(self):
        return (x['_id'] for x in self._collection.find(projection=['_id']))

    def list(self, order=None):
        if order:
            order = [(order.key, order.order)]
        return self._collection.find(sort=order)

    def set(self, key, data):
        self._collection.insert({**data, '_id': key})

    def unset(self, key):
        self._collection.remove({'_id': key})

    def query(self, query):
        return self._collection.find(query)

    def unset_all(self):
        self._collection.remove()
