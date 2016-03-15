import re
import http

import tornado.web

from jam import exceptions
from jam.auth import Permissions
from jam.server.api.v1.base.constants import ID_RE


class View:
    parent = None

    @classmethod
    def lineage(cls):
        p, parents = cls, []
        while p:
            parents.append(p)
            p = p.parent
        return list(reversed(parents))

    @classmethod
    def load(cls, id, *parents):
        raise NotImplementedError()

    def __init__(self, *parents, resource=None):
        self.parents = parents
        self.resource = resource
        self.loaded = (resource and self.parents + (resource, )) or self.parents

    def get_permissions(self, request):
        return Permissions.from_method(request.method)

    def validate_id(self, id):
        parent_re = r'\.'.join([re.escape(parent.ref) for parent in self.parents])
        tail = ID_RE if self.resource is None else re.escape(self.resource.ref)
        if id is None or re.match(r'^({}\.)?{}$'.format(parent_re, tail), str(id)) is None:
            raise exceptions.JamException(
                '400',
                http.client.BAD_REQUEST,
                'Invalid id',
                'Expected data.id {}, optionally prefixed by its parents ids seperated via .'.format(
                    'to match the Regex ' + ID_RE if self.resource is None else 'to be ' + self.resource.ref
                ),
                should_log=False
            )
        return id.split('.')[-1]

    def create(self, payload, user):
        id = self.validate_id(payload.get('id'))
        return self.do_create(id, payload['attributes'], user)

    def read(self, user):
        return self.resource

    def update(self):
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

    def delete(self):
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

    def list(self, filter, sort, page, page_size, user):
        return self.parents[-1].select().where(filter).page(page, page_size).order_by(sort)

    def do_create(self, id, attributes, user):
        raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)
