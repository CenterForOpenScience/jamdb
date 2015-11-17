import abc
import json

import furl

import tornado.web

from iodm.auth import User
from iodm import exceptions


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


class BaseAPIHandler(tornado.web.RequestHandler, metaclass=abc.ABCMeta):

    def get_current_user(self):
        return User(
            self.request.headers.get('Authorization') or
            self.get_query_argument('token', default=None) or
            self.get_cookie('cookie')
        )

    @classmethod
    def as_entry(cls):
        return (cls.PATTERN, cls)

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = json.loads(self.request.body.decode())
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
        if isinstance(value, exceptions.IodmException) and not value.should_log:
            return
        super().log_exception(typ, value, tb)

    def write_error(self, status_code, exc_info):
        etype, exc, _ = exc_info

        if issubclass(etype, exceptions.IodmException):
            self.set_status(exc.code)
            if exc.data:
                self.finish(exc.data)
            else:
                self.finish({
                    'code': exc.code,
                    'message': exc.message
                })
        else:
            self.finish({
                'code': status_code,
                'message': self._reason,
            })
