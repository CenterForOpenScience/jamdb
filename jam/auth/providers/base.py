from jam.auth import User


class BaseAuthProvider:
    refreshable = False

    async def _refresh(self, user):
        raise NotImplementedError

    async def _authenticate(self, data):
        raise NotImplementedError

    async def authenticate(self, user, data):
        if user and user.provider == self.type and self.refreshable:
            return User.create(*await self._refresh(user))
        return User.create(*await self._authenticate(data))
