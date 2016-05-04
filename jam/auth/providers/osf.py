import aiohttp

from jam import settings
from jam import exceptions
from jam.auth.providers.base import BaseAuthProvider


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
