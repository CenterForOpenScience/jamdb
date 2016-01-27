import re
import datetime
import http.client

import jwt

import tornado.web

from raven.contrib.tornado import SentryMixin

from jam.auth import User
from jam import exceptions
from jam.auth import Permissions
from jam.server.api.jsonapi import JSONAPIHandler

NAMESPACER = '.'
ID_RE = r'[\d\w\-]{3,64}'
ENDING = r'(?:/{})?/?'


def ResourceEndpoint(view, serializer):
    v1, v2, kwargs = [], [], {'view': view, 'serializer': serializer}
    selector = r'(?P<{}_id>{})'.format(view.name, ID_RE)

    for v in view.lineage()[:-1]:
        # Just of list of resource id regexes that will be concatenated with NAMESPACER
        v2.append(r'(?P<{}_id>{})'.format(v.name, ID_RE))
        # Builds /resources/regexeforresourceid
        v1.extend([v.plural, r'(?P<{}_id>{})'.format(v.name, ID_RE)])

    relationships = '/v2/{}/{}/(?P<relationship>{})/?'.format(
        view.plural,
        NAMESPACER.join(v2 + [selector]),
        '|'.join(serializer.relations.keys())
    )

    v1.append(view.plural)

    v1 = '/v1/' + '/'.join(v1) + ENDING.format(selector)
    v2 = '/v2/' + view.plural + ENDING.format(NAMESPACER.join(v2 + [selector]))

    endpoints = [
        (v1, ResourceHandler, kwargs),
        (v2, ResourceHandler, kwargs),
    ]

    # If the serializer has relationships add a relationship handler
    if serializer.relations:
        endpoints.append((relationships, ResourceHandler, kwargs))

    return endpoints


