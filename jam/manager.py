import uuid

import jam
from jam import settings
from jam import exceptions
from jam.auth import Permissions
from jam.base import BaseCollection
from jam.namespace import Namespace
from jam.backends.util import get_backend


class NamespaceManager(BaseCollection):

    def __init__(self, name=None):
        self.uuid = self.name = name or 'jam'
        storage_backend = get_backend(settings.NAMESPACEMANAGER_BACKENDS['storage'])
        logger_backend = get_backend(settings.NAMESPACEMANAGER_BACKENDS['logger'])
        state_backend = get_backend(settings.NAMESPACEMANAGER_BACKENDS['state'])

        super().__init__(
            jam.Storage(storage_backend(**storage_backend.settings_for('manager', self.uuid, 'storage'))),
            jam.Logger(logger_backend(**logger_backend.settings_for('manager', self.uuid, 'logger'))),
            jam.State(state_backend(**state_backend.settings_for('manager', self.uuid, 'state'))),
            schema={'type': 'jsonschema', 'schema': Namespace.SCHEMA}
        )

    def create_namespace(self, name, user, permissions=None):
        uid = str(uuid.uuid4()).replace('-', '')
        try:
            self.create(name, {
                'uuid': uid,
                'permissions': {**(permissions or {}), user: Permissions.ADMIN},
                'logger': {
                    'backend': settings.NAMESPACE_BACKENDS['logger'],
                    'settings': get_backend(settings.NAMESPACE_BACKENDS['logger']).settings_for(self.uuid, uid, 'logger')
                },
                'state': {
                    'backend': settings.NAMESPACE_BACKENDS['state'],
                    'settings': get_backend(settings.NAMESPACE_BACKENDS['state']).settings_for(self.uuid, uid, 'state')
                },
                'storage': {
                    'backend': settings.NAMESPACE_BACKENDS['storage'],
                    'settings': get_backend(settings.NAMESPACE_BACKENDS['storage']).settings_for(self.uuid, uid, 'storage')
                }
            }, user)
        except exceptions.KeyExists:
            raise exceptions.KeyExists(
                code='N409',
                title='Namespace already exists',
                detail='Namespace "{}" already exists'.format(name)
            )

        return self.get_namespace(name)

    def get_namespace(self, name):
        try:
            return Namespace(self.read(name))
        except exceptions.NotFound:
            raise exceptions.NotFound(
                code='N404',
                title='Namespace not found',
                detail='Namespace "{}" was not found'.format(name)
            )

    def _generate_patch(self, previous, new):
        keys = set(new.keys())
        if not keys.issubset(Namespace.WHITELIST):
            raise exceptions.InvalidFields(keys - Namespace.WHITELIST)

        patch = super()._generate_patch(previous, new)
        # Remove any extranious keys added or deleted by diffing
        return list(filter(lambda p: p['path'].split('/')[1] in Namespace.WHITELIST, patch))

    def _validate_patch(self, patch):
        for blob in patch:
            if not blob['path'].split('/')[1] in Namespace.WHITELIST:
                raise exceptions.InvalidField(blob['path'])
            if blob.get('value') and blob['path'].startswith('/permissions'):
                blob['value'] = Permissions.from_string(blob['value'])
        return patch
