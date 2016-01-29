# Authentication
JamDB uses [Json Web Tokens](https://jwt.io) for authentication.


## Authenticating

JamDB allows authentication through many providers.
Currently `osf` and `self` are the only available providers.

A user may authenticate to JamDB by sending a properly formatted `POST` request to Jam's auth endpoint, `/v1/auth`

```http
GET /v1/auth HTTP/1.1

{
  "data": {
    "type": "users",
    "attributes": {
      "provider": ...
      ...
    }
  }
}
```

> provider and the latter elements of `attributes` have been left blank as they very for each provider.


A successful authentication request will return the following data

```json
    {
        "data": {
            "id": "<type>-<provider>-<id>",
            "type": "users",
            "attributes": {
                "id": "<id>",
                "type": "<type>",
                "provider": "<provider>",
                "token": "<jwt>",
            }
        }
    }
```

`data.id` is the [user id](#user-ids-and-selectors) it will be matched against [user selectors](#user-ids-and-selectors) to calculate it's permissions.

`data.attributes.id` is the provider specific id for this user.

`data.attributes.type` is the [type of user](#user-types) for this user.

`data.attributes.provider` is the provider that was used to authenticate as this user.

`data.attributes.token` is the jwt used to authorize requests to JamDB


## Authorizing

Authorization may be provided for an HTTP request in either the `Authorization` header or the `token` query parameter.

> Note: The `Authorization` header takes presidence over the `token` query parameter

```http
GET /v1/namespaces/Pokemon HTTP/1.1
Authorization: mycooljwt
```

```http
PUT /v1/namespaces/Pokemon?token=mycooljwt HTTP/1.1
```

## User IDs and Selectors
