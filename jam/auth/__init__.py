__import__('pkg_resources').declare_namespace(__name__)

from iodm.auth.user import User
from iodm.auth.permissions import Permissions

__all__ = ('User', 'Permissions')
