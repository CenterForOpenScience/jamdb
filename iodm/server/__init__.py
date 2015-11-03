import asyncio

import tornado.web
import tornado.platform.asyncio

from iodm import Namespace
from iodm.server.api import v1


async def make_app(debug=True):
    namespacer = Namespace('Testing')

    return tornado.web.Application([
        (*entry, {'namespacer': namespacer})
        for entry in v1.HANDLERS
    ], debug=debug)


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
