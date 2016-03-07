import jam
from jam.base import BaseCollection
from jam.auth import PERMISSIONS_SCHEMA
from jam.backends.util import load_backend
from jam.backends.util import BACKEND_SCHEMA


class Collection(BaseCollection):

    WHITELIST = {'permissions', 'schema', 'flags'}

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
            'flags': {
                'oneOf': [
                    {'type': 'null'},
                    {
                        'type': 'object',
                        'patternProperties': {
                            '.+': {'type': 'boolean'}
                        }
                    }
                ]
            },
            'schema': {
                'oneOf': [
                    {'type': 'null'},
                    {
                        'type': 'object',
                        'properties': {
                            'schema': {},
                            'type': {'type': 'string'}
                        },
                        'required': ['type', 'schema']
                    }
                ]
            }
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
    def ref(self):
        return self._document.ref

    @property
    def flags(self):
        return self._document.data['flags']

    @property
    def document(self):
        return self._document

    def __init__(self, document):
        self._document = document

        logger = document.data['storage']
        state = document.data['state']
        storage = document.data['storage']

        super().__init__(
            jam.Storage(load_backend(storage['backend'], **storage['settings'])),
            jam.Logger(load_backend(logger['backend'], **logger['settings'])),
            jam.State(load_backend(state['backend'], **state['settings'])),
            permissions=document.data['permissions'],
            schema=document.data.get('schema')
        )
