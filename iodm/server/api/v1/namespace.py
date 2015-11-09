from iodm import NamespaceManager
from iodm.auth import Permissions
from iodm.server.api.v1.base import APIResource


manager = NamespaceManager()


class NamespaceResource(APIResource):

    @property
    def namespace(self):
        return self.resource

    def __init__(self):
        super().__init__('namespace')

    def get_permissions(self, request):
        return Permissions.ADMIN

    def load(self, namespace_id, request):
        return super().load(manager.get_namespace(namespace_id))

    def read(self, user):
        return {
            'id': self.namespace.name,
            'type': 'namespace',
            'attributes': {
                'name': self.namespace.name,
                'permissions': self.namespace.permissions
            },
            # 'links': {'self': url}
        }
