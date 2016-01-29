import logging

import jwt

from stevedore import driver

from raven.contrib.tornado import SentryMixin

from jam.auth import User
from jam import exceptions
from jam.server.api.jsonapi import JSONAPIHandler


logger = logging.getLogger(__name__)


class AuthHandler(SentryMixin, JSONAPIHandler):

    def get_current_user(self):
        try:
            return User(
                self.request.headers.get('Authorization') or
                self.get_query_argument('token', default=None),
                verify=False
            )
        except jwt.InvalidTokenError:
            return User(None)

    async def post(self):
        try:
            data = self.json['data']
        except (TypeError, ValueError, KeyError):
            raise exceptions.MalformedData()

        if data.get('type') != 'users':
            raise exceptions.IncorrectParameter('data.type', 'users', data.get('type', 'null'))

        if not isinstance(data.get('attributes'), dict):
            raise exceptions.InvalidType('data.attributes', 'dict', type(data.get('type')))

        try:
            provider = driver.DriverManager(
                namespace='jam.auth.providers',
                name=data['attributes'].pop('provider'),
                invoke_on_load=True,
            ).driver
        except (KeyError, driver.NoMatches):
            raise exceptions.BadRequest(detail='Unknown provider')

        user = await provider.authenticate(self.current_user, data['attributes'])

        self.write({'data': {
            'id': user.uid,
            'type': 'users',
            'attributes': {
                'id': user.id,
                'type': user.type,
                'provider': user.provider,
                'token': user.token.decode(),
                # 'refreshable': provider.refreshable, #TODO Implement refreshing
            }
        }})

    def log_exception(self, typ, value, tb):
        if isinstance(value, exceptions.JamException) and not value.should_log:
            return
        self.captureException((typ, value, tb))
        super().log_exception(typ, value, tb)

    def write_error(self, status_code, exc_info):
        etype, exc, _ = exc_info

        if not isinstance(exc, exceptions.JamException):
            return super().write_error(status_code, exc_info)

        self.set_status(int(exc.status))
        self.finish({'errors': [exc.serialize()]})
