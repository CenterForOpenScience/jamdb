__import__('pkg_resources').declare_namespace(__name__)

from iodm.backends import Q
from iodm.backends import O
from iodm.state import State
from iodm.logger import Logger
from iodm.storage import Storage
from iodm.namespace import Namespace
from iodm.collection import Collection
from iodm.manager import NamespaceManager

from iodm.util import logging  # noqa

__version__ = '0.0.0'

__all__ = (
    'Q',
    'O',
    'Logger',
    'Storage',
    'State',
    'Collection',
    'Namespace',
    'NamespaceManager',
    '__version__',
)
