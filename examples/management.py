from jam import Logger
from jam import Storage
from jam import Snapshot
from jam import Collection
from jam.backends import GitBackend
from jam.backends import RedisBackend
from jam.backends import EphemeralBackend


class Manager:
    MAPPING = {
        'git': GitBackend,
        'redis': RedisBackend,
        'ephemeral': EphemeralBackend,
    }

    def __init__(self):
        self.backend = EphemeralBackend()

    def get_collection(self, name):
        col_dict = self.backend.get(name)
        return Collection(
            Storage(self.MAPPING[col_dict['storage'][0]](*col_dict['storage'][1:])),
            Logger(self.MAPPING[col_dict['logs'][0]](*col_dict['logs'][1:])),
            Snapshot(self.MAPPING[col_dict['snapshot'][0]](*col_dict['snapshot'][1:])),
        )

    def create_collection(self, name, settings):
        self.backend.set(name, settings)


if __name__ == '__main__':
    gary = Manager()
    gary.create_collection('User1', {
        'logs': ('git', 'data/logs'),
        'storage': ('redis', ),
        'snapshot': ('ephemeral', ),
    })
    gary.create_collection('User2', {
        'logs': ('ephemeral', ),
        'storage': ('ephemeral', ),
        'snapshot': ('ephemeral', ),
    })

    collection = gary.get_collection('User1')

    collection.create('foo', 'bar')
    collection.create('bar', {'testing': 'all day'})

    collection2 = gary.get_collection('User2')

    collection2.create('data', 'are')
    collection2.create('key', ['Some', 'Datas', 'here'])

    assert collection2.read('key').data[1] == 'Datas'

    # Clean up
    gary.get_collection('User1')._logger._backend.unset_all()
