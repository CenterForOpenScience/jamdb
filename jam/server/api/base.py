import abc
import json
import http.client

import jwt
import furl

import tornado.web

from raven.contrib.tornado import SentryMixin

from jam.auth import User
from jam import exceptions


CORS_ACCEPT_HEADERS = [
    'Range',
    'Content-Type',
    'Authorization',
    'Cache-Control',
    'X-Requested-With',
]

CORS_EXPOSE_HEADERS = [
    'Range',
    'Accept-Ranges',
    'Content-Range',
    'Content-Length',
    'Content-Encoding',
]


class BaseAPIHandler(tornado.web.RequestHandler, SentryMixin, metaclass=abc.ABCMeta):

    def get_current_user(self):
        try:
            return User(
                self.request.headers.get('Authorization') or
                self.get_query_argument('token', default=None) or
                self.get_cookie('cookie')
            )
        except jwt.ExpiredSignatureError:
            return User(None)

    @classmethod
    def as_entry(cls):
        return (cls.PATTERN, cls)

    @property
    def json(self):
        if not hasattr(self, '_json'):
            try:
                self._json = json.loads(self.request.body.decode())
            except ValueError:
                raise exceptions.MalformedData()
            if not isinstance(self._json, dict):
                raise exceptions.MalformedData()
        return self._json

    @property
    def furl(self):
        if not hasattr(self, '_furl'):
            self._furl = furl.furl(self.request.full_url().rstrip('/')).set(args={})
        return self._furl.copy()

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')

    def log_exception(self, typ, value, tb):
        if isinstance(value, exceptions.JamException) and not value.should_log:
            return
        self.captureException((typ, value, tb))
        super().log_exception(typ, value, tb)

    def write_error(self, status_code, exc_info):
        etype, exc, _ = exc_info

        if issubclass(etype, exceptions.JamException):
            self.set_status(int(exc.status))
            self.finish({'errors': [exc.serialize()]})
        else:
            self.set_status(int(status_code))
            self.finish({
                'errors': [{
                    'status': status_code,
                    'detail': self._reason,
                }]
            })


class Default404Handler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))

    def get(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def put(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def post(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def delete(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def options(self):
        self.set_status(204)
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')

    def write_error(self, status_code, exc_info):
        etype, exc, _ = exc_info

        if issubclass(etype, exceptions.JamException):
            self.set_status(int(exc.status))
            self.finish({'errors': [exc.serialize()]})
        else:
            self.set_status(int(status_code))
            self.finish({
                'errors': [{
                    'status': str(int(status_code)),
                    'detail': self._reason,
                }]
            })
