import datetime

import jwt


# User_id = {user_type}-{provider}-{user_id}

class User:

    @classmethod
    def create(cls, type, provider, id, exp=1):
        return cls(jwt.encode({
            'sub': '-'.join([type, provider or '', id]),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=exp),
        }, 'TestKey'))

    def __init__(self, jwt_token, verify=True):
        if not jwt_token:
            self.id = None
            self.jwt = None
            self.uid = None
            self.type = None
            self.token = None
            self.provider = None
            return
        self.token = jwt_token
        self.jwt = jwt.decode(jwt_token, 'TestKey', verify=verify, option={'require_exp': True})
        self.uid = self.jwt['sub']
        type_, provider, *parts = self.uid.split('-')

        self.type = type_ or None
        self.provider = provider or None
        self.id = '-'.join(parts) or None
