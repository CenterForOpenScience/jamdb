import os
import asyncio
import logging

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.platform.asyncio

from jam import settings
from jam.server.api import v1
from jam.server.api.base import Default404Handler


HERE = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def make_app():
    endpoints = [
        ('/v1/auth/?', v1.AuthHandler),
        ('/v1/docs/()?', tornado.web.StaticFileHandler, {'path': os.path.join(HERE, 'static/doc/v1.html')}),
    ]

    for endpoint in reversed(v1.RESOURCES):
        endpoint = endpoint.as_handler_entry()
        endpoint = (
            '/{}{}'.format(v1.__name__.split('.')[-1], endpoint[0]),
            endpoint[1], endpoint[2]
        )
        endpoints.append(endpoint)
        logger.info('Loaded {} endpoint "{}"'.format(v1.__name__, endpoint[0]))

    return tornado.web.Application(
        endpoints,
        xheaders=settings.XHEADERS,
        debug=settings.DEBUG,
        default_handler_class=Default404Handler,
    )


def profile(ktime=10):
    asyncio.get_event_loop().call_later(ktime, lambda: asyncio.get_event_loop().stop())
    settings.DEBUG = False
    main()


def main():
    if settings.FORK:
        if settings.FORK is True:
            settings.FORK = 0
        assert not settings.DEBUG, 'Cannot run in multiprocess mode and debug mode'
        tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
        server = tornado.httpserver.HTTPServer(make_app())
        server.bind(settings.PORT, settings.HOST)
        server.start(settings.FORK)
        asyncio.get_event_loop().set_debug(settings.DEBUG)
        return tornado.ioloop.IOLoop.current().start()

    tornado.platform.asyncio.AsyncIOMainLoop().install()
    make_app().listen(settings.PORT, settings.HOST)
    asyncio.get_event_loop().set_debug(settings.DEBUG)
    return asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
