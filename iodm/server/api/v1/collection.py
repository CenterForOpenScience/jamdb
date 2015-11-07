import calendar

from dateutil.parser import parse

import iodm
from iodm.backends import EphemeralBackend
from iodm.server.api.v1.base import APIResource
from iodm.server.api.v1.namespace import NamespaceResource


class CollectionResource(APIResource):

    def __init__(self):
        super().__init__('collection', NamespaceResource)

    def load(self, collection_id, request):
        collection = self.parent.resource.get_collection(collection_id)

        maybe_time = request.query_arguments.get('timemachine')
        if maybe_time:
            maybe_time = maybe_time[-1].decode('utf-8')
            try:
                timestamp = float(maybe_time)
            except ValueError:
                timestamp = calendar.timegm(parse(maybe_time).utctimetuple())

            collection = collection.at_time(
                timestamp,
                iodm.State(EphemeralBackend()),
                regenerate=False
            )

            if collection.regenerate() > 200:
                collection.snapshot()

        return super().load(collection)

    def list(self):
        return list(self.parent.resource.keys())

    def read(self):
        return self.resource.to_json_api()
