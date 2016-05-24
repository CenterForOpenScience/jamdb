import datetime

import jwt

from jam import settings
from jam.auth.permissions import Permissions


# User_id = {user_type}-{provider}-{user_id}

class User:

    @classmethod
    def create(cls, type, provider, id, exp=1, limited=False, granted=None):
        return cls(jwt.encode({
            'limit': limited,
            'sub': '-'.join([type, provider or '', id]),
            'granted': {k: int(v) for k, v in (granted or {}).items()},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=exp),
        }, settings.JWT_SECRET))

    def __init__(self, jwt_token, verify=True):
        if not jwt_token:
            self.id = None
            self.jwt = None
            self.uid = None
            self.type = None
            self.token = None
            self.granted = {}
            self.limited = False
            self.provider = None
            return
        self.token = jwt_token
        self.jwt = jwt.decode(jwt_token, settings.JWT_SECRET, verify=verify, option={'require_exp': True})
        self.uid = self.jwt['sub']
        self.limited = self.jwt['limit']
        self.granted = {k: Permissions(v) for k, v in self.jwt['granted'].items()}
        type_, provider, *parts = self.uid.split('-')

        self.type = type_ or None
        self.provider = provider or None
        self.id = '-'.join(parts) or None
