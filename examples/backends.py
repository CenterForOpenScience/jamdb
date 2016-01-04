from jam import Logger
from jam import Storage
from jam import Snapshot
from jam import Collection
from jam.backends import RedisBackend
from jam.backends import EphemeralBackend


class EphemeralSnapshot(Snapshot):
    def __init__(self):
        super().__init__(EphemeralBackend())


if __name__ == '__main__':
    elogger = Logger(EphemeralBackend())
    estorage = Storage(RedisBackend(database=2))
    esnapshot = Snapshot(EphemeralBackend())
    rsnapshot = Snapshot(RedisBackend(database=3))

    ecollection = Collection(estorage, elogger, esnapshot, regenerate=False)

    ecollection.create('key', 'value')
    ecollection.create('value', {'keee': 'eeeeee'})
    ecollection.rename('value', 'otherkey')

    clone = Collection(estorage, elogger, rsnapshot, regenerate=True)

    assert clone.read('key') == ecollection.read('key')
    assert clone.read('otherkey') == ecollection.read('otherkey')
    assert list(clone.history('value')) == list(ecollection.history('value'))
