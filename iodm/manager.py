import uuid

import iodm
from iodm import exceptions
from iodm.auth import Permissions
from iodm.collection import Collection
from iodm.namespace import Namespace
from iodm.backends import MongoBackend


class NamespaceManager(Collection):

    def __init__(self, name=None, uuid=None):
        self.name = name = name or 'iodm'
        self.uuid = uuid or 'namespace'
        super().__init__(
            iodm.Storage(MongoBackend('iodm', 'storage-manager-' + name)),
            iodm.Logger(MongoBackend('iodm', 'logger-manager-' + name)),
            iodm.State(MongoBackend('iodm', 'state-manager-' + name)),
        )

    def create_namespace(self, name, user, permissions=None):
        uid = str(uuid.uuid4()).replace('-', '')
        self.create(name, {
            'uuid': uid,
            'permissions': {
                **(permissions or {}),
                user: Permissions.ADMIN
            },
            'logger': {
                'backend': 'mongo',
                'settings': self.MAPPING['mongo'].settings_for(self.uuid, uid, 'logger')
            },
            'state': {
                'backend': 'mongo',
                'settings': self.MAPPING['mongo'].settings_for(self.uuid, uid, 'state')
            },
            'storage': {
                'backend': 'mongo',
                'settings': self.MAPPING['mongo'].settings_for(self.uuid, uid, 'storage')
            }
        }, user)

        return self.get_namespace(name)

    def get_namespace(self, name):
        return Namespace(name=name, **self.read(name).data)
