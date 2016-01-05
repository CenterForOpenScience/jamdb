import os
import sys
import yaml
import logging


class _Settings:

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.load(os.path.join(os.path.dirname(__file__), 'defaults.yml'))
        try:
            self.load(os.path.join(os.path.dirname(__file__), 'local.yml'))
            self.logger.warning('local.yml loaded')
        except FileNotFoundError:
            pass

    def load(self, path):
        with open(path, 'r') as settings:
            self.update(yaml.load(settings.read()))

    def update(self, data):
        self.__dict__.update(data)

    def __getattr__(self, attr):
        raise AttributeError('No setting for "{}"'.format(attr))

sys.modules[__name__] = _Settings()