class ResourceHandler(SentryMixin, JSONAPIHandler):
    TYPE_DATA_SET = {
        'PUT': {},
        'GET': {type(None)},
        'DELETE': {type(None)},
        'POST': {dict, list},
        'PATCH': {dict, list},
    }

    def get_current_user(self):
        try:
            return User(
                self.request.headers.get('Authorization') or
                self.get_query_argument('token', default=None)
            )
        except jwt.InvalidTokenError:
            return User(None)

    def serialize(self, inst):
        if inst is None:
            return None
        return self._serializer.serialize(self.request, inst, *self._view.parents)

    def initialize(self, view, serializer):
        self._view = None
        self._view_class = view
        self._serializer = serializer

    def prepare(self):
        super().prepare()
        if self.request.method == 'OPTIONS':
            return  # Dont do anything for OPTIONS requests

        loaded = []
        try:
            for view in self._view_class.lineage():
                key = view.name + '_id'
                if self.path_kwargs[key] is None:
                    break
                loaded.append(view.load(self.path_kwargs[key], *loaded))
        except exceptions.NotFound as e:
            err = e
            # Load as many resources as are available to do a permissions check
            # A 404 will be thrown if the user has the required permissions
            self._view = view(*loaded)
        else:
            err = None
            self._view = self._view_class(*loaded)

        # If this is a relationship swap out the current view with the relation
        if 'relationship' in self.path_kwargs:
            relationship = self._serializer.relations[self.path_kwargs['relationship']]
            self._view = relationship.view(*loaded)
            self._serializer = relationship.serializer()

        permissions = Permissions.get_permissions(self.current_user, *loaded)
        required_permissions = self._view.get_permissions(self.request)

        # For use later on
        self.current_user.permissions = permissions

        # Check permissions
        if (required_permissions & permissions) != required_permissions:
            if self.current_user.uid is None:
                raise exceptions.Unauthorized()
            raise exceptions.Forbidden(required_permissions)

        # Not found is always raised AFTER permissions checks
        if err:
            raise err

        if self.request.method in ('GET', 'DELETE'):
            return  # GET and DELETE bodies are ignored

        if not isinstance(self.json, (dict, list)):
            raise exceptions.MalformedData()

        # data = self.json.get('data', {})
        # if data.get('type') != self._view.plural:
        #     raise exceptions.IncorrectParameter('data.type', self._view.type, data.get('type', 'null'))

    # Create
    def post(self, **args):
        if self._view.resource:
            raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

        if not isinstance(self.json.get('data'), (list, dict)):
            raise exceptions.InvalidParameterType('data', 'List or Object', type(self.json.get('data')))

        if isinstance(self.json['data'], list):
            return self.post_bulk()

        new = self._view.create(self.json['data'], self.current_user)
        self.write({'data': self.serialize(new)})
        self.set_status(http.client.CREATED)

    def post_bulk(self):
        if 'bulk' not in self.extensions:
            raise exceptions.MissingExtension('bulk')
        new, errors = [], []
        for entry in self.json['data']:
            try:
                new.append(self._view.create(entry, self.current_user))
            except KeyError as e:
                new.append(None)
                # TODO take KeyError into account
                errors.append(exceptions.MalformedData().serialize())
            except (TypeError, ValueError):
                new.append(None)
                errors.append(exceptions.MalformedData().serialize())
            except exceptions.JamException as e:
                new.append(None)
                errors.append(e.serialize())
            else:
                errors.append(None)
        self.write({
            'data': [self.serialize(n) for n in new],
            'errors': errors
        })
        self.set_status(http.client.CREATED)

    # Read/List
    def get(self, **args):
        if self._view.resource:
            return self.write({
                'data': self.serialize(self._view.read(self.current_user))
            })

        selector = self._view.list(self.filter, self.sort, self.page, self.page_size, self.current_user)

        return self.write({
            'meta': {
                'total': selector.count(),
                'perPage': self.page_size
            },
            # TODO
            'links': {},
            'data': [self.serialize(resource) for resource in selector]
        })

    # Replace
    def put(self, **args):
        raise tornado.web.HTTPError(http.client.NOT_IMPLEMENTED)
        # self._view.replace(self.json['id'], self.json['data']['attributes'], self.current_user)

    # Update
    def patch(self, **args):
        if not self._view.resource:
            # Currently dont support creation/deletion via patch
            # See here for me detail http://jsonapi.org/extensions/jsonpatch/
            raise tornado.web.HTTPError(http.client.NOT_IMPLEMENTED)

        # I'm so sorry. Minimizes the amount of code needed for this check.
        # JsonPatch must have a list anything else must have a dict
        if ('jsonpatch' in self.extensions) ^ isinstance(self.json, list):
            if 'jsonpatch' not in self.extensions:
                raise exceptions.MissingExtension('jsonpatch')  # Got a list with incorrect Content-Type
            else:
                raise exceptions.InvalidParameterType('', 'List', 'Object')  # Got a dict with jsonpatch

        if isinstance(self.json, dict):
            try:
                patch = self.json['data']['attributes']
            except (KeyError, TypeError):
                raise exceptions.MalformedData()
        else:
            patch = self.json

        # NOTE: This response format diverges from the jsonpatch spec.
        # See here for me detail http://jsonapi.org/extensions/jsonpatch/
        return self.write({
            'data': self.serialize(self._view.update(patch, self.current_user))
        })

    # Delete
    def delete(self, **args):
        if not self._view.resource:
            raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)
        self._view.delete(self.current_user)
        self.set_status(http.client.NO_CONTENT)

    def log_exception(self, typ, value, tb):
        if isinstance(value, exceptions.JamException) and not value.should_log:
            return
        self.captureException((typ, value, tb))
        super().log_exception(typ, value, tb)

    def write_error(self, status_code, exc_info):
        etype, exc, _ = exc_info

        if not issubclass(etype, exceptions.JamException):
            return super().write_error(status_code, exc_info)

        self.set_status(int(exc.status))
        self.finish({'errors': [exc.serialize()]})


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

    def get_permissions(self, request):
        return Permissions.from_method(request.method)

    def validate_id(self, id):
        parent_re = r'\.'.join([parent.name for parent in self.parents])
        if re.match(r'^({}\.)?{}$'.format(parent_re, ID_RE), id) is None:
            raise exceptions.JamException(
                '400',
                http.client.BAD_REQUEST,
                'Invalid id',
                'Expected detail to match the Regex {}, optionally prefixed by its parents ids seperated via .'.format(ID_RE)
            )
        return id.split('.')[-1]

    def create(self, payload, user):
        id = self.validate_id(payload.get('id', ''))
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


class Serializer:
    view = None
    relations = {}

    @classmethod
    def serialize(cls, request, inst, *parents):
        return {
            'id': NAMESPACER.join([getattr(p, 'name', None) or p.ref for p in parents] + [inst.ref]),
            'type': cls.type,
            'meta': cls.meta(inst),
            # 'links': cls.links(request, inst, *parents),
            'attributes': cls.attributes(inst),
            'relationships': cls.relationships(request, inst, *parents)
        }

    @classmethod
    def relationships(cls, request, inst, *parents):
        return {
            name: relation.serialize(request, inst, *parents)
            for name, relation in cls.relations.items()
            if relation.included
        }

    @classmethod
    def meta(cls, inst):
        return {
            'created-by': inst.created_by,
            'modified-by': inst.modified_by,
            'created-on': datetime.datetime.fromtimestamp(inst.created_on).isoformat(),
            'modified-on': datetime.datetime.fromtimestamp(inst.created_on).isoformat()
        }


class Relationship:
    included = True

    @classmethod
    def serialize(cls, request, inst, *parents):
        return {
            'links': {
                'self': cls.self_link(request, inst, *parents),
                'related': cls.related_link(request, inst, *parents),
            }
        }

    @classmethod
    def view(inst, *parents):
        raise NotImplementedError()

    @classmethod
    def serializer(cls):
        raise NotImplementedError()

    @classmethod
    def self_link(request, inst, *parents):
        raise NotImplementedError()

    @classmethod
    def related_link(request, inst, *parents):
        raise NotImplementedError()
