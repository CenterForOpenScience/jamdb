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
                'backend': logger,
                'settings': self.MAPPING[logger].settings_for(self.uuid, uid, 'logger')
            },
            'state': {
                'backend': state,
                'settings': self.MAPPING[state].settings_for(self.uuid, uid, 'state')
            },
            'storage': {
                'backend': storage,
                'settings': self.MAPPING[storage].settings_for(self.uuid, uid, 'storage')
            }
        }, user)

        return self.get_namespace(name)

    def get_namespace(self, name):
        return Namespace(name=name, **self.read(name).data)
