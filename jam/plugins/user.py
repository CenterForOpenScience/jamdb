import re
import json
import logging
from urllib.parse import quote

import aiohttp
import sendgrid

from jam.auth import User
from jam import exceptions
from jam.auth import Permissions
from jam.plugins.base import Plugin


logger = logging.getLogger(__name__)
EMAIL_RE = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


class UserPlugin(Plugin):
    NAME = 'user'
    EXPLICIT = True
    SCHEMA = {
        'type': 'object',
        'properties': {
            'template': {'type': 'string'},
            'emailField': {'type': 'string'},
            'sendgridKey': {'type': 'string'},
            'createdIsOwner': {'type': 'boolean'},
            'fromEmail': {'type': 'string', 'pattern': EMAIL_RE}
        },
        'additionalProperties': False,
    }

    @classmethod
    def get_type(cls, request):
        if request.method == 'POST':
            return 'reset'
        if request.method in ('PATCH', 'GET'):
            return 'supressions'
        return None

    @property
    def template(self):
        return self._raw.get('template')

    @property
    def sendgrid_key(self):
        return self._raw.get('sendgridKey')

    @property
    def email_field(self):
        return self._raw.get('emailField', 'email')

    @property
    def from_email(self):
        return self._raw.get('fromEmail')

    @property
    def created_is_owner(self):
        return self._raw.get('createdIsOwner', False)

    def get_required_permissions(self, request):
        return Permissions.NONE  # TODO validate

    def prerequisite_check(self):
        super().prerequisite_check()
        if not self.sendgrid_key:
            raise exceptions.BadRequest(detail='sendgridKey must be provided via collection.plugins.sendgridKey')

    def extract_email(self, id=None, doc=None):
        doc = doc or self.collection.read(id)
        email = doc.data.get(self.email_field, 'null')
        if re.match(EMAIL_RE, email) is None:
            raise exceptions.BadRequest(detail='"{}" at "{}" is not a valid email'.format(email, self.email_field))
        return email

    async def get(self, handler):
        error = None
        id = handler.get_query_argument('id')

        try:
            doc = self.collection.read(id)
        except exceptions.NotFound as e:
            error = e

        permissions = handler.current_user.permissions | Permissions.get_permissions(handler.current_user, doc)

        if error or not (permissions & Permissions.READ):
            return handler.write({
                'data': {
                    'id': id,
                    'type': 'suppressions',
                    'attributes': {}
                }
            })

        attrs = {}
        email = self.extract_email(doc=doc)
        groups = handler.get_query_arguments('group[]')

        for group in groups:
            async with aiohttp.get('https://api.sendgrid.com/v3/asm/groups/{}/suppressions'.format(group), headers={'Authorization': 'Bearer {}'.format(self.sendgrid_key)}) as response:
                if response.status != 200 or not isinstance(await response.json(), list):
                    attrs[group] = False
                else:
                    attrs[group] = email in await response.json()

        return handler.write({
            'data': {
                'id': id,
                'type': 'supressions',
                'attributes': attrs
            }
        })

    async def patch(self, handler):
        if not handler.payload:
            raise exceptions.BadRequest()

        if not handler.payload.attributes.get('id'):
            raise exceptions.BadRequest(detail='Id must be provided')

        error = None
        id = handler.payload.attributes.pop('id')

        try:
            doc = self.collection.read(id)
        except exceptions.NotFound as e:
            error = e

        permissions = handler.current_user.permissions | Permissions.get_permissions(handler.current_user, doc)
        if error or not (permissions & Permissions.UPDATE):
            return handler.write({
                'data': {
                    'id': id,
                    'type': 'suppressions',
                    'attributes': {}
                }
            })

        email = self.extract_email(doc=doc)
        headers = {'Authorization': 'Bearer {}'.format(self.sendgrid_key)}

        for group, subscribe in list(handler.payload.attributes.items()):
            if subscribe:
                async with aiohttp.post('https://api.sendgrid.com/v3/asm/groups/{}/suppressions'.format(group), headers=headers, data=json.dumps({'recipient_emails': [email]})) as response:
                    assert response.status == 201  # TODO Handle errors
            else:
                async with aiohttp.delete('https://api.sendgrid.com/v3/asm/groups/{}/suppressions/{}'.format(group, quote(email)), headers=headers) as response:
                    assert response.status == 204  # TODO Handle errors
            handler.payload.attributes[group] = bool(subscribe)

        return handler.write({
            'data': {
                'id': id,
                'type': 'supressions',
                'attributes': handler.payload.attributes
            }
        })

    def post(self, handler):
        if not self.template:
            raise exceptions.BadRequest(detail='template must be provided via collection.plugins.template')

        if not self.from_email:
            raise exceptions.BadRequest(detail='fromEmail must be provided via collection.plugins.fromEmail')

        if not handler.payload:
            raise exceptions.BadRequest()

        if not handler.payload.attributes.get('id'):
            raise exceptions.BadRequest(detail='Id must be provided')

        try:
            doc = self.collection.read(handler.payload.attributes['id'])
        except exceptions.NotFound:
            return handler.write({
                'data': {
                    'id': handler.payload.attributes.get('id'),
                    'type': 'reset',
                    'attributes': {
                        'status': 'success'
                    }
                }
            })

        email = doc.data.get(self.email_field, 'null')
        if re.match(EMAIL_RE, email) is None:
            raise exceptions.BadRequest(detail='"{}" at "{}" is not a valid email'.format(email, self.email_field))

        namespace = handler._view._namespace  # A little hack never hurt anyone
        from jam.auth.providers.self import SelfAuthProvider
        user = User.create(SelfAuthProvider.type, '{}:{}'.format(namespace.ref, self.collection.ref), doc.ref, exp=8)

        try:
            sg = sendgrid.SendGridClient(self.sendgrid_key, raise_errors=True)
            mail = sendgrid.Mail(to=email)

            mail.set_from(self.from_email)
            mail.add_substitution(':token', user.token.decode())
            mail.add_substitution(':user', user.id)
            mail.add_filter('templates', 'enable', 1)
            mail.add_filter('templates', 'template_id', self.template)
            # Sendgrid requires subject text and html to be set to a non falsey value
            # It is highly recommended that you overwrite these in your own templates
            mail.set_subject('JamDB password reset')
            mail.set_text('Your temporary token is :token')
            mail.set_html('Your temporary token is :token')

            logger.info(sg.send(mail))
        except sendgrid.SendGridError:
            logger.exception('Sendgrid Error:')
            raise exceptions.ServiceUnavailable(detail='Unable to submit request to sendgrid')

        return handler.write({
            'data': {
                'id': handler.payload.attributes.get('id'),
                'type': 'reset',
                'attributes': {
                    'status': 'success'
                }
            }
        })
