import uuid
import asyncio
import datetime

import jwt
import aiohttp
import tornado.web
from stevedore import driver

from iodm.auth import User
from iodm.server.api.base import BaseAPIHandler


class AuthHandler(BaseAPIHandler):

    def prepare(self):
        self.user = User(self.get_cookie('cookie'), verify=False)

    async def post(self):
        data = self.json['data']
        assert data.get('type') == 'users', "'type' must be 'users', not {}".format(data.get('type', 'null'))

        provider = driver.DriverManager(
            namespace='iodm.auth.providers',
            name=data['attributes'].pop('provider'),
            invoke_on_load=True,
        ).driver

        user = await provider.authenticate(self.user, data['attributes'])

        self.write({'data': {
            'id': user.uid,
            'type': 'users',
            'attributes': {
                'token': user.token.decode(),
                'refreshable': provider.refreshable,
            }
        }})
