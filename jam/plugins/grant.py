from jam.auth import Permissions
from jam.plugins.base import Plugin


class GrantPlugin(Plugin):
    NAME = 'grant'
    EXPLICIT = True
    SCHEMA = {
        'type': 'object',
        'properties': {
            'document': {'type': 'string'},
            'collection': {'type': 'string'},
        },
        'additionalProperties': False,
    }

    @property
    def document_permissions(self):
        return Permissions.from_string(self._raw.get('document', ''))

    @property
    def collection_permissions(self):
        return Permissions.from_string(self._raw.get('collection', ''))

    @property
    def document_enabled(self):
        return bool(self._raw.get('document'))

    @property
    def collection_enabled(self):
        return bool(self._raw.get('collection'))

    def get_permissions(self, request):
        return Permissions.NONE
