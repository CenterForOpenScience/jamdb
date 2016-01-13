import re

import tornado.web

from jam import exceptions
from jam.auth import Permissions
from jam.server.api.base import BaseAPIHandler


class ResourceHandler(BaseAPIHandler):

    @property
    def page(self):
        return self.parse_int_with_bounds(self.get_query_argument('page', default=1), lower=1)

    @property
    def page_size(self):
        return self.parse_int_with_bounds(self.get_query_argument('page[size]', default=self.resource.PAGE_SIZE), lower=0)

    def parse_int_with_bounds(self, raw, lower=None, upper=None):
        try:
            num = int(raw)
        except (TypeError, ValueError):
            raise Exception()
        if (lower and num < lower) or (upper and num > upper):
            raise Exception()
        return num

    def initialize(self, resource):
        self.resource = resource()

    def prepare(self):
        super().prepare()
        if self.request.method == 'OPTIONS':
            return  # Dont do anything for OPTIONS requests

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

        # TODO this is kinda hacky
        self.current_user.permissions = self.permissions

        # TODO 404s get raised before permissions are checked
        required_permissions = self.resource.get_permissions(self.request)
        if (required_permissions & self.permissions) != required_permissions:
            if self.current_user.uid is None:
                raise exceptions.Unauthorized()
            raise exceptions.Forbidden(required_permissions)

    def parse_filter(self):
        filter_dict = {}
        matcher = re.compile(r'filter\[(.+)\]')
        for key in self.request.query_arguments:
            match = matcher.match(key)
            if match:
                if match.groups()[-1] in {'ref'}:
                    filter_dict[match.groups()[-1]] = self.request.query_arguments[key][-1].decode()
                else:
                    filter_dict['data.{}'.format(match.groups()[-1])] = self.request.query_arguments[key][-1].decode()
        return filter_dict

    def get(self, **kwargs):
        # Get a specific resource
        if self.resource.resource is not None:
            return self.write({
                'data': self.resource.serialize(self.resource.read(self.current_user), self.request)
            })

        # Resource listing
        selector = self.resource.list(self.current_user, filter=self.parse_filter())
        return self.write({
            'data': [self.resource.__class__.serialize(x, self.request) for x in selector.page(self.page - 1, self.page_size)],
            'meta': {
                'total': selector.count(),
                'perPage': self.page_size
            },
            'links': {}
        })

    def post(self, **kwargs):
        if self.resource.resource is not None:
            raise tornado.web.HTTPError(405)

        try:
            data = self.json['data']
        except KeyError:
            raise exceptions.InvalidParameterType('data', dict, None)

        if data.get('type') != self.resource.type:
            raise exceptions.IncorrectParameter('data.type', self.resource.type, data.get('type'))

        self.set_status(201)
        self.write({
            'data': self.resource.__class__.serialize(self.resource.create(data, self.current_user), self.request)
        })

    def put(self, **kwargs):
        assert self.resource.resource is not None
        data = self.json['data']
        assert data['id'] == self.path_kwargs[self.resource.name + '_id']
        assert data['type'] == self.resource.type
        return self.write({
            'data': self.resource.__class__.serialize(self.resource.replace(data, self.current_user), self.request)
        })

    def patch(self, **kwargs):
        assert self.resource.resource is not None
        data = self.json['data']
        assert data['id'] == self.path_kwargs[self.resource.name + '_id']
        assert data['type'] == self.resource.type
        return self.write({
            'data': self.resource.__class__.serialize(self.resource.update(data, self.current_user), self.request)
        })

    def delete(self, **kwargs):
        self.set_status(204)
        self.resource.delete(self.current_user)


class APIResource:
    ID_RE = r'[\d\w\.\-]{3,64}'

    @classmethod
    def as_handler_entry(cls):
        inst = cls()
        return (inst.general_pattern, ResourceHandler, {'resource': cls})

    @property
    def general_pattern(self):
        if self.parent:
            url = self.parent.specific_pattern
        else:
            url = '/'
        return '{0}{1}(?:/(?P<{2}_id>{3}))?/?'.format(url, self.plural, self.name, self.__class__.ID_RE)

    @property
    def specific_pattern(self):
        if self.parent:
            url = self.parent.specific_pattern
        else:
            url = '/'
        return '{0}{1}/(?P<{2}_id>{3}?)/'.format(url, self.plural, self.name, self.__class__.ID_RE)

    def __init__(self, resource_name, parent=None, plural=None):
        if parent:
            self.parent = parent()
        else:
            self.parent = None

        self.resource = None
        self.name = resource_name
        self.plural = plural or self.name + 's'
        self.type = self.plural

    def get_permissions(self, request):
        return Permissions.from_method(request.method)

    def load(self, resource):
        self.resource = resource
        return resource

    def create(self, data, user):
        raise tornado.web.HTTPError(405)

    def read(self, user):
        raise tornado.web.HTTPError(405)

    def update(self, data, user):
        raise tornado.web.HTTPError(405)

    def delete(self, user):
        raise tornado.web.HTTPError(405)

    def list(self, user, page=0, filter=None):
        raise tornado.web.HTTPError(405)

    def replace(self, data, user):
        raise tornado.web.HTTPError(405)
