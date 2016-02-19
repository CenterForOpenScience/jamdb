# Notes:
* ids are must match the regex [\d\w\-]{3,64}

`/v1/namespaces`
`/v1/namespaces/<namespace_id>`
`/v1/namespaces/<namespace_id>/collections`
`/v1/namespaces/<namespace_id>/collections/<collection_id>`
`/v1/namespaces/<namespace_id>/collections/<collection_id>/_search`
`/v1/namespaces/<namespace_id>/collections/<collection_id>/documents`
`/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>`
`/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>/history`
`/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>/history/<history_id>`

`/v1/id/namespaces`
`/v1/id/namespaces/<namespace_id>`
`/v1/id/namespaces/<namespace_id>/collections`
`/v1/id/collections/<namespace_id>.<collection_id>`
`/v1/id/collections/<namespace_id>.<collection_id>/_search`
`/v1/id/collections/<namespace_id>.<collection_id>/documents`
`/v1/id/documents/<namespace_id>.<collection_id>.<document_id>`
`/v1/id/documents/<namespace_id>.<collection_id>.<document_id>/history`
`/v1/id/history/<namespace_id>.<collection_id>.<document_id>.<history_id>`
