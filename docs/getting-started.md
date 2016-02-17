# Getting Started
Please note: These docs are still in progress. If something doesn't look quite right it's probably wrong.

Further examples can be found but in the [features directory.](features/)

This tutorial assumes that the JamDB server you're interacting with will be at `http://localhost:1212`.

## Namespace
To start using JamDB, you will need a namespace. A namespace is the equivalent of a database in MongoDB or PostgreSQL.

It will act as a container for any collections you make and store permissions that apply to itself and anything inside of it.

Administrator privileges are required to make any modification to a namespace.

Currently there is no way to create a namespace through the API. If you're working with a remote instance of JamDB contact the server administrator to set up a namespace for you. If you're running a local instance of JamDB you can create a namespace by running `jam create <namespace id> -u 'jam-Pokemon:Trainers-Ash`.

> We'll be using `Pokemon` as the namespace id for the rest of this document.

Once your namespace is setup you'll need to send the proper `Authorization` header to access it.

Jam uses [json web tokens](https://jwt.io), jwt for short, in the `Authorization` header or the `token` query parameter.

There are 3 ways to acquire a jwt.
1. Contact the server admin and request a temporary token.
2. Generate a token by running `jam token 'jam-Pokemon:trainers-Ash'`
  - This will only work if you are running JamDB locally

3. Authenticate via the [Auth Endpoint](docs/authentication.md)

> We'll be using `mycooljwt` as the jwt for the rest of this document.

You can get information about your namespace by running this command in a bash shell

```http
GET /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt
```

```json
{
  "data": {
    "id": "Pokemon",
    "type": "namespaces",
    "attributes": {
      "name": "Pokemon",
      "permissions": {
        "jam-Pokemon:Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

> Permissions may be different depending on how you got your jwt.

Let's say we want all our trainer friends to have read access to all our pokemon data.

We can update our namespace in two ways.

We can use [jsonpatch](http://jsonpatch.com/) to add just the field we want.

```http
PATCH /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt
Content-Type: Content-Type: application/vnd.api+json; ext=jsonpatch

[{"op": "add", "path": "/permissions/jam-Pokemon:Trainers-*", "value": "READ"}]
```

```json
{
  "data": {
    "id": "Pokemon",
    "type": "namespaces",
    "attributes": {
      "name": "Pokemon",
      "permissions": {
        "jam-Pokemon:Trainers-*": "READ",
        "jam-Pokemon:Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

Many jsonpatch objects may be sent at once.

```http
PATCH /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt
Content-Type: Content-Type: application/vnd.api+json; ext=jsonpatch

[
  {"op": "add", "path": "/permissions/jam-Pokemon:Trainers-*", "value": "READ"},
  {"op": "add", "path": "/permissions/jam-Pokemon:Trainers-Misty", "value": "ADMIN"},
  {"op": "add", "path": "/permissions/jam-Pokemon:Trainers-Brock", "value": "ADMIN"}
]
```

```json
{
  "data": {
    "id": "Pokemon",
    "type": "namespaces",
    "attributes": {
      "name": "Pokemon",
      "permissions": {
        "jam-Pokemon:Trainers-*": "READ",
        "jam-Pokemon:Trainers-Ash": "ADMIN",
        "jam-Pokemon:Trainers-Misty": "ADMIN",
        "jam-Pokemon:Trainers-Brock": "ADMIN",
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

Or we can just PATCH up our updated data and let the JamDB server figure it out.

```http
PATCH /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt

{
  "data": {
    "id": "Pokemon",
    "type": "namespaces",
    "attributes": {
      "permissions": {
        "jam-Pokemon:Trainers-*": "READ",
        "jam-Pokemon:Trainers-Ash": "ADMIN"
      }
    }
  }
}
```

```json
{
  "data": {
    "id": "Pokemon",
    "type": "namespaces",
    "attributes": {
      "permissions": {
        "jam-Pokemon:Trainers-*": "READ",
        "jam-Pokemon:Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

## Collections
Now that we've set up our namespace it's time to create collections.

A collection is a bucket for arbitrary data to live in. It may enforce a schema on its data. It also may extend the permissions of the namespace.

To create a collection we just have to POST our data to our namespace's collections endpoint.

```http
POST /v1/namespaces/Pokemon/collections
Authorization: mycooljwt

{
  "id": "Pokedex",
  "type": "collections",
  "attributes": {}
}
```

```json
{
  "data": {
    "id": "Pokemon.Pokedex",
    "type": "collections",
    "attributes": {
      "permissions": {
        "jam-Pokemon:Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

> Note: we have been given ADMIN access to this collection because we created it.

> Note: The id has been extended to Pokemon.Pokedex because Pokedex belongs to Pokemon.
> The full id or the truncated id may be used when sending update requests.
> The truncated id will be used for the rest of this document.

Now our fellow trainers are free to browse through the Pokedex collection, which we will add information into later.

It's a lot of work to load all this data into our collection by ourselves. Let's get some help!

We want to give a couple of our friends access to insert data into this collection but we don't want to grant them access to all of our collection.

Using collection level permissions, we can do just that.

Collections can be updated the same way that namespace are, either POSTing or PATCHing data.

> JSONPatching changes is a bit nicer to look at so we'll be using that method for the rest of this document.
> Keep in mind that you could just as easily PATCH the updated document instead.

```http
PATCH /v1/namespaces/Pokemon/collections/Pokedex
Authorization: mycooljwt

[
  {"op": "add", "path": "/permissions/jam-Pokemon:Trainers-Gary", "value": "CREATE, UPDATE"},
  {"op": "add", "path": "/permissions/jam-Pokemon:Trainers-ProfessorOak", "value": "CREATE, UPDATE"},
  {"op": "add", "path": "/permissions/jam-Pokemon:Trainers-ProfessorBirch", "value": "CREATE, UPDATE"}
]
```

```json
{
  "data": {
    "id": "Pokemon.Pokedex",
    "type": "collections",
    "attributes": {
      "permissions": {
        "jam-Pokemon:Trainers-Ash": "ADMIN",
        "jam-Pokemon:Trainers-Gary": "CU",
        "jam-Pokemon:Trainers-ProfessorOak": "CU",
        "jam-Pokemon:Trainers-ProfessorBirch": "CU"
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

> Note: Our permissions got compressed from CREATE, UPDATE to CU.
> This is because of how jam stores permissions, the values are equivilent.
> We could have set Gary's, Professor Oak's, and Professor Birch's permissions to CU but CREATE, UPDATE is a bit easier to read.

> Note: Remember that we gave jam-Pokemon:Trainers-* READ permissions earlier.
> Whenever Gary, Professor Oak, or Professor Birch access the Pokedex collection the will have that permission added to their CREATE, UPDATE permissions.

While we trust our friends, we may safety net. That way when we build an app we won't have to worry about invalid data.

We are going to leverage the power of JSONSchema and JamDB's schema validation for this.

> Note: For the sake of length and readability we are going to use a shortened schema.
> The actual Pokedex schema is much longer.

```http
PATCH /v1/namespaces/Pokemon/collections/Pokedex
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
          "HP": {
            "id": "HP",
            "type": "integer"
          },
          "evolves": {
            "id": "evolves",
            "type": "boolean"
          }
        },
        "required": [
          "name",
          "type",
          "HP",
          "evolves"
        ]
      }
    }
  }
]
```

> Note: The type of schema must be set at schema.type, the actual schema lives at schema.schema.
> This is so that JamDB may support other forms of schema validation in the future. Currently JSONSchema is the only supported validator.

> Note: `$` are illegal in JamDB key name.
> Make sure to exclude `$schema` from your JSONSchema

```json
{
  "data": {
    "id": "Pokemon.Pokedex",
    "type": "collections",
    "attributes": {
      "permissions": {
        "jam-Pokemon:Trainers-Ash": "ADMIN",
        "jam-Pokemon:Trainers-Gary": "CU",
        "jam-Pokemon:Trainers-ProfessorOak": "CU",
        "jam-Pokemon:Trainers-ProfessorBirch": "CU"
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
            "HP": {
              "id": "HP",
              "type": "integer"
            },
            "evolves": {
              "id": "evolves",
              "type": "boolean"
            }
          },
          "required": [
            "name",
            "type",
            "HP",
            "evolves"
          ]
        }
      }
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

# Documents

A document is any **JSON object** with a string identifier that lives in a collection.

> Strings, numbers, and arrays are all valid JSON but the root of a document must be a JSON object.

Time for the fun part, filling out the Pokedex!

Document are created like anything else, by POSTing to Pokedex's documents endpoint

```http
POST /v1/namespaces/Pokemon/collections/Pokedex/documents
Authorization: mycooljwt

{
  "data": {
    "id": "Pikachu",
    "type": "documents",
    "attributes": {
      "HP": 35,
      "evolves": true,
      "type": "Electric"
    }
  }
}
```

```json
{
  "data": {
    "id": "Pokemon.Pokedex.Pikachu",
    "type": "documents",
    "attributes": {
      "HP": 35,
      "evolves": true,
      "type": "Electric"
    },
    "meta": {...},
    "relationships": {...}
  }
}
```

For this next portion we're going to assume that our friends have filled out the rest of the Pokedex collection for us.

Now that we have all our data loaded up let's search it. We'll start with finding all entries with the `Electric` type.

> Documents may be filter by using the `filter[{key}]` query parameter.
> `{key}` is the key that you want to filter on and the value of that parameter is the value you'd like to filter for.
> `.`s are used to separate keys when referring to a nested object.

> Note: To save space we'll be using a page size of 2.
> Page size may be anywhere between 0 and 100, inclusive, and defaults to 50.

```http
GET /v1/namespaces/Pokemon/collections/Pokedex/documents?filter[type]=Electric&page[size]=2
Authorization: mycooljwt
```

```json
{
  "data": [
    {
      "id": "Pokemon.Pokedex.Pikachu",
      "type": "documents",
      "attributes": {
        "HP": 35,
        "evolves": true,
        "type": "Electric"
      },
      "meta": {...},
      "relationships": {...}
    }, {
      "id": "Pokemon.Pokedex.Riachu",
      "type": "documents",
      "attributes": {
        "HP": 60,
        "evolves": false,
        "type": "Electric"
      },
      "meta": {...},
      "relationships": {...}
    },
  ],
  "links": {...}
}
```

Next let's find the entry with the highest HP that is an electric type.

This can be achieved by filtering on type and then sorting on HP.

> Note: Sorts may be done ascending or descending by prepending the key you wish to sort on with a `+` or `-`, respectively.
> Sort if no order is specified it defaults to ascending.
> If no sort parameter is given the results are sorted by id, ascending.
> If you wish to sort on id, ascending or descending, use `sort=ref`. This is subject to change.

```http
GET /v1/namespaces/Pokemon/collections/Pokedex/documents?filter[type]=Electric&page[size]=1&sort=HP
Authorization: mycooljwt
```

```json
{
  "data": [
    {
      "id": "Pokemon.Pokedex.Ampharos",
      "type": "documents",
      "attributes": {
        "HP": 90,
        "evolves": false,
        "type": "Electric"
      },
      "meta": {...},
      "relationships": {...}
    }
  ],
  "links": {...}
}
```

Finally, Gary is trying to remember the id of a specific entry but only remembers that is ends with "two."

What an excellent opportunity to tap into JamDB's [Elastic Search](https://www.elastic.co/products/elasticsearch) API.

> The power of elasticsearch's [query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax) is exposed as the `q` query parameter at the _search endpoint.
> In accordance with the filter parameter, to query the id of a document use the `ref` key instead of id.

```http
GET /v1/namespaces/Pokemon/collections/Pokedex/documents?q=ref:*two
Authorization: mycooljwt
```

```json
{
  "data": [
    {
      "id": "Pokemon.Pokedex.Mewtwo",
      "type": "documents",
      "attributes": {
        "HP": 106,
        "evolves": false,
        "type": "Psychic"
      },
      "meta": {...},
      "relationships": {...}
    }
  ],
  "links": {...}
}
```
