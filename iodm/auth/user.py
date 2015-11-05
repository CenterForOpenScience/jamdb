import jwt


class User:

    def __init__(self, jwt_token, verify=True):
        if not jwt_token:
            self.id = None
            self.jwt = None
            self.uid = None
            self.type = None
            self.provider = None
            return
        self.jwt = jwt.decode(jwt_token, 'TestKey', verify=verify, option={'require_exp': True})
        self.uid = self.jwt['sub']
        type_, provider, *parts = self.uid.split('-')

        self.type = type_ or None
        self.provider = provider or None
        self.id = '-'.join(parts) or None
