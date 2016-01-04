from iodm import settings
# Hack to force all storages into memory

settings.NAMESPACE_BACKENDS = {
    'state': 'ephemeral',
    'logger': 'ephemeral',
    'storage': 'ephemeral',
}
settings.NAMESPACE_DEFAULT_BACKENDS = {
    'state': 'ephemeral',
    'logger': 'ephemeral',
    'storage': 'ephemeral',
}
settings.NAMESPACEMANAGER_BACKENDS = {
    'state': 'ephemeral',
    'logger': 'ephemeral',
    'storage': 'ephemeral',
}
import asyncio
import logging
import requests
import threading
import time

from iodm import NamespaceManager
from iodm import server
from iodm.backends import EphemeralBackend
import iodm


class ServerThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.loop = asyncio.new_event_loop()

    def run(self):
        logger = logging.getLogger(iodm.__name__)
        logger.setLevel(logging.ERROR)
        asyncio.set_event_loop(self.loop)
        server.main(debug=False, port=self.port)

    def stop(self):
        self.loop.call_soon_threadsafe(lambda: self.loop.stop())
        self.join()
        self.loop.close()


def before_all(context):
    port = 50325
    logger = logging.getLogger(requests.__name__)
    logger.setLevel(logging.ERROR)
    context.base_url = 'http://localhost:{}'.format(port)
    context.server_thread = ServerThread(port)
    context.server_thread.start()
    for _ in range(5):
        try:
            requests.get(context.base_url)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1000)
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
    context.ignored_auth = []
    for v in EphemeralBackend._cls_cache.values():
        v.clear()
    context.manager = NamespaceManager()


def after_scenario(context, scenario):
    if hasattr(context, 'time'):
        context.time.stop()
