from iodm.backends.util import Order
from iodm.backends.util import Query
from iodm.backends.redis import RedisBackend
from iodm.backends.ephemeral import EphemeralBackend


Q, O = Query, Order


__all__ = (
    'Q', 'Query',
    'O', 'Order',
    'RedisBackend',
    'EphemeralBackend',
)
