# Collections
A collection is a bucket for arbitrary data. It's the equivalent of a table in a SQL or NoSQL database. It __may__ enforce a schema on its data. It also __may__ extend the permissions of the namespace.

### Creating a collection
To create a collection we just have to POST the data about our collection to our namespace's collections endpoint.

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
> - We have been given ADMIN access to this collection because we created it.
> - The id has been extended to `ProgrammingLanguages.Functional` because the `Functional` collection belongs to the `ProgrammingLanguages` namespace.
> - The full id (`ProgrammingLanguages.Functional`) or the truncated id (`Functional`) may be used when sending update requests.
> - The truncated id will be used for the rest of this document.

Now our fellow programmers are free to browse through the Functional collection, which we will add information into later.

It's a lot of work to load all this data into our collection by ourselves. Let's get some help!

### Adding collection permissions
We want to give a couple of our friends access to insert data into this collection but we don't want to grant them access to all of our collection.

Using collection-level permissions, we can do just that.

Collections can be updated the same way that namespace are, either POSTing or PATCHing data.
> __Please note:__
>
> - The JSONPatching format is a bit nicer to look at so we'll be using that method for the rest of this document.<br>
> - Keep in mind that you could just as easily PATCH the updated document instead.

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
> - Our permissions got compressed from CREATE, UPDATE to CU. This is the format JamDB stores permissions. CREATE, UPDATE and CU are equivalent. We
could have set Gary's, Professor Oak's, and Professor Birch's permissions to CU but CREATE, UPDATE is a bit easier to read.
> - Remember that we gave `jam-ProgrammingLanguages:Programmers-*` READ permissions earlier.
> - Whenever Gary, Professor Oak, or Professor Birch access the Functional collection they will have that permission added to their CREATE, UPDATE permissions.

While we trust our friends, we may want to enforce data validation.

We are going to leverage the power of [JSONSchema](http://json-schema.org) and JamDB's schema validation for this.

> Note: For the sake of length and readability we are going to use an abbreviated schema. The actual Functional schema is much longer because we're huge nerds.

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
> - `schema.type` must be set to the type of the schema. The actual schema lives at `schema.schema`. This is so that JamDB may support other forms of schema validation in the future. Currently JSONSchema is the only supported
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

[Documents](documents.html) would be a good place to continue on to.
