from jam import settings
# Hack to force all storages into memory
settings.load('test.yml', local=True)
settings.load('test-local.yml', local=True, _try=True)

import asyncio
import logging
import requests
import threading
import time

from jam import NamespaceManager
from jam import server
from jam.backends.ephemeral import EphemeralBackend
import jam


class ServerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()

    def run(self):
        logger = logging.getLogger(jam.__name__)
        logger.setLevel(logging.ERROR)
        logging.getLogger('tornado.access').setLevel(logging.FATAL)
        asyncio.set_event_loop(self.loop)
        server.main()

    def stop(self):
        self.loop.call_soon_threadsafe(lambda: self.loop.stop())
        self.join()
        self.loop.close()


def before_all(context):
    logger = logging.getLogger(requests.__name__)
    logger.setLevel(logging.ERROR)
    context.base_url = 'http://localhost:{}'.format(settings.PORT)
    context.server_thread = ServerThread()
    context.server_thread.start()
    for _ in range(5):
        try:
            requests.get(context.base_url)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(5)
    else:
        raise Exception('Unable to connect to testing server at {}'.format(context.base_url))


def after_all(context):
    context.server_thread.stop()


def before_scenario(context, senario):
    context.resources = {
        'namespace': {},
        'collection': {},
        'document': {},
    }
    context.system_auth = []
    context.ignored_auth = []
    for v in EphemeralBackend._cls_cache.values():
        v.clear()

    context.mocks = {}
    context.patches = {}
    context.manager = NamespaceManager()


def after_scenario(context, scenario):
    if hasattr(context, 'time'):
        context.time.stop()

    for patcher in context.patches.values():
        patcher.stop()
