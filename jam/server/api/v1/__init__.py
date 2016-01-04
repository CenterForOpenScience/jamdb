from jam.server.api.v1.auth import AuthHandler  # noqa
from jam.server.api.v1.search import SearchResource
from jam.server.api.v1.history import HistoryResource
from jam.server.api.v1.document import DocumentResource
from jam.server.api.v1.namespace import NamespaceResource
from jam.server.api.v1.collection import CollectionResource


RESOURCES = (
    NamespaceResource,
    CollectionResource,
    SearchResource,
    DocumentResource,
    HistoryResource,
)
