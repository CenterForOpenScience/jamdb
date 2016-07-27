import asyncio
import http.client

import jwt

import tornado.web

from raven.contrib.tornado import SentryMixin

from jam.auth import User
from jam import exceptions
from jam.server.api.jsonapi import JSONAPIHandler
from jam.server.api.jsonapi import BulkPayload
from jam.server.api.jsonapi import JsonAPIPayload


NAMESPACER = '.'
ID_RE = r'[\d\w\-]{3,64}'
ENDING = r'(?:/{})?/?'


class ResourceHandler(SentryMixin, JSONAPIHandler):

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
        return self._serializer(self.request, self.current_user, inst, *self._view.parents).serialize()

    def initialize(self, view, serializer):
        self._view = None
        self._view_class = view
        self._serializer = serializer

    def load_view(self, root_view):
        loaded = []
        try:
            for view in root_view.lineage():
                key = view.name + '_id'
                if self.path_kwargs[key] is None:
                    break
                loaded.append(view.load(self.path_kwargs[key], *loaded))
        except exceptions.NotFound as e:
            # Load as many resources as are available to do a permissions check
            # A 404 will be thrown if the user has the required permissions
            return view(*loaded), e
        return root_view(*loaded), None

    def check_permissions(self):
        permissions = self._view.get_permissions(self.current_user, self._view.loaded)
        required_permissions = self._view.get_required_permissions(self.request)

        # For use later on
        self.current_user.permissions = permissions

        # Check permissions
        if (required_permissions & permissions) != required_permissions:
            if self.current_user.uid is None:
                raise exceptions.Unauthorized()
            raise exceptions.Forbidden(required_permissions)

    def prepare(self):
        super().prepare()
        if self.request.method == 'OPTIONS':
            return  # Dont do anything for OPTIONS requests

        self._view, err = self.load_view(self._view_class)

        self.check_permissions()

        # Not found is always raised AFTER permissions checks
        if err:
            raise err

        if self.request.method in ('GET', 'DELETE'):
            return  # GET and DELETE bodies are ignored

        self.payload  # Force payload to load and validate

    # Create
    def post(self, **args):
        if self._view.resource:
            raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)

        if isinstance(self.payload, BulkPayload):
            return self.post_bulk()

        if self.payload.type != self._view.plural:
            raise exceptions.IncorrectParameter('data.type', self._view.plural, self.payload.type)

        new = self._view.create(self.payload._raw['data'], self.current_user)
        self.write({'data': self.serialize(new)})
        self.set_status(http.client.CREATED)

    def post_bulk(self):
        new, errors = [], []
        for entry in self.payload.payloads:

            if entry.type != self._view.plural:
                raise exceptions.IncorrectParameter('data.type', self._view.plural, entry.type)

            try:
                new.append(self._view.create(entry._raw['data'], self.current_user))
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
        if not self._view.resource:
            raise tornado.web.HTTPError(http.client.METHOD_NOT_ALLOWED)
        raise tornado.web.HTTPError(http.client.NOT_IMPLEMENTED)
        # self._view.replace(self.json['id'], self.json['data']['attributes'], self.current_user)

    # Update
    def patch(self, **args):
        if not self._view.resource:
            # Currently dont support creation/deletion via patch
            # See here for me detail http://jsonapi.org/extensions/jsonpatch/
            raise tornado.web.HTTPError(http.client.NOT_IMPLEMENTED)

        if isinstance(self.payload, JsonAPIPayload):
            patch = self.payload.attributes
            self._view.validate_id(self.payload.id)

            if self.payload.type != self._view.plural:
                raise exceptions.IncorrectParameter('data.type', self._view.plural, self.payload.type)
        else:
            patch = self.payload.patches

        # NOTE: This response format diverges from the jsonpatch spec.
        # See here for me detail http://jsonapi.org/extensions/jsonpatch/
        return self.write({
            'data': self.serialize(self._view.update(patch, self.current_user))
        })

    # Delete
    def delete(self, **kargs):
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

        if not isinstance(exc, exceptions.JamException):
            return super().write_error(status_code, exc_info)

        self.set_status(int(exc.status))
        self.finish({'errors': [exc.serialize()]})


# The hardest job of them all
class RelationshipHandler(ResourceHandler):

    def load_view(self, root_view):
        view, err = super().load_view(root_view)

        if err:
            # Dont bother loading additional views if an error was encountered
            return view, err

        # Swap out the current view with the relation
        relationship = self._serializer.relations[self.path_kwargs['relationship']]
        self._serializer = relationship.serializer()

        return relationship.view(*view.loaded), None


class PluginHandler(ResourceHandler):

    def load_view(self, root_view):
        view, err = super().load_view(root_view)

        if err:
            # Dont bother loading additional views if an error was encountered
            return view, err

        # Load up the plugin
        self.plugin = view.resource.plugin(self._serializer.plugins[self.path_kwargs['plugin']])

        self.plugin.prerequisite_check()

        # _view is only for permission handling
        return view, None

    def _check_type(self):
        type = self.plugin.get_type(self.request)
        if type and self.payload.type != type:
            raise exceptions.IncorrectParameter('data.type', type, self.payload.type)

    def check_permissions(self):
        permissions = self._view.get_permissions(self.current_user, self._view.loaded)
        required_permissions = self.plugin.get_required_permissions(self.request)

        # For use later on
        self.current_user.permissions = permissions

        # Check permissions
        if (required_permissions & permissions) != required_permissions:
            if self.current_user.uid is None:
                raise exceptions.Unauthorized()
            raise exceptions.Forbidden(required_permissions)

    async def post(self, **args):
        self._check_type()
        # Set before to allow plugins to augment
        self.set_status(http.client.CREATED)
        resp = self.plugin.post(self)
        if asyncio.iscoroutine(resp):
            await resp

    async def get(self, **args):
        resp = self.plugin.get(self)
        if asyncio.iscoroutine(resp):
            await resp

    async def put(self, **args):
        self._check_type()
        resp = self.plugin.put(self)
        if asyncio.iscoroutine(resp):
            await resp

    async def patch(self, **args):
        self._check_type()
        resp = self.plugin.patch(self)
        if asyncio.iscoroutine(resp):
            await resp

    async def delete(self, **args):
        # Set before to allow plugins to augment
        self.set_status(http.client.NO_CONTENT)
        resp = self.plugin.delete(self)
        if asyncio.iscoroutine(resp):
            await resp
