import re
import logging

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

    def get_permissions(self, request):
        if request.method == 'POST':
            return Permissions.ADMIN
        return Permissions.READ

    def post(self, handler):
        if not self.sendgrid_key:
            raise exceptions.BadRequest(detail='sendgridKey must be provided via collection.plugins.sendgridKey')

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
        user = User.create('self', '{}:{}'.format(namespace.ref, self.collection.ref), doc.ref, exp=8)

        try:
            sg = sendgrid.SendGridClient(self.sendgrid_key, raise_errors=True)
            mail = sendgrid.Mail(to=email)

            mail.set_from(self.from_email)
            mail.add_substitution(':token', user.token.decode())
            mail.add_filter('templates', 'enable', 1)
            mail.add_filter('templates', 'template_id', self.template)
            # Sendgrid requires subject text and html to be set to a non falsey value
            # Its highly recommened that you overwrite these in your own templates
            mail.set_subject('JamDB password reset')
            mail.set_text('Your temporary token is :token')
            mail.set_html('Your temporary token is :token')

            sg.send(mail)
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
