import os
import sys
import yaml
import logging


class _Settings:

    here = os.path.join(os.path.dirname(__file__))
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.load('defaults.yml', local=True)
        self.load('local.yml', local=True, _try=True)

    def load(self, path, local=False, _try=False):
        if local:
            path = os.path.join(self.here, path)
        try:
            with open(path, 'r') as settings:
                self.update(yaml.load(settings.read()))
        except FileNotFoundError:
            if not _try:
                raise
        if _try:
            self.logger.warning('{} loaded'.format(path))

    def update(self, data):
        self.__dict__.update(data)

    def __getattr__(self, attr):
        raise AttributeError('No setting for "{}"'.format(attr))

sys.modules[__name__] = _Settings()
