import asyncio
import logging

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.platform.asyncio

from jam import settings
from jam.server.api import v1
from jam.server.api.base import Default404Handler


logger = logging.getLogger(__name__)


def make_app():
    endpoints = [
        ('/v1/auth/?', v1.AuthHandler)
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
        debug=settings.DEBUG,
        default_handler_class=Default404Handler,
    )


def profile(ktime=10):
    asyncio.get_event_loop().call_later(ktime, lambda: asyncio.get_event_loop().stop())
    settings.DEBUG = False
    main()


def main():
    app = make_app()

    if settings.FORK:
        if settings.FORK is True:
            settings.FORK = 0
        tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
        server = tornado.httpserver.HTTPServer(app)
        server.bind(settings.PORT, settings.HOST)
        server.start(settings.FORK)
        asyncio.get_event_loop().set_debug(settings.DEBUG)
        tornado.ioloop.IOLoop.current().start()

    tornado.platform.asyncio.AsyncIOLoop().install()
    app.listen(settings.PORT, settings.HOST)
    asyncio.get_event_loop().set_debug(settings.DEBUG)
    return asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
