import uuid
import asyncio
import datetime

import jwt
import aiohttp
import tornado.web

from iodm.auth import User
from iodm.server.api.base import BaseAPIHandler


class AuthHandler(BaseAPIHandler):

    def prepare(self):
        self.user = User(self.get_cookie('cookie'), verify=False)

    async def _osf(self, data):
        resp = await aiohttp.request('GET', 'https://staging-accounts.osf.io/oauth2/profile', headers={
            'Authorization': 'Bearer {}'.format(data['access_token'])
        })

        assert resp.status == 200
        return 'user', 'osf', (await resp.json())['id']

    async def _anon(self, data):
        # Allow users to reauthenticate as anon and keep the same id
        if self.user.type == 'anon' and self.user.provider is None:
            return 'anon', '', self.user.id
        return 'anon', '', str(uuid.uuid4()).replace('-', '')

    async def post(self):
        data = self.json['data']
        assert data.get('type') == 'users', "'type' must be 'users', not {}".format(data.get('type', 'null'))

        provider = data['attributes'].pop('provider', None)
        fetch_auth = getattr(self, '_' + provider, None)
        assert fetch_auth is not None

        uid = '-'.join(await fetch_auth(data['attributes']))

        signed_jwt = jwt.encode({
            'sub': uid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }, 'TestKey')

        self.write({
            'id': uid,
            'type': 'users',
            'attributes': {
                'token': signed_jwt.decode()
            }
        })
