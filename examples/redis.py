from iodm import Logger
from iodm import Storage
from iodm import Snapshot
from iodm import Collection
from iodm.backends import RedisBackend
from iodm.backends import EphemeralBackend

if __name__ == '__main__':
    logger = Logger(RedisBackend())
    storage = Storage(RedisBackend(database=1))
    snapshot = Snapshot(EphemeralBackend())

    collection = Collection(storage, logger, snapshot, regenerate=False)

    collection.create('key', 'value')
    collection.create('value', {'keee': 'eeeeee'})
    collection.rename('value', 'otherkey')

    clone = Collection(storage, logger, Snapshot(EphemeralBackend()), regenerate=True)

    assert clone.read('key') == collection.read('key')
    assert clone.read('otherkey') == collection.read('otherkey')
