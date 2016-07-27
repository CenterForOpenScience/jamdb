import aiohttp
import functools

from jam import settings
from jam import exceptions
from jam import NamespaceManager
from jam.plugins.grant import GrantPlugin
from jam.auth.permissions import Permissions
from jam.auth.providers.base import BaseAuthProvider


manager = NamespaceManager()


PERMISSION_MAP = {
    'read': Permissions.READ,
    'write': Permissions.CRUD,
    'admin': Permissions.ADMIN,
}


class OSFAuthProvider(BaseAuthProvider):
    name = 'osf'
    type = 'user'

    async def _authenticate(self, data):
        async with aiohttp.request('GET', '{}/oauth2/profile'.format(settings.OSF['ACCOUNTS_URL']), headers={
            'Authorization': 'Bearer {}'.format(data.get('access_token'))
        }) as resp:
            if resp.status != 200:
                raise exceptions.Unauthorized()
            return 'user', 'osf', (await resp.json())['id']


# TODO Fuzz test me
class OSFGrantAuthProvider(BaseAuthProvider):
    name = 'osf'
    type = 'grant'

    async def _authenticate(self, data):
        namespace = manager.get_namespace(data['namespace'])
        collection = namespace.get_collection(data['collection'])

        if not GrantPlugin.is_enabled(collection):
            raise exceptions.PluginNotEnabled(GrantPlugin.NAME)

        if data.get('document'):
            if not collection.plugin('grant').document_enabled:
                raise exceptions.BadRequest(detail='document permissions must be provided via collection.plugins.grant.document')
            resource = data['document']
        else:
            if not collection.plugin('grant').collection_enabled:
                raise exceptions.BadRequest(detail='collection permissions must be provided via collection.plugins.grant.collection')
            resource = data['collection']

        async with aiohttp.request('GET', '{}/oauth2/profile'.format(settings.OSF['ACCOUNTS_URL']), headers={
            'Authorization': 'Bearer {}'.format(data.get('access_token'))
        }) as resp:
            if resp.status != 200:
                raise exceptions.Unauthorized()
            user_id = (await resp.json())['id']

        async with aiohttp.request('GET', '{}/v2/nodes/{}/'.format(settings.OSF['API_URL'], resource), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(data['access_token']),
        }) as resp:
            if resp.status != 200:
                raise exceptions.Unauthorized()

            ref = '{namespace}.{collection}'.format(**data)
            granted = Permissions.from_string(data['permissions']) & functools.reduce(
                lambda acc, x: acc | PERMISSION_MAP.get(x, Permissions.NONE),
                (await resp.json())['data']['attributes']['current_user_permissions'],
                Permissions.NONE
            )

            if data.get('document'):
                ref += '.' + data['document']
                granted &= collection.plugin('grant').document_permissions
            else:
                granted &= collection.plugin('grant').collection_permissions

            return 'user', 'osf', user_id, .06, False, {ref: granted}
