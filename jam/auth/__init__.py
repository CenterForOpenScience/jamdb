from jam.auth.user import User
from jam.auth.permissions import Permissions

PERMISSIONS_SCHEMA = {
    'type': 'object',
    'patternProperties': {
        r'^(\*|[^\s\-\*]+\-\*|[^\s\-\*]+\-[^\s\-\*]+\-\*|[^\s\-\*]+\-[^\s\-\*]+\-[^\s\-\*]+)$': {
            'type': 'integer'
        }
    },
    'additionalProperties': False,
}

__all__ = ('User', 'Permissions', PERMISSIONS_SCHEMA)
