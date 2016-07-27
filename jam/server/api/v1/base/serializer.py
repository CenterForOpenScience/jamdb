import datetime

from jam.auth import Permissions
from jam.server.api.v1.base.constants import NAMESPACER


class Serializer:
    view = None
    plugins = {}
    relations = {}

    def __init__(self, request, user, inst, *parents):
        self._user = user
        self._instance = inst
        self._request = request
        self._parents = parents
        self._permission = user.permissions

    def serialize(self):
        return {
            'id': NAMESPACER.join([p.ref or p.ref for p in self._parents] + [self._instance.ref]),
            'type': self.__class__.type,
            'meta': self.meta(),
            # 'links': cls.links(request, inst, *parents),
            'attributes': self.attributes(),
            'relationships': self.relationships()
        }

    def relationships(self):
        return {
            name: relation.serialize(self._request, self._instance, *self._parents)
            for name, relation in self.__class__.relations.items()
            if relation.included
        }

    def meta(self):
        return {
            'permissions': Permissions(self._permission).name,
            'created-by': self._instance.created_by,
            'modified-by': self._instance.modified_by,
            'created-on': datetime.datetime.fromtimestamp(self._instance.created_on).isoformat(),
            'modified-on': datetime.datetime.fromtimestamp(self._instance.modified_on).isoformat()
        }
