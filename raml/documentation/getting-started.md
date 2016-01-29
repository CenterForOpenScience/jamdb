# Getting Started

Please note: These docs are still in progress.
If something doesn't look quite right it's probably wrong.

This tutorial assumes that the JamDB server you're interacting with will be at `http://localhost:1212`.

## API Notes

## Namespace

To start using JamDB, you will need a namespace. A namespace is the equivalent of a database in MongoDB or PostgreSQL.

It will act as a container for any collections you make and store permissions that apply to itself and anything inside of it.

Administrator privileges are required to make any modification to a namespace.

Currently there is no way to create a namespace through the API.
If you're working with a remote instance of JamDB contact the server administrator to set up a namespace for you.
If you're running a local instance of JamDB you can create a namespace by running `jam create <namespace id> -u 'tracked-Pokemon|Trainers-Ash`.

> We'll be using `Pokemon` as the namespace id for the rest of this document.

Once your namespace is setup you'll need to send the proper `Authorization` header to access it.

Jam uses [json web tokens](https://jwt.io), jwt for short, in the `Authorization` header or the `token` query parameter.

There are 3 ways to acquire a jwt.

1. Contact the server admin and request a temporary token.
2. Generate a token by running `jam token 'tracked-Pokemon|trainers-Ash'`
  * This will only work if you are running JamDB locally
3. Authenticate via the [Auth Endpoint](#authorization)

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
        "tracked-Pokemon|Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...}
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

[{"op": "add", "path": "/permissions/tracked-Pokemon|Trainers-*", "value": "READ"}]
```

```json
{
  "data": {
    "id": "Pokemon",
    "type": "namespaces",
    "attributes": {
      "name": "Pokemon",
      "permissions": {
        "tracked-Pokemon|Trainers-*": "READ",
        "tracked-Pokemon|Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...}
  }
}
```

Many jsonpatch objects may be sent at once.

```http
PATCH /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt
Content-Type: Content-Type: application/vnd.api+json; ext=jsonpatch

[
  {"op": "add", "path": "/permissions/tracked-Pokemon|Trainers-*", "value": "READ"},
  {"op": "add", "path": "/permissions/tracked-Pokemon|Trainers-Misty", "value": "ADMIN"},
  {"op": "add", "path": "/permissions/tracked-Pokemon|Trainers-Brock", "value": "ADMIN"}
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
        "tracked-Pokemon|Trainers-*": "READ",
        "tracked-Pokemon|Trainers-Ash": "ADMIN",
        "tracked-Pokemon|Trainers-Misty": "ADMIN",
        "tracked-Pokemon|Trainers-Brock": "ADMIN",
      }
    },
    "meta": {...}
  }
}
```

Or we can just PATCH up our updated data and let the JamDB server figure it out.

```http
PATCH /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt

{
  "id": "Pokemon",
  "type": "namespaces",
  "attributes": {
    "name": "Pokemon",
    "permissions": {
      "tracked-Pokemon|Trainers-*": "READ",
      "tracked-Pokemon|Trainers-Ash": "ADMIN"
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
      "name": "Pokemon",
      "permissions": {
        "tracked-Pokemon|Trainers-*": "READ",
        "tracked-Pokemon|Trainers-Ash": "ADMIN"
      }
    },
    "meta": {...}
  }
}
```


# Collections
