from iodm import Namespace
from iodm.server.api.v1.base import APIResource


class NamespaceResource(APIResource):

    def __init__(self):
        super().__init__('namespace')

    def load(self, namespace_id, request):
        return super().load(Namespace(namespace_id))

    def read(self):
        namespace = self.resource
        return {
            'id': namespace.name,
            'type': 'namespace',
            'attributes': {
                'name': namespace.name,
                'permissions': namespace.permissions
            },
            # 'links': {'self': url}
        }
