import iodm
from iodm import exceptions
from iodm.auth import Permissions
from iodm.collection import Collection
from iodm.backends import MongoBackend
from iodm.backends import ElasticsearchBackend


class Namespace(Collection):
    MAPPING = {
        'mongo': MongoBackend,
        'elasticsearch': ElasticsearchBackend
    }

    # permissions = {'*': Permissions.ADMIN}

    def __init__(self, name):
        self.name = name
        super().__init__(
            iodm.Storage(MongoBackend('iodm-namespace', name + '-storage')),
            iodm.Logger(MongoBackend('iodm-namespace', name + '-logs')),
            iodm.State(MongoBackend('iodm-namespace', name + '-state')),
        )
        try:
            self.permissions = self.read('permissions').data
        except exceptions.NotFound:
            self.permissions = {}

    def get_collection(self, name):
        col = self.read(name).data
        col_dict = col['settings']
        return Collection(
            iodm.Storage(self.MAPPING[col_dict['storage'][0]](*col_dict['storage'][1:])),
            iodm.Logger(self.MAPPING[col_dict['logs'][0]](*col_dict['logs'][1:])),
            iodm.State(self.MAPPING[col_dict['state'][0]](*col_dict['state'][1:])),
            permissions=col['permissions']
        )

    def create_collection(self, name, settings, user, permissions=None):
        self.create(name, {
            'name': name,
            'settings': settings,
            'permissions': permissions or {}
        }, user)

# {"state": ["mongo", "test", "state"], "storage": ["mongo", "test", "storage"], "logs": ["mongo", "test", "logs"]}
