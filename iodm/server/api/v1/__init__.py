from iodm.server.api.v1.document import HistoryHandler
from iodm.server.api.v1.document import DocumentHandler
from iodm.server.api.v1.document import DocumentsHandler
from iodm.server.api.v1.collection import CollectionHandler
from iodm.server.api.v1.collection import CollectionsHandler

HANDLERS = (
    HistoryHandler.as_entry(),
    DocumentHandler.as_entry(),
    DocumentsHandler.as_entry(),
    CollectionHandler.as_entry(),
    CollectionsHandler.as_entry(),
)
