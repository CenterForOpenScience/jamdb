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

from iodm import NamespaceManager
from iodm import server
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
    context.base_url = 'http://127.0.0.1:{}'.format(port)
    context.server_thread = ServerThread(port)
    context.server_thread.start()
    context.manager = NamespaceManager()


def after_all(context):
    context.server_thread.stop()


def before_scenario(context, senario):
    context.resources = {}
    context.ignored_auth = []
