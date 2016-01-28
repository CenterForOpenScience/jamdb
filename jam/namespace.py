import uuid

import jam
from jam import settings
from jam import exceptions
from jam.auth import Permissions
from jam.collection import Collection
from jam.auth import PERMISSIONS_SCHEMA
from jam.backends.util import get_backend
from jam.backends.util import load_backend
from jam.backends.util import BACKEND_SCHEMA


class Namespace(Collection):

    WHITELIST = {'permissions'}

    SCHEMA = {
        'type': 'object',
        'properties': {
            'permissions': PERMISSIONS_SCHEMA,
            'uuid': {
                'type': 'string',
                'pattern': '^[a-fA-F0-9]{32}$'
            },
            'logger': BACKEND_SCHEMA,
            'state': BACKEND_SCHEMA,
            'storage': BACKEND_SCHEMA,
        },
        'additionalProperties': False,
        'required': [
            'logger',
            'permissions',
            'state',
            'storage',
            'uuid'
        ]
    }

    WHITELIST = {'permissions'}

    def __init__(self, uuid, name, storage, logger, state, permissions=None):
        self.uuid = uuid
        self.name = name
        super().__init__(
            jam.Storage(load_backend(storage['backend'], **storage['settings'])),
            jam.Logger(load_backend(logger['backend'], **logger['settings'])),
            jam.State(load_backend(state['backend'], **state['settings'])),
            permissions=permissions
        )

    def get_collection(self, name):
        try:
            col = Collection.from_dict(self.read(name).data)
            col.name = name  # TODO Fix me, this just makes life much easier
            return col
        except exceptions.NotFound:
            raise exceptions.NotFound(
                code='C404',
                title='Collection not found',
                detail='Collection "{}" was not found in namespace "{}"'.format(name, self.name)
            )

    def create_collection(self, name, user, logger=None, storage=None, state=None, permissions=None, schema=None):
        uid = str(uuid.uuid4()).replace('-', '')
        state = state or settings.COLLECTION_BACKENDS['state']
        logger = logger or settings.COLLECTION_BACKENDS['logger']
        storage = storage or settings.COLLECTION_BACKENDS['storage']

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

        try:
            self.create(name, collection_dict, user)
        except exceptions.KeyExists:
            raise exceptions.KeyExists(
                code='C409',
                title='Collection already exists',
                detail='Collection "{}" already exists in namespace "{}"'.format(name, self.name)
            )

        return collection
