import re
import logging

import mandrill

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
            'mandrillKey': {'type': 'string'},
            'createdIsOwner': {'type': 'boolean'},
        },
        'additionalProperties': False,
    }

    @classmethod
    def get_type(cls, request):
        if request.method == 'POST':
            return 'reset'
        return None

    @property
    def template(self):
        return self._raw.get('template', 'password-reset')

    @property
    def mandrill_key(self):
        return self._raw.get('mandrillKey', None)

    @property
    def email_field(self):
        return self._raw.get('emailField', 'email')

    @property
    def created_is_owner(self):
        return self._raw.get('createdIsOwner', False)

    def get_permissions(self, request):
        if request.method == 'POST':
            return Permissions.ADMIN
        return Permissions.READ

    def post(self, handler):
        if not self.mandrill_key:
            raise exceptions.BadRequest(detail='mandrillKey must be provided via collection.plugins.mandrillKey')

        if not handler.payload:
            raise exceptions.BadRequest(detail='mandrillKey must be provided via collection.plugins.mandrillKey')

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
        user = User.create('self', '{}:{}'.format(namespace.ref, self.collection.ref), doc.ref, exp=8)

        try:
            mandrill.Mandrill(self.mandrill_key).messages.send_template(
                template_name=self.template,
                template_content=[{'token': user.token}],
                message={'to': [{'email': email}]}
            )
        except mandrill.Error:
            logger.exception('Mandrill Error:')
            raise exceptions.ServiceUnavailable(detail='Unable to submit request to mandrill')

        return handler.write({
            'data': {
                'id': handler.payload.attributes.get('id'),
                'type': 'reset',
                'attributes': {
                    'status': 'success'
                }
            }
        })
