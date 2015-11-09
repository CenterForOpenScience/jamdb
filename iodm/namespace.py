import uuid

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

    def __init__(self, uuid, name, storage, logger, state, permissions=None):
        self.uuid = uuid
        self.name = name
        super().__init__(
            iodm.Storage(self.MAPPING[storage['backend']](**storage['settings'])),
            iodm.Logger(self.MAPPING[logger['backend']](**logger['settings'])),
            iodm.State(self.MAPPING[state['backend']](**state['settings'])),
            permissions or {}
        )

    def get_collection(self, name):
        col = self.read(name).data

        return Collection(
            iodm.Storage(self.MAPPING[col['storage']['backend']](**col['storage']['settings'])),
            iodm.Logger(self.MAPPING[col['logger']['backend']](**col['logger']['settings'])),
            iodm.State(self.MAPPING[col['state']['backend']](**col['state']['settings'])),
            col['permissions']
        )

    def create_collection(self, name, user, permissions=None):
        uid = str(uuid.uuid4())
        self.create(name, {
            'uuid': uid,
            'permissions': {
                **(permissions or {}),
                user: Permissions.ADMIN
            },
            'logger': {
                'backend': 'mongo',
                'settings': {
                    'database': 'iodm',
                    'collection': '{}-{}-logger'.format(self.uuid, uid),
                }
            },
            'state': {
                'backend': 'mongo',
                'settings': {
                    'database': 'iodm',
                    'collection': '{}-{}-state'.format(self.uuid, uid),
                }
            },
            'storage': {
                'backend': 'mongo',
                'settings': {
                    'database': 'iodm',
                    'collection': '{}-{}-storage'.format(self.uuid, uid),
                }
            }
        }, user)
        return self.get_collection(name)

# {"state": ["mongo", "test", "state"], "storage": ["mongo", "test", "storage"], "logs": ["mongo", "test", "logs"]}
