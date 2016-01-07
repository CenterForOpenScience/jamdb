# Authentication
JamDB uses [Javascript Web Tokens](https://jwt.io) for authentication.

A successful authentication require returns the following structure

```json
    {
        "data": {
            "id": "<type>-<provider>-<id>",
            "type": "users",
            "attributes": {
                "type": "user",
                "token": "<jwt>",
                "provider": "<provider>"
            }
        }
    }
```

To authenticate to the JamDB Rest API the `token` attribute of the previous structure must be provided via the HTTP `Authentication` header or as a cookie named `jam`.
