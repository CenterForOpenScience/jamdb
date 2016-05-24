import functools
import http.client
import operator
import re
import weakref

import tornado.web
import ujson as json

import jam
from jam import exceptions
from jam.server.api.base import CORSMixin
from jam.server.api.jsonapi.parser import parse


def parse_value(raw):
    try:
        return int(raw)
    except ValueError:
        pass

    try:
        return float(raw)
    except ValueError:
        return raw


def parse_int(raw, lo=None, hi=None):
    try:
        num = int(raw)
    except (TypeError, ValueError):
        raise tornado.web.HTTPError(http.client.BAD_REQUEST)
    if lo is not None and num < lo:
        raise tornado.web.HTTPError(http.client.BAD_REQUEST)
    if hi is not None and num > hi:
        raise tornado.web.HTTPError(http.client.BAD_REQUEST)
    return num


class cached_property:

    def __init__(self, get_func, set_func=False):
        self.__get__ = functools.wraps(self.__get__, get_func)
        self._cache = weakref.WeakKeyDictionary()
        self._get_func = get_func
        self._set_func = set_func

    def __get__(self, inst, type=None):
        if inst not in self._cache:
            self._cache[inst] = self._get_func(inst)
        return self._cache[inst]


class JSONAPIHandler(CORSMixin, tornado.web.RequestHandler):
    DEFAULT_SORT = 'ref'
    MAX_PAGE_SIZE = 100
    DEFAULT_PAGE_SIZE = 50
    EXTENSIONS = ['bulk', 'jsonpatch']

    @cached_property
    def page(self):
        # Note: the query parameter page is 1 based
        # Anywhere else in this code, including the return of this function, is 0 based
        return parse_int(self.get_query_argument('page', default=1), lo=1) - 1

    @cached_property
    def page_size(self):
        return parse_int(
            self.get_query_argument('page[size]', default=self.DEFAULT_PAGE_SIZE),
            lo=0,
            hi=self.MAX_PAGE_SIZE
        )

    @cached_property
    def filter(self):
        filter_dict = {}
        matcher = re.compile(r'filter\[(.+)\]')
        for key in self.request.query_arguments:
            match = matcher.match(key)
            if match:
                if match.groups()[-1] in {'ref'}:
                    filter_dict[match.groups()[-1]] = self.request.query_arguments[key][-1].decode()
                else:
                    filter_dict['data.{}'.format(match.groups()[-1])] = self.request.query_arguments[key][-1].decode()
        if not filter_dict:
            return None
        return functools.reduce(operator.and_, [
            jam.Q(key, 'eq', parse_value(value))
            for key, value in filter_dict.items()
        ])

    @cached_property
    def json(self):
        try:
            return json.loads(self.request.body.decode())
        except ValueError:
            raise exceptions.MalformedData()

    @cached_property
    def payload(self):
        return parse(self.request.method, self.json, self.extensions)

    @cached_property
    def sort(self):
        sort = self.get_query_argument('sort', default=None)
        if not sort:
            return jam.O.Ascending(self.DEFAULT_SORT)
        if re.match('^[\-\+]?[\d\w\.]+$', sort) is None:
            raise tornado.web.HTTPError(http.client.BAD_REQUEST)
        return jam.O(
            ('' if sort.lstrip('+-') in {'ref', 'created_on', 'modified_on'} else 'data.') + sort.lstrip('+-'),
            {'-': jam.O.DESCENDING}.get(sort[0], jam.O.ASCENDING)
        )

    @cached_property
    def extensions(self):
        spl = self.request.headers.get('Content-Type', '').split('ext=')
        if len(spl) < 2:
            return []
        return [ext.strip() for ext in spl[1].strip('";').split(',')]

    def set_default_headers(self):
        super().set_default_headers()
        self.set_header('Accept', 'application/vnd.api+json; ext=jsonpatch')
        self.set_header('Content-Type', 'application/vnd.api+json; ext=jsonpatch')

    def prepare(self):
        super().prepare()
        if self.request.method == 'OPTIONS':
            pass

        # TODO Implement content negotiation
        # http://jsonapi.org/format/#content-negotiation-servers
        # if not self.request.headers.get('Content-Type')
        # if not self.get_content_type().startswith('application/vnd.api+json'):
        #     raise tornado.web.HTTPError(http.client.UNSUPPORTED_MEDIA_TYPE)

    def set_status(self, status, reason=None):
        return super().set_status(int(status), reason=reason)

    def write_error(self, status_code, exc_info):
        self.set_status(int(status_code))
        self.finish({
            'errors': [{
                'detail': getattr(exc_info[1], 'log_message', self._reason),
                'status': str(int(status_code)),
                'title': self._reason,
            }]
        })
