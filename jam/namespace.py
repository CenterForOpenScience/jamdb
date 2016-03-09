import uuid
import operator
from functools import reduce

import jsonpatch

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
        self.ref = name
        self.name = name
        super().__init__(
            jam.Storage(load_backend(storage['backend'], **storage['settings'])),
            jam.Logger(load_backend(logger['backend'], **logger['settings'])),
            jam.State(load_backend(state['backend'], **state['settings'])),
            permissions=permissions,
            schema={'type': 'jsonschema', 'schema': Collection.SCHEMA}
        )

    def get_collection(self, name):
        try:
            col = Collection.from_dict(self.read(name).data)
            col.ref = name  # TODO Fix me, this just makes life much easier
            col.name = name
            return col
        except exceptions.NotFound:
            raise exceptions.NotFound(
                code='C404',
                title='Collection not found',
                detail='Collection "{}" was not found in namespace "{}"'.format(name, self.name)
            )

    def create_collection(self, name, user, logger=None, storage=None, state=None, permissions=None, schema=None, flags=None):
        uid = str(uuid.uuid4()).replace('-', '')
        state = state or settings.COLLECTION_BACKENDS['state']
        logger = logger or settings.COLLECTION_BACKENDS['logger']
        storage = storage or settings.COLLECTION_BACKENDS['storage']

        if isinstance(permissions or {}, dict):
            try:
                permissions = {
                    key: Permissions(reduce(operator.or_, [Permissions[p.strip()] for p in value.split(',')], Permissions.NONE))
                    for key, value in (permissions or {}).items()
                }
                permissions = {**(permissions or {}), user: Permissions.ADMIN}
            except KeyError as e:
                raise exceptions.InvalidPermission(e.args[0])
            except AttributeError:
                pass  # Schema validation will catch issues

        collection_dict = {
            'uuid': uid,
            'flags': flags or {},
            'schema': schema,
            'permissions': permissions,
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

    def update(self, key, patch, user):
        if isinstance(patch, dict):
            keys = set(patch.keys())
            if not keys.issubset(Collection.WHITELIST):
                raise exceptions.InvalidFields(keys - Collection.WHITELIST)

            previous = self._state.get(key)
            patch = jsonpatch.JsonPatch.from_diff(previous.data, {**previous.data, **patch})
            patch = list(filter(lambda p: p['path'].split('/')[1] in Collection.WHITELIST, patch))

        for blob in patch:
            if not blob['path'].split('/')[1] in Collection.WHITELIST:
                raise exceptions.InvalidField(blob['path'])
            if blob.get('value') and not isinstance(blob.get('value'), Permissions) and blob['path'].startswith('/permissions'):
                try:
                    blob['value'] = Permissions(reduce(operator.or_, [Permissions[p.strip()] for p in blob['value'].split(',')], Permissions.NONE))
                except (AttributeError, KeyError):
                    raise exceptions.InvalidPermission(blob['value'])

        return super().update(key, patch, user)
