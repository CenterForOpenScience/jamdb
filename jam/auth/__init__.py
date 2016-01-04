__import__('pkg_resources').declare_namespace(__name__)

from jam.auth.user import User
from jam.auth.permissions import Permissions

__all__ = ('User', 'Permissions')
