# JamDB API interface

## Routes
* `/v1/auth`
* `/v1/namespaces`
* `/v1/namespaces/<namespace_id>`
* `/v1/namespaces/<namespace_id>/collections`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/_search`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>/history`
* `/v1/namespaces/<namespace_id>/collections/<collection_id>/documents/<document_id>/history/<history_id>`

### Route Caveats
* All elements wrapped in `<>` are matched by the regex `[\d\w\.\-]{3,64}`
    - Valid characters being `0-9 a-z A-Z . -`
* templates ids ARE case sensitive
* Trailing slashes `/` are optional


## API Overview
JamDB follows the [JSONAPI standard](http://jsonapi.org/)

All responses will be formatted as:
```json
{
    "id": "resource id",
    "type": "namespaces|collections|documents|history",
    "attributes": {
    },
    "meta": {
        "created-by": "<creator_id>",
        "modified-by": "<modifier_id>",
        "created-on": "ISO8601 UTC date",
        "modifed-on": "ISO8601 UTC date"
    },
    "relationships": {
        "<related_resource_name>": {
            "self": "url",
            "related": "url",
        }
    }
}
```

### Permissions
Permission levels are represented as powers of 2

| Permission | power | number |
| :--: | :--: | :--: |
| None | N/A | 0 |
| Create | 1 | 2 |
| Read | 2 | 4 |
| Update | 3 | 8 |
| Delete | 4 | 16 |
| Admin | 63 | 9223372036854775807 |

Permissions can be combined via a bitwise OR

`READ_WRITE = CREATE | READ | UPDATE`

`CRUD = READ_WRITE | DELETE`

A permissions object is a hash/dictionary where the key is a selector and the value is the given permission

A selector is the same patten as a user id, the pattern can be terminated early by the wild card character `*`

Valid selectors are:

`*`

`{user_type}-*`

`{user_type}-{provider}-*`

`{user_type}-{provider}-{user_id}`


Permissions are gathered from the current resource being accessed and all its parents and then or'ed together to receive the final permission level.


### Resources

#### Namespaces
Required fields for creation: [`name`]

Fields that may be updated: [`name`, `permissions`]

```json
{
    "name": "",
    "permissions": {},
}
```

#### Collection
Required fields for creation: [`name`]

Fields that may be updated: [`name`, `permissions`]

```json
{
    "name": "",
    "permissions": {},
    "state": "",
    "logger": "",
    "storage": "",
}
```


#### Document
The attributes of documents are completely free form.

The only requirements are that `id` must match the same regex as the url
