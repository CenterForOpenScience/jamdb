import uuid
import operator
from functools import reduce

import jsonpatch

import jam
from jam import settings
from jam import exceptions
from jam.auth import Permissions
from jam.namespace import Namespace
from jam.collection import Collection
from jam.backends.util import get_backend


class NamespaceManager(Collection):

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
            return Namespace(name=name, **self.read(name).data)
        except exceptions.NotFound:
            raise exceptions.NotFound(
                code='N404',
                title='Namespace not found',
                detail='Namespace "{}" was not found'.format(name)
            )

    def update(self, key, patch, user):
        if isinstance(patch, dict):
            keys = set(patch.keys())
            if not keys.issubset(Namespace.WHITELIST):
                raise exceptions.InvalidFields(keys - Namespace.WHITELIST)

            previous = self._state.get(key)
            patch = jsonpatch.JsonPatch.from_diff(previous.data, {**previous.data, **patch})
            patch = list(filter(lambda p: p['path'].split('/')[1] in Namespace.WHITELIST, patch))

        for blob in patch:
            if not blob['path'].split('/')[1] in Namespace.WHITELIST:
                raise exceptions.InvalidField(blob['path'])
            if blob.get('value') and blob['path'].startswith('/permissions'):
                try:
                    blob['value'] = Permissions(reduce(operator.or_, [Permissions[p.strip()] for p in blob['value'].split(',')], Permissions.NONE))
                except (AttributeError, KeyError):
                    raise exceptions.InvalidPermission(blob['value'])

        return super().update(key, patch, user)
