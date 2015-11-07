import tornado.web

from iodm.auth import Permissions
from iodm.server.api.base import BaseAPIHandler


class ResourceHandler(BaseAPIHandler):

    def initialize(self, resource):
        self.resource = resource

    def prepare(self):
        super().prepare()
        resources = []
        resource = self.resource
        while resource:
            resources = [resource] + resources
            resource = resource.parent

        loaded = [
            r.load(self.path_kwargs[r.name + '_id'], self.request)
            for r in resources
            if self.path_kwargs.get(r.name + '_id')
        ]

        self.permissions = Permissions.get_permissions(self.current_user, *loaded)
        self.permissions = Permissions.ADMIN
        # TODO this is kinda hacky
        self.user.permissions = self.permissions
        assert Permissions.from_method(self.request.method) & self.permissions

    def get(self, **kwargs):
        if self.resource.resource is not None:
            data = self.resource.read()
        else:
            data = self.resource.list()
        return self.write(data)

    def post(self, **kwargs):
        assert self.resource.resource is None
        data = self.json['data']
        assert data['type'] == self.resource.name
        self.set_status(201)
        self.write(self.resource.create(data, self.current_user))

    def put(self, **kwargs):
        assert self.resource.resource is not None
        data = self.json['data']
        assert data['id'] == self.path_kwargs[self.resource.name + '_id']
        assert data['type'] == self.resource.name
        return self.write(self.resource.replace(data, self.current_user))

    def patch(self, **kwargs):
        assert self.resource.resource is not None
        data = self.json['data']
        assert data['id'] == self.path_kwargs[self.resource.name + '_id']
        assert data['type'] == self.resource.name
        return self.write(self.resource.replace(data, self.current_user))

    def delete(self, **kwargs):
        self.set_status(204)
        self.resource.delete(self.current_user)


class APIResource:

    @classmethod
    def as_handler_entry(cls):
        inst = cls()
        return (inst.general_pattern, ResourceHandler, {'resource': inst})

    @property
    def general_pattern(self):
        if self.parent:
            url = self.parent.specific_pattern
        else:
            url = '/'
        return '{0}{1}s(?:/(?P<{1}_id>\w+))?/?'.format(url, self.name)

    @property
    def specific_pattern(self):
        if self.parent:
            url = self.parent.specific_pattern
        else:
            url = '/'
        return '{0}{1}s/(?P<{1}_id>\w+)/'.format(url, self.name)

    def __init__(self, resource_name, parent=None):
        if parent:
            self.parent = parent()
        else:
            self.parent = None
        self.name = resource_name
        self.resource = None

    def load(self, resource):
        self.resource = resource
        return resource

    def list(self):
        raise tornado.web.HTTPError(405)

    def create(self):
        raise tornado.web.HTTPError(405)

    def read(self):
        raise tornado.web.HTTPError(405)

    def update(self):
        raise tornado.web.HTTPError(405)

    def replace(self):
        raise tornado.web.HTTPError(405)

    def delete(self):
        raise tornado.web.HTTPError(405)
