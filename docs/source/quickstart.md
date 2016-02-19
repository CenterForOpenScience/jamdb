# Getting Started
Please note: This documentation is a work in progress.

Further examples can be found in the [features directory.](features/)

This tutorial assumes that the JamDB server you're interacting with will be
at `http://localhost:1212`. It also assumes access to a terminal shell on
either OSX or Linux with the `curl` command installed and executable.

## Namespace
To start using JamDB, you will need a namespace. A namespace is the
equivalent of a database in MongoDB or PostgreSQL.

It will act as a top-level container for any collections you make and store
permissions that apply to itself and cascade to anything inside of it.

Administrator privileges are required to make any modification to a
namespace.

### Creating a namespace
Currently, there is no way to create a namespace through the API. If you're
working with a remote instance of JamDB, contact the server administrator
to create a namespace. If you're running a local instance of JamDB, you can
create a namespace by running `jam create <namespace id> -u
'jam-ProgrammingLanguages:Programmers-Ash`.

> We'll be using `ProgrammingLanguages` as the example namespace id for the
rest of this document. Namespace ids are case-sensitive.

Once your namespace is setup, you'll need to send the proper
`Authorization` header to access it.

### Authorizing against a namespace
JamDB uses [json web tokens](https://jwt.io), JWT for short, in the
`Authorization` header or the `token` query string parameter.

There are three ways to acquire a JWT:

1. Contact the server administrator and request a temporary token.
2. Authenticate via the [Auth Endpoint](authentication.md)
3. If you are running a JamDB server locally you can generate a token by
running `jam token 'jam-ProgrammingLanguages:Programmers-Ash'`

> We'll be using `mycooljwt` as the example JWT for the rest of this
document.


### Investigating a namespace
You can get information about your namespace by making an HTTP request
using [curl](https://en.wikipedia.org/wiki/CURL), [Paw](
https://luckymarmot.com/paw), or a similar program.

__HTTP Request:__

```http
GET /v1/namespaces/ProgrammingLanguages HTTP/1.1
Authorization: mycooljwt
```

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages",
    "type": "namespaces",
    "attributes": {
      "name": "ProgrammingLanguages",
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN"
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

> Permissions may be different depending on how you got your JWT.

Let's say we want all of our programmer friends to have read access to all
of our ProgrammingLanguages data.

We can update our namespace in two ways.

We can use [jsonpatch](http://jsonpatch.com/) to add just the field we want.

__HTTP Request:__

```http
PATCH /v1/namespaces/ProgrammingLanguages HTTP/1.1
Authorization: mycooljwt
Content-Type: Content-Type: application/vnd.api+json; ext=jsonpatch

[{"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-*", "value": "READ"}]
```

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages",
    "type": "namespaces",
    "attributes": {
      "name": "ProgrammingLanguages",
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-*": "READ",
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN"
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

Many jsonpatch objects may be sent at once.

__HTTP Request:__

```http
PATCH /v1/namespaces/ProgrammingLanguages HTTP/1.1
Authorization: mycooljwt
Content-Type: Content-Type: application/vnd.api+json; ext=jsonpatch

[
  {"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-*", "value": "READ"},
  {"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-Misty", "value": "ADMIN"},
  {"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-Brock", "value": "ADMIN"}
]
```

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages",
    "type": "namespaces",
    "attributes": {
      "name": "ProgrammingLanguages",
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-*": "READ",
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN",
        "jam-ProgrammingLanguages:Programmers-Misty": "ADMIN",
        "jam-ProgrammingLanguages:Programmers-Brock": "ADMIN",
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```


Or we can just PATCH up our updated data and let the JamDB server figure it
out.

__HTTP Request:__

```http
PATCH /v1/namespaces/ProgrammingLanguages HTTP/1.1
Authorization: mycooljwt

{
  "data": {
    "id": "ProgrammingLanguages",
    "type": "namespaces",
    "attributes": {
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-*": "READ",
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN"
      }
    }
  }
}
```

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages",
    "type": "namespaces",
    "attributes": {
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-*": "READ",
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN"
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

## Collections
Now that we've set up our namespace, it's time to create collections.

A collection is a bucket for arbitrary data. It __may__ enforce a schema on
its data. It also __may__ extend the permissions of the namespace.

### Creating a collection
To create a collection we just have to POST the data about our collection
to our namespace's collections endpoint.

__HTTP Request:__

```http
POST /v1/namespaces/ProgrammingLanguages/collections HTTP/1.1
Authorization: mycooljwt

{
  "id": "Functional",
  "type": "collections",
  "attributes": {}
}
```

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages.Functional",
    "type": "collections",
    "attributes": {
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN"
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

> __Please Note__:
>
> - We have been given ADMIN access to this collection because we created
it.
> - The id has been extended to `ProgrammingLanguages.Functional` because
the `Functional` collection belongs to the `ProgrammingLanguages` namespace.
> - The full id (`ProgrammingLanguages.Functional`) or the truncated id
(`Functional`) may be used when sending update requests.
> - The truncated id will be used for the rest of this document.

Now our fellow programmers are free to browse through the Functional
collection, which we will add information into later.

It's a lot of work to load all this data into our collection by ourselves.
Let's get some help!

### Adding collection permissions
We want to give a couple of our friends access to insert data into this
collection but we don't want to grant them access to all of our collection.

Using collection-level permissions, we can do just that.

Collections can be updated the same way that namespace are, either POSTing
or PATCHing data.
> __Please note:__
>
> - The JSONPatching format is a bit nicer to look at
so we'll be using that method for the rest of this document.<br>
> - Keep in mind that you could just as easily PATCH the updated document
instead.

```http
PATCH /v1/namespaces/ProgrammingLanguages/collections/Functional HTTP/1.1
Authorization: mycooljwt

[
  {"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-Gary", "value": "CREATE, UPDATE"},
  {"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-ProfessorOak", "value": "CREATE, UPDATE"},
  {"op": "add", "path": "/permissions/jam-ProgrammingLanguages:Programmers-ProfessorBirch", "value": "CREATE, UPDATE"}
]
```

```javascript
{
  "data": {
    "id": "ProgrammingLanguages.Functional",
    "type": "collections",
    "attributes": {
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN",
        "jam-ProgrammingLanguages:Programmers-Gary": "CU",
        "jam-ProgrammingLanguages:Programmers-ProfessorOak": "CU",
        "jam-ProgrammingLanguages:Programmers-ProfessorBirch": "CU"
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

> __Please note__:
>
> - Our permissions got compressed from CREATE, UPDATE to CU. This is the
format JamDB stores permissions. CREATE, UPDATE and CU are equivalent. We
could have set Gary's, Professor Oak's, and Professor Birch's permissions
to CU but CREATE, UPDATE is a bit easier to read.
> - Remember that we gave `jam-ProgrammingLanguages:Programmers-*` READ
permissions earlier.
> - Whenever Gary, Professor Oak, or Professor Birch access the Functional
collection they will have that permission added to their CREATE, UPDATE
permissions.

While we trust our friends, we may want to enforce data validation.

We are going to leverage the power of [JSONSchema](http://json-schema.org)
and JamDB's schema validation for this.

> Note: For the sake of length and readability we are going to use an
abbreviated schema. The actual Functional schema is much longer because
we're huge nerds.

__HTTP Request:__

```http
PATCH /v1/namespaces/ProgrammingLanguages/collections/Functional HTTP/1.1
Authorization: mycooljwt

[
  {
    "op": "add",
    "path": "/schema",
    "value": {
      "type": "jsonschema",
      "schema": {
        "id": "/",
        "type": "object",
        "properties": {
          "name": {
            "id": "name",
            "type": "string"
          },
          "type": {
            "id": "type",
            "type": "string"
          },
          "Number": {
            "id": "Number",
            "type": "integer"
          },
          "Interpreted": {
            "id": "Interpreted",
            "type": "boolean"
          }
        },
        "required": [
          "name",
          "type",
          "Number",
          "Interpreted"
        ]
      }
    }
  }
]
```

> __Please Note:__
>
> - `schema.type` must be set to the type of the schema. The actual schema
lives at `schema.schema`. This is so that JamDB may support other forms of
schema validation in the future. Currently JSONSchema is the only supported
validator.
> - `$` are illegal in JamDB key names.
> - Make sure not to use `$schema` or `$ref` in your JSONSchema.

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages.Functional",
    "type": "collections",
    "attributes": {
      "permissions": {
        "jam-ProgrammingLanguages:Programmers-Ash": "ADMIN",
        "jam-ProgrammingLanguages:Programmers-Gary": "CU",
        "jam-ProgrammingLanguages:Programmers-ProfessorOak": "CU",
        "jam-ProgrammingLanguages:Programmers-ProfessorBirch": "CU"
      },
      "schema": {
        "type": "jsonschema",
        "schema": {
          "id": "/",
          "type": "object",
          "properties": {
            "type": {
              "id": "type",
              "type": "string"
            },
            "Number": {
              "id": "Number",
              "type": "integer"
            },
            "Interpreted": {
              "id": "Interpreted",
              "type": "boolean"
            }
          },
          "required": [
            "name",
            "type",
            "Number",
            "Interpreted"
          ]
        }
      }
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

## Documents

A document is any **JSON object** with a string identifier that lives in a
collection.

> Strings, numbers, and arrays are all valid JSON but the root of a
document must be a JSON object.

Time for the fun part: Filling out the functional collection!

### Creating Documents
Document are created like anything else: by POSTing to functional
collection's documents endpoint.

__HTTP Request:__

```http
POST /v1/namespaces/ProgrammingLanguages/collections/Functional/documents HTTP/1.1
Authorization: mycooljwt

{
  "data": {
    "id": "Clojure",
    "type": "documents",
    "attributes": {
      "Number": 35,
      "Interpreted": true,
      "type": "JVM"
    }
  }
}
```

__HTTP Response:__

```javascript
{
  "data": {
    "id": "ProgrammingLanguages.Functional.Clojure",
    "type": "documents",
    "attributes": {
      "Number": 35,
      "Interpreted": true,
      "type": "JVM"
    },
    "meta": {/*...*/},
    "relationships": {/*...*/}
  }
}
```

For this next portion, we're going to assume that our friends have filled
out the rest of the Functional collection for us. Such nice friends.

## Filtering, Pagination, and Sorting

Now that we have all our data loaded up, let's search it. We'll start with
finding all entries of the type `JVM`.

### Filtering
> - Filtering is available on the `documents` endpoint
> - The query string parameter is `filter[{key}]={value}`
> - `{key}` is the key that you want to filter on
> - `{value}` is the value that you want to filter the key by
> - `.`s are used to separate keys when referring to a nested object,
`filter[nested.keys.like.this]=value`

### Page size
> - To save space we'll be using a page size of 2
> - Page size may be anywhere between 0 and 100, inclusive, and defaults to
50
> - The query string parameter is `page[size]={value}`

__HTTP Request:__

```http
GET /v1/namespaces/ProgrammingLanguages/collections/Functional/documents?filter[type]=JVM&page[size]=2 HTTP/1.1
Authorization: mycooljwt
```

__HTTP Response:__

```javascript
{
  "data": [
    {
      "id": "ProgrammingLanguages.Functional.Clojure",
      "type": "documents",
      "attributes": {
        "Number": 35,
        "Interpreted": true,
        "type": "JVM"
      },
      "meta": {/*...*/},
      "relationships": {/*...*/}
    }, {
      "id": "ProgrammingLanguages.Functional.Haskell",
      "type": "documents",
      "attributes": {
        "Number": 60,
        "Interpreted": false,
        "type": "native"
      },
      "meta": {/*...*/},
      "relationships": {/*...*/}
    },
  ],
  "links": {/*...*/}
}
```
### Sorting
Next let's find the entry with the highest Number that is an JVM type.

This can be achieved by filtering on type and then sorting on Number.

> __Please note:__
>
> - Sorts may be done ascending or descending by prefixing the key you wish
to sort on with `+` or `-`, respectively
> - Sort order defaults to ascending
> - Sort defaults to id
> - If you want to sort on id, descending use `sort=-ref`. This is subject
to change
> - The query string parameter is `sort={order}{value}`

__HTTP Request:__

```http
GET /v1/namespaces/ProgrammingLanguages/collections/Functional/documents?filter[type]=JVM&page[size]=1&sort=Number HTTP/1.1
Authorization: mycooljwt
```

__HTTP Response:__

```javascript
{
  "data": [
    {
      "id": "ProgrammingLanguages.Functional.Elixir",
      "type": "documents",
      "attributes": {
        "Number": 90,
        "Interpreted": false,
        "type": "erlang"
      },
      "meta": {/*...*/},
      "relationships": {/*...*/}
    }
  ],
  "links": {/*...*/}
}
```

## Searching
Finally, Gary is trying to remember the id of a specific entry but only
remembers that is ends with "oq"

What an excellent opportunity for us to tap into JamDB's [Elastic Search](
https://www.elastic.co/products/elasticsearch) API.

> __Please note:__
>
> - The power of elasticsearch's [query string syntax](
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax)
is exposed as the `q` query string parameter on the _search endpoint.
> - In accordance with the other query string parameters, to query the id
of a document use the `ref` key instead of id.
> - The query string parameter is `q={url_escaped_elasticsearch_query}`

__HTTP Request:__

```http
GET /v1/namespaces/ProgrammingLanguages/collections/Functional/documents?q=ref:*oq  HTTP/1.1
Authorization: mycooljwt
```

__HTTP Response:__

```javascript
{
  "data": [
    {
      "id": "ProgrammingLanguages.Functional.Coq",
      "type": "documents",
      "attributes": {
        "Number": 106,
        "Interpreted": true,
        "type": "OCaml"
      },
      "meta": {/*...*/},
      "relationships": {/*...*/}
    }
  ],
  "links": {/*...*/}
}
```
