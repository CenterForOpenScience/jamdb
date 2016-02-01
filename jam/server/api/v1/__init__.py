from jam.server.api.v1.auth import AuthHandler
from jam.server.api.v1.base import ResourceEndpoint
from jam.server.api.v1.history import HistoryView, HistorySerializer
from jam.server.api.v1.document import DocumentView, DocumentSerializer
from jam.server.api.v1.namespace import NamespaceView, NamespaceSerializer
from jam.server.api.v1.collection import CollectionView, CollectionSerializer


ENDPOINTS = (
    ResourceEndpoint(HistoryView, HistorySerializer),
    ResourceEndpoint(DocumentView, DocumentSerializer),
    ResourceEndpoint(NamespaceView, NamespaceSerializer),
    ResourceEndpoint(CollectionView, CollectionSerializer),
)

__all__ = ('ENDPOINTS', 'AuthHandler')
