import logging

from jam.settings.defaults import *  # noqa

logger = logging.getLogger(__name__)

try:
    from jam.settings.local import *  # noqa
except ImportError:
    logger.warning('No local.py found, using defaults')
