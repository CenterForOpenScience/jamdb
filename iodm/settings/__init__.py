import logging

from iodm.settings.defaults import *  # noqa

logger = logging.getLogger(__name__)

try:
    from iodm.settings.local import *  # noqa
except ImportError:
    logger.warning('No local.py found, using defaults')
