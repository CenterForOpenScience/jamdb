import http.client

import tornado.web


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


class CORSMixin:
    CORS_ACCEPT_HEADERS = [
        'Content-Type',
        'Authorization',
        'Cache-Control',
        # 'X-Requested-With',
    ]

    CORS_EXPOSE_HEADERS = [
        'Content-Length',
        'Content-Encoding',
    ]

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', ', '.join(self.CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(self.CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        super().set_default_headers()

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, PATCH, POST, DELETE')


class Default404Handler(CORSMixin, tornado.web.RequestHandler):

    def get(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def put(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def post(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def delete(self):
        raise tornado.web.HTTPError(http.client.NOT_FOUND)

    def write_error(self, status_code, exc_info):
        etype, exc, _ = exc_info
        self.set_status(int(status_code))
        self.finish({
            'errors': [{
                'status': str(int(status_code)),
                'detail': self._reason,
            }]
        })

    # avoid dumping duplicate information to application log
    def log_exception(self, typ, value, tb):
        if isinstance(value, tornado.web.HTTPError):
            if value.log_message:
                format = "%d %s: " + value.log_message
                args = ([value.status_code, self._request_summary()] +
                        list(value.args))
                tornado.web.gen_log.warning(format, *args)
        else:
            tornado.web.app_log.error("Uncaught exception %s\n", self._request_summary(),
                                      exc_info=(typ, value, tb))
