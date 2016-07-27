import uuid

import jam
from jam import settings
from jam import exceptions
from jam.models import Document
from jam.auth import Permissions
from jam.base import BaseCollection
from jam.collection import Collection
from jam.auth import PERMISSIONS_SCHEMA
from jam.backends.util import get_backend
from jam.backends.util import load_backend
from jam.backends.util import BACKEND_SCHEMA


class Namespace(BaseCollection):

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

    @property
    def document(self):
        return self._document

    @property
    def ref(self):
        return self._document.ref

    @property
    def uuid(self):
        return self._document.data['uuid']

    def __init__(self, document):
        self._document = document

        state = document.data['state']
        logger = document.data['logger']
        storage = document.data['storage']

        super().__init__(
            jam.Storage(load_backend(storage['backend'], **storage['settings'])),
            jam.Logger(load_backend(logger['backend'], **logger['settings'])),
            jam.State(load_backend(state['backend'], **state['settings'])),
            permissions=document.data['permissions'],
            schema={'type': 'jsonschema', 'schema': Collection.SCHEMA}
        )

    def get_collection(self, name):
        try:
            return Collection(self.read(name))
        except exceptions.NotFound:
            raise exceptions.NotFound(
                code='C404',
                title='Collection not found',
                detail='Collection "{}" was not found in namespace "{}"'.format(name, self.ref)
            )

    def create_collection(self, name, user, logger=None, storage=None, state=None, permissions=None, schema=None, plugins=None, **kwargs):
        if kwargs:
            raise exceptions.InvalidFields(kwargs.keys())

        uid = str(uuid.uuid4()).replace('-', '')
        state = state or settings.COLLECTION_BACKENDS['state']
        logger = logger or settings.COLLECTION_BACKENDS['logger']
        storage = storage or settings.COLLECTION_BACKENDS['storage']

        if isinstance(permissions or {}, dict):
            try:
                permissions = {
                    key: Permissions.from_string(value)
                    for key, value in (permissions or {}).items()
                }
                permissions[user] = Permissions.ADMIN
            except KeyError as e:
                raise exceptions.InvalidPermission(e.args[0])
            except AttributeError:
                pass  # Schema validation will catch issues

        collection_dict = {
            'uuid': uid,
            'plugins': plugins or {},
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
        Collection(Document(
            ref=name,
            log_ref=None,
            data_ref=None,
            created_on=0,
            created_by='',
            modified_on=0,
            modified_by='',
            data=collection_dict,
        ))

        try:
            return Collection(self.create(name, collection_dict, user))
        except exceptions.KeyExists:
            raise exceptions.KeyExists(
                code='C409',
                title='Collection already exists',
                detail='Collection "{}" already exists in namespace "{}"'.format(name, self.ref)
            )

    def _generate_patch(self, previous, new):
        keys = set(new.keys())
        if not keys.issubset(Collection.WHITELIST):
            raise exceptions.InvalidFields(keys - Collection.WHITELIST)

        patch = super()._generate_patch(previous, new)
        # Remove any extranious keys added or deleted by diffing
        return list(filter(lambda p: p['path'].split('/')[1] in Collection.WHITELIST, patch))

    def _validate_patch(self, patch):
        for blob in patch:
            if not blob['path'].split('/')[1] in Collection.WHITELIST:
                raise exceptions.InvalidField(blob['path'])
            if blob.get('value') and blob['path'].startswith('/permissions'):
                blob['value'] = Permissions.from_string(blob['value'])
        return patch
