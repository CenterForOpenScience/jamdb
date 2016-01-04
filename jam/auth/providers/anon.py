import uuid

from jam.auth.providers.base import BaseAuthProvider


class AnonAuthProvider(BaseAuthProvider):
    name = None
    type = 'anon'
    refreshable = True

    async def _refresh(self, user):
        return 'anon', None, user.id

    async def _authenticate(self, data):
        return 'anon', None, str(uuid.uuid4()).replace('-', '')
