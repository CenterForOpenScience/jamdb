import abc
import json
import time
import calendar

import furl

import tornado.web

from dateutil.parser import parse

import iodm
from iodm.backends import EphemeralBackend


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


class TimeMachineAPIHandler(BaseAPIHandler):

    def initialize(self, namespacer):
        self.namespacer = namespacer

    def prepare(self):
        maybe_time = self.get_query_argument('timemachine', default=None)
        self.collection = self.namespacer.get_collection(self.path_kwargs['collection_id'], regenerate=False)

        if maybe_time is not None:

            if self.request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
                raise Exception('Read only')

            try:
                timestamp = int(maybe_time)
            except ValueError:
                timestamp = calendar.timegm(parse(maybe_time).utctimetuple())

            self.collection = self.collection.at_time(
                timestamp,
                iodm.Snapshot(EphemeralBackend()),
                regenerate=False
            )

        # if self.collection.regenerate() > 200:
            # self.collection.snapshot()
