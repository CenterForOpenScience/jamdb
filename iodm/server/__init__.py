import asyncio
import logging

import tornado.web
import tornado.platform.asyncio

from iodm import Namespace
from iodm.server.api import v1


logger = logging.getLogger(__name__)


async def make_app(debug=True):
    endpoints = []

    for endpoint in v1.RESOURCES:
        endpoint = endpoint.as_handler_entry()
        endpoints.append(endpoint)
        logger.info('Loaded {} endpoint "{}"'.format(v1.__name__, endpoint[0]))

    return tornado.web.Application(endpoints, debug=debug)


def profile(ktime=10):
    asyncio.get_event_loop().call_later(ktime, lambda: asyncio.get_event_loop().stop())
    main(debug=False)


def main(debug=True):
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    app = asyncio.get_event_loop().run_until_complete(make_app(debug))

    app.listen(1212, '127.0.0.1')

    asyncio.get_event_loop().set_debug(debug)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
