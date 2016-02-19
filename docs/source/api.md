# API Semantics

# Notes:
* ids are must match the regex [\d\w\-]{3,64}

## Routes list
* `/v1/namespaces`
* `/v1/namespaces/<namespace_id>`
* `/v1/namespaces/<namespace_id>/collections`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/_search`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>/history`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>/history/<history_id>`
* `/v1/id/namespaces`
* `/v1/id/namespaces/<namespace_id>`
* `/v1/id/namespaces/<namespace_id>/collections`
* `/v1/id/collections/<namespace_id>.<collection_id>`
* `/v1/id/collections/<namespace_id>.<collection_id>/_search`
* `/v1/id/collections/<namespace_id>.<collection_id>/documents`
* `/v1/id/documents/<namespace_id>.<collection_id>.<document_id>`
* `/v1/id/documents/<namespace_id>.<collection_id>.<document_id>/history`
* `/v1/id/history/<namespace_id>.<collection_id>.<document_id>.<history_id>`


## Extensions

### JSONPatch

JamDB implements JSONAPI's jsonpatch extension as described [here.](http://jsonapi.org/extensions/jsonpatch/)

Example payloads and responses may be seen [here](/features/document/update.feature), [here](/features/namespace/update.feature), or [here](/features/collection/update.feature).

#### Deviations
JSONPatch operations other than updating a single document are not currently supported.


### Bulk

JamDB implements JSONAPI's bulk extension as described [here](http://jsonapi.org/extensions/bulk/).

Example payloads and responses may be seen [here](/features/document/create.feature).

#### Deviations
Bulk deletes are not currently supported.

Bulk operations are not transactional.
If a document creation fails for any reason it will not impede the creation of other documents.
The failure will be returned in the `errors` key of the response json corrosponding to its index in the POSTed `data` field.
The behavior is demonstrated [here](/features/document/create.feature).
