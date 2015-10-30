from iodm import Logger
from iodm import Storage
from iodm import Snapshot
from iodm import Collection
from iodm.backends import GitBackend
from iodm.backends import EphemeralBackend


class GitSnapshot(Snapshot):
    def __init__(self):
        super().__init__(GitBackend())


if __name__ == '__main__':
    logger = Logger(GitBackend('data/logs'))
    storage = Storage(GitBackend('data/storage'))
    snapshot = Snapshot(GitBackend('data/snapshot'))

    collection = Collection(storage, logger, snapshot, regenerate=False)

    collection.create('key', 'value')
    collection.create('value', {'keee': 'eeeeee'})
    collection.rename('value', 'otherkey')

    clone = Collection(storage, logger, Snapshot(EphemeralBackend()), regenerate=True)

    assert clone.read('key') == collection.read('key')
    assert clone.read('otherkey') == collection.read('otherkey')

    hist = list(collection.history('value'))

    # Clean up
    logger._backend.unset_all()
    storage.unset_all()
    snapshot._backend.unset_all()
