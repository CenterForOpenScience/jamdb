import logging

import jwt

from stevedore import driver

from jam.auth import User
from jam import exceptions
from jam.server.api.jsonapi import JSONAPIHandler


logger = logging.getLogger(__name__)


class AuthHandler(JSONAPIHandler):

    def get_current_user(self):
        try:
            return User(
                self.request.headers.get('Authorization') or
                self.get_query_argument('token', default=None),
                verify=False
            )
        except jwt.InvalidTokenError:
            return User(None)

    def prepare(self):
        self.user = User(self.get_cookie('cookie'), verify=False)

    async def post(self):
        try:
            data = self.json['data']
        except (TypeError, ValueError, KeyError):
            raise exceptions.MalformedData()

        if data.get('type') != 'users':
            raise exceptions.IncorrectParameter('data.type', 'users', data.get('type', 'null'))

        provider = driver.DriverManager(
            namespace='jam.auth.providers',
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
