import uuid

import iodm
from iodm import exceptions
from iodm.auth import Permissions
from iodm.collection import Collection
from iodm.backends.util import load_backend


class Namespace(Collection):

    def __init__(self, uuid, name, storage, logger, state, permissions=None):
        self.uuid = uuid
        self.name = name
        super().__init__(
            iodm.Storage(load_backend(storage['backend'], **storage['settings'])),
            iodm.Logger(load_backend(logger['backend'], **logger['settings'])),
            iodm.State(load_backend(state['backend'], **state['settings'])),
            permissions=permissions
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
                'settings': get_backend(logger).settings_for(self.uuid, uid, 'logger')
            },
            'state': {
                'backend': state,
                'settings': get_backend(state).settings_for(self.uuid, uid, 'state')
            },
            'storage': {
                'backend': storage,
                'settings': get_backend(storage).settings_for(self.uuid, uid, 'storage')
            }
        }

        # Validate that our inputs can actually be deserialized to a collection
        collection = Collection.from_dict(collection_dict)

        self.create(name, collection_dict, user)

        return collection
