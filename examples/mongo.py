from jam import Logger
from jam import Storage
from jam import Snapshot
from jam import Collection
from jam.backends import MongoBackend
from jam.backends import EphemeralBackend

if __name__ == '__main__':
    logger = Logger(MongoBackend('jamtest', 'logs'))
    storage = Storage(MongoBackend('jamtest', 'storage'))
    snapshot = Snapshot(EphemeralBackend())

    collection = Collection(storage, logger, snapshot, regenerate=False)

    collection.create('key', 'value')
    collection.create('value', {'keee': 'eeeeee'})
    collection.rename('value', 'otherkey')

    clone = Collection(storage, logger, Snapshot(EphemeralBackend()), regenerate=True)

    assert clone.read('key') == collection.read('key')
    assert clone.read('otherkey') == collection.read('otherkey')
