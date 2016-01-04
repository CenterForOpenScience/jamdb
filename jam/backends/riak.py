from riak import RiakClient

from jam import exceptions
from jam.backends.base import Backend
from jam.backends.util import CompoundQuery


class RiakBackend(Backend):

    DEFAULT_CONNECTION = RiakClient()

    def __init__(self, bucket_type, bucket_name, connection=None):
        self._connection = connection or RiakBackend.DEFAULT_CONNECTION
        self._bucket_type = self._connection.bucket_type(bucket_type)
        self._bucket = self._bucket_type.bucket(bucket_name)

    def get(self, key):
        return self._bucket.get(key)

    def keys(self):
        stream = self._bucket.stream_keys()
        for key in stream:
            yield key
        stream.close()

    def list(self, order=None):
        if order:
            order = [(order.key, order.order)]
        return self._collection.find(sort=order)

    def set(self, key, data):
        self._bucket.new(key, encoded_data=data)

    def unset(self, key):
        self._bucket.delete(key)

    def query(self, query, order=None):
        if order:
            order = [(order.key, order.order)]
        return self._bucket.search(query)

    def unset_all(self):
        self._collection.remove()
