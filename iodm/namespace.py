import uuid

import iodm
from iodm import exceptions
from iodm.auth import Permissions
from iodm.collection import Collection
from iodm.backends import MongoBackend
from iodm.backends import ElasticsearchBackend


class Namespace(Collection):

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
        return Collection.from_dict(self.read(name).data)

    def create_collection(self, name, user, logger='mongo', storage='mongo', state='elasticsearch', permissions=None, schema=None):
        uid = str(uuid.uuid4()).replace('-', '')

        collection_dict = {
            'uuid': uid,
            'schema': schema,
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
        }

        # Validate that our inputs can actually be deserialized to a collection
        collection = Collection.from_dict(collection_dict)

        self.create(name, collection_dict, user)

        return collection
