__import__('pkg_resources').declare_namespace(__name__)

from jam.backends import Q
from jam.backends import O
from jam.state import State
from jam.logger import Logger
from jam.storage import Storage
from jam.namespace import Namespace
from jam.collection import Collection
from jam.manager import NamespaceManager

from jam.util import logging  # noqa

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
