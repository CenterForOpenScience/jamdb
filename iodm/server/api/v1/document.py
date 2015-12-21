import bson
import operator
import functools
import datetime

import iodm
from iodm.auth import Permissions
from iodm.server.api.v1.base import APIResource
from iodm.server.api.v1.collection import CollectionResource


class DocumentResource(APIResource):

    PAGE_SIZE = 50

    @classmethod
    def serialize(cls, document, request):
        # TODO Feel less bad about this
        namespace_id = request.path.split('/')[3]
        collection_id = request.path.split('/')[5]
        return {
            'id': document.ref,
            'type': 'documents',
            'attributes': document.data,
            'meta': {
                'created-by': document.created_by,
                'modified-by': document.modified_by,
                'created-on': datetime.datetime.fromtimestamp(document.created_on).isoformat(),
                'modified-on': datetime.datetime.fromtimestamp(document.created_on).isoformat()
            },
            'relationships': {
                'namespace': {
                    'links': {
                        'self': '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace_id),
                        'related': '{}://{}/v1/namespaces/{}'.format(request.protocol, request.host, namespace_id),
                    }
                },
                'collection': {
                    'links': {
                        'self': '{}://{}/v1/namespaces/{}/collections/{}'.format(request.protocol, request.host, namespace_id, collection_id),
                        'related': '{}://{}/v1/namespaces/{}/collections/{}'.format(request.protocol, request.host, namespace_id, collection_id),
                    }
                },
                'history': {
                    'links': {
                        'self': '{}://{}/v1/namespaces/{}/collections/{}/documents/{}/history'.format(request.protocol, request.host, namespace_id, collection_id, document.ref),
                        'related': '{}://{}/v1/namespaces/{}/collections/{}/documents/{}/history'.format(request.protocol, request.host, namespace_id, collection_id, document.ref),
                    }
                }
            }
        }

    @property
    def document(self):
        return self.resource

    @property
    def collection(self):
        return self.parent.resource

    # @property
    # def name(self):
    #     return self.collection.name

    def __init__(self):
        super().__init__('document', CollectionResource)

    def get_permissions(self, request):
        if request.method == 'GET' and self.resource is None:
            return Permissions.NONE
        return super().get_permissions(request)

    def load(self, document_id, request):
        return super().load(self.parent.resource.read(document_id))

    # CRUD-LR

    def create(self, data, user):
        return self.collection.create(
            data.get('id') or str(bson.ObjectId()),
            data['attributes'],
            user.uid
        )

    def read(self, user):
        return self.document

    def update(self, data, user):
        return self.collection.update(
            self.document.ref,
            data['attributes'],
            user.uid,
            merger=lambda x, y: {**x, **y}
        )

    def delete(self, user):
        self.collection.delete(self.resource.ref, user.uid)

    def replace(self, data, user):
        return self.collection.update(
            self.document.ref,
            data['attributes'],
            user.uid
        )

    def list(self, user, page=0, filter=None):
        selector = self.collection.select().order_by(
            iodm.O.Ascending('ref')
        ).page(page, self.PAGE_SIZE)

        if not user.permissions & Permissions.READ:
            filter['created_by'] = user.uid

        if not filter:
            query = None
        else:
            query = functools.reduce(operator.and_, [
                iodm.Q(key, 'eq', value)
                for key, value in
                filter.items()
            ])

        return selector.where(query)
