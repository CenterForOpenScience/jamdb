# Documents

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
