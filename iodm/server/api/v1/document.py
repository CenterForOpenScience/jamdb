import bson

from iodm.auth import Permissions
from iodm.server.api.v1.base import APIResource
from iodm.server.api.v1.collection import CollectionResource


class DocumentResource(APIResource):

    @property
    def document(self):
        return self.resource

    @property
    def collection(self):
        return self.parent.resource

    def __init__(self):
        super().__init__('document', CollectionResource)

    def load(self, document_id, request):
        return super().load(self.parent.resource.read(document_id))

    def list(self):
        return [
            document.to_json_api()
            for document in self.parent.resource.list()
            if document.permissions.get(user.uid, Permissions.NONE) & user.permissions
        ]

    def create(self, data, user):
        document = self.parent.resource.create(
            data.get('id') or str(bson.ObjectId()),
            data['attributes'],
            user.uid
        )
        return document.to_json_api()

    def delete(self, user):
        self.parent.resource.delete(self.resource.ref, user.uid)

    def replace(self, data, user):
        return self.collection.update(
            self.document.ref,
            data['attributes'],
            user.uid
        ).to_json_api()

    def update(self, data, user):
        return self.collection.update(
            self.document.ref,
            data['attributes'],
            user.uid,
            merger=lambda x, y: {**x, **y}
        ).to_json_api()
