Data Modeling
=============

JamDB is non-relational. A document is any **JSON object** with a string identifier that lives in a collection.

> Strings, numbers, and arrays are all valid JSON but the root of a document must be a JSON object.

Your data model is up to you. You can use IDs to create pseudo-relationships.

```
                  +--------------------------------------------------------+
                  |AuthorizationNamespace                                  |
                  +--------------------------------------------------------+
                  |                                                        |
                  |   +---------------+                                    |
                  |   |UserCollection |                                    |
                  |   +---------------+                                    |
                  |   |Id             +----------+                         |
                  |   |Name           |          |                         |
                  |   |FavoriteColor  |          |                         |
                  |   |ShirtSize      |          |                         |
                  |   |Gender         |          +--------------------+    |
                  |   |Email          |          ||UserGroupCollection|    |
                  |   +---------------+          |--------------------+    |
                  |                              ||UserId             |    |
                  |   +---------------------------+GroupId            |    |
                  |   |GroupCollection||          |                   |    |
                  |   +----------------|          +-------------------+    |
                  |   |Id             ++                                   |
                  |   |Name           |                                    |
                  |   +---------------+                                    |
                  |                                                        |
                  +--------------------------------------------------------+
```
