__import__("pkg_resources").declare_namespace(__name__)

from iodm.backends.util import Order
from iodm.backends.util import Query
from iodm.backends.git import GitBackend
from iodm.backends.redis import RedisBackend
from iodm.backends.mongo import MongoBackend
from iodm.backends.ephemeral import EphemeralBackend
from iodm.backends.elasticsearch import ElasticsearchBackend


Q, O = Query, Order


__all__ = (
    'Q', 'Query',
    'O', 'Order',
    'GitBackend',
    'MongoBackend',
    'RedisBackend',
    'EphemeralBackend',
    'ElasticsearchBackend'
)
