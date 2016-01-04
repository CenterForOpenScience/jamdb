import uuid
import asyncio
import logging
import datetime

import jwt
import aiohttp
import tornado.web
from stevedore import driver

from iodm.auth import User
from iodm.server.api.base import BaseAPIHandler


logger = logging.getLogger(__name__)


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
                'pid': user.id,
                'type': user.type,
                'provider': user.provider,
                'token': user.token.decode(),
                'refreshable': provider.refreshable,
            }
        }})
