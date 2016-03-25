from jam import exceptions
from jam.auth import Permissions


class Plugin:
    SCHEMA = None
    EXPLICIT = True
    DEFAULTS = None

    @classmethod
    def get_type(cls, request):
        return None

    @classmethod
    def is_enabled(cls, collection):
        return cls.NAME in collection.plugins

    def __init__(self, collection):
        self.collection = collection
        self._raw = collection.plugins.get(self.__class__.NAME, {})

    def prerequisite_check(self):
        if self.EXPLICIT and self.NAME not in self.collection.plugins:
            raise exceptions.PluginNotEnabled(self.NAME)

    def get_permissions(self, request):
        return Permissions.ADMIN

    def get(self, handler):
        raise exceptions.MethodNotAllowed('GET')

    def post(self, handler):
        raise exceptions.MethodNotAllowed('POST')

    def put(self, handler):
        raise exceptions.MethodNotAllowed('PUT')

    def patch(self, handler):
        raise exceptions.MethodNotAllowed('PATCH')

    def delete(self, handler):
        raise exceptions.MethodNotAllowed('DELETE')
