from iodm.server.api.base import BaseAPIHandler


class CollectionsHandler(BaseAPIHandler):
    PATTERN = '/collections/?'

    def initialize(self, namespacer):
        self.namespacer = namespacer

    def get(self):
        self.write({
            'data': list(self.namespacer.keys())
        })


class CollectionHandler(BaseAPIHandler):
    PATTERN = '/collections/(?P<collection_id>\w+)/?'

    def initialize(self, namespacer):
        self.namespacer = namespacer

    def get(self, collection_id):

        data = list(self.namespacer.get_collection(collection_id).list())

        self.write({
            'data': list(self.namespacer.get_collection(collection_id).list())
        })
