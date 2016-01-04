from iodm.server.api.v1.auth import AuthHandler  # noqa
from iodm.server.api.v1.search import SearchResource
from iodm.server.api.v1.history import HistoryResource
from iodm.server.api.v1.document import DocumentResource
from iodm.server.api.v1.namespace import NamespaceResource
from iodm.server.api.v1.collection import CollectionResource


RESOURCES = (
    NamespaceResource,
    CollectionResource,
    SearchResource,
    DocumentResource,
    HistoryResource,
)
