# Namespaces
A namespace is the equivalent of a database in MongoDB or PostgreSQL.

It will act as a top-level container for any collections you make and store permissions that apply to itself and cascade to anything inside of it.

Administrator privileges are required to make any modification to a namespace.

### Creating a namespace
Currently, there is no way to create a namespace through the API. If you're working with a remote instance of JamDB, contact the server administrator to create a namespace. If you're running a local instance of JamDB, you can create a namespace by running `jam create <namespace id> -u 'jam-ProgrammingLanguages:Programmers-Ash`.

> We'll be using `ProgrammingLanguages` as the example namespace id for the rest of this document. Namespace ids are case-sensitive.

Once your namespace is setup, you'll need to send the proper `Authorization` header to access it.

### Authorizing against a namespace
JamDB uses [json web tokens](https://jwt.io), JWT for short, in the `Authorization` header or the `token` query string parameter.

There are three ways to acquire a JWT:

1. Contact the server administrator and request a temporary token.
2. Authenticate via the [Auth Endpoint](authentication.html)
3. If you are running a JamDB server locally you can generate a token by running `jam token 'jam-ProgrammingLanguages:Programmers-Ash'`

> We'll be using `mycooljwt` as the example JWT for the rest of this
document.

### Investigating a namespace
You can get information about your namespace by making an HTTP request using [curl](https://en.wikipedia.org/wiki/CURL), [Paw](https://luckymarmot.com/paw), or a similar program.

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


## Namespace Permissions

Giving other users permissions to a namespace is easy.

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


Or we can just PATCH up our updated data and let the JamDB server figure it out.

**This is potentially a destructive action.**
Any existing permissions will be completely replaced. If you want to do a partial update use the JSONPatch method above.

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

[Collections](collections.html) are the next step in the documentation.
