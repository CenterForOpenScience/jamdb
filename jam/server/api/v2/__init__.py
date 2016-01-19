from jam.server.api.v2.base import ResourceEndpoint
from jam.server.api.v2.history import HistoryView, HistorySerializer
from jam.server.api.v2.document import DocumentView, DocumentSerializer
from jam.server.api.v2.namespace import NamespaceView, NamespaceSerializer
from jam.server.api.v2.collection import CollectionView, CollectionSerializer


ENDPOINTS = (
    ResourceEndpoint(HistoryView, HistorySerializer),
    ResourceEndpoint(DocumentView, DocumentSerializer),
    ResourceEndpoint(NamespaceView, NamespaceSerializer),
    ResourceEndpoint(CollectionView, CollectionSerializer),
)
