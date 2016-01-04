__import__("pkg_resources").declare_namespace(__name__)

from iodm.backends.order import O
from iodm.backends.query import Q
from iodm.backends.git import GitBackend
# from iodm.backends.redis import RedisBackend
from iodm.backends.mongo import MongoBackend
from iodm.backends.ephemeral import EphemeralBackend
from iodm.backends.elasticsearch import ElasticsearchBackend


__all__ = (
    'Q',
    'O',
    'GitBackend',
    'MongoBackend',
    # 'RedisBackend',
    'EphemeralBackend',
    'ElasticsearchBackend'
)
