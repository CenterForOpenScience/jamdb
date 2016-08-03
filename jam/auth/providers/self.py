import asyncio

import bcrypt

from jam import exceptions
from jam import NamespaceManager
from jam.plugins.user import UserPlugin
from jam.auth.providers.base import BaseAuthProvider

manager = NamespaceManager()


class SelfAuthProvider(BaseAuthProvider):
    name = 'self'
    type = 'jam'

    PASSWORD_SCHEMA = {
        'id': 'password',
        'type': 'string',
        'pattern': '^\$2b\$1[0-3]\$\S{53}$'
    }

    async def _authenticate(self, data):
        namespace = manager.get_namespace(data['namespace'])
        collection = namespace.get_collection(data['collection'])

        if not UserPlugin.is_enabled(collection):
            raise exceptions.PluginNotEnabled(UserPlugin.NAME)

        if not (
            collection.schema
            and 'password' in collection.schema._schema.get('required', [])
            and collection.schema._schema['properties']['password'] == self.PASSWORD_SCHEMA
        ):
            raise exceptions.BadRequest(title='Bad password schema', detail='The schema for password must be {} and must be a required field'.format(self.PASSWORD_SCHEMA))

        # TODO validate retrieved document
        doc = collection.read(data['username'])
        password = doc.data['password'].encode()

        hashed = await asyncio.get_event_loop().run_in_executor(None, lambda: bcrypt.hashpw(data['password'].encode(), password))

        if hashed == password:
            return SelfAuthProvider.type, '{}:{}'.format(namespace.ref, collection.ref), data['username'], 8
        raise exceptions.Unauthorized()
