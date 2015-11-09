import uuid

import iodm
from iodm import exceptions
from iodm.auth import Permissions
from iodm.collection import Collection
from iodm.namespace import Namespace
from iodm.backends import MongoBackend


class NamespaceManager(Collection):

    def __init__(self, name=None):
        self.name = name = name or 'iodm'
        super().__init__(
            iodm.Storage(MongoBackend('iodm-namespace', name + '-manager-storage')),
            iodm.Logger(MongoBackend('iodm-namespace', name + '-manager-logs')),
            iodm.State(MongoBackend('iodm-namespace', name + '-manger-state')),
        )

    def create_namespace(self, name, user, permissions=None):
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
                    'collection': '{}-logger'.format(uid),
                }
            },
            'state': {
                'backend': 'mongo',
                'settings': {
                    'database': 'iodm',
                    'collection': '{}-state'.format(uid),
                }
            },
            'storage': {
                'backend': 'mongo',
                'settings': {
                    'database': 'iodm',
                    'collection': '{}-storage'.format(uid),
                }
            }
        }, user)

        return self.get_namespace(name)

    def get_namespace(self, name):
        return Namespace(name=name, **self.read(name).data)
