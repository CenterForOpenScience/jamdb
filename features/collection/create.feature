Feature: Creating a collection
  Scenario: Collection exists
    Given namespace foo does exist
    And we have ADMIN permissions to namespace foo
    And collection bar exists in namespace foo
    When we create collection bar in namespace foo
    Then the response code will be 409
    And the response will contain
      """
        {
          "errors": [{
            "code": "C409",
            "status": "409",
            "title": "Collection already exists",
            "detail": "Collection \"bar\" already exists in namespace \"foo\""
          }]
        }
      """

  Scenario: Namespace doesn't exist
    Given namespace foo does not exist
    When we create collection bar in namespace foo
    Then the response code will be 404
    And the response will contain
      """
        {
          "errors": [{
            "code": "N404",
            "status": "404",
            "title": "Namespace not found",
            "detail": "Namespace \"foo\" was not found"
          }]
        }
      """

  Scenario: New collection
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace foo does exist
    And we have ADMIN permissions to namespace foo
    When we create collection bar in namespace foo
    Then the response code will be 201
    And the response will contain
      """
      {
        "data": {
            "id": "foo.bar",
            "type": "collections",
            "attributes": {
              "name": "bar",
              "permissions": {
                "user-testing-we": "ADMIN"
              }
            },
            "meta": {
              "created-by": "user-testing-we",
              "modified-by": "user-testing-we",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/foo/collections/bar/documents",
                  "related": "http://localhost:50325/v1/namespaces/foo/collections/bar/documents"
                }
              }
            }
          }
      }
      """

  Scenario: No permissions to namespace
    Given namespace foo does exist
    And we are not logged in
    When we create collection bar in namespace foo
    Then the response code will be 401


  Scenario Outline: Insufficient permissions to namespace
    Given namespace foo does exist
    And we have <permission> permissions to namespace foo
    When we create collection bar in namespace foo
    Then the response code will be 403

    Examples: Permissions
      | permission |
      | CREATE     |
      | READ       |
      | UPDATE     |
      | DELETE     |
      | CRUD       |
      | READ_WRITE |


  Scenario: Initial schema
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we POST "/v1/namespaces/StarCraft/collections"
      """
        {
          "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "schema": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "Health": {
                      "type": "integer"
                    }
                  },
                  "additionalProperties": false,
                  "required": [
                    "Unit"
                  ]
                },
                "type": "jsonschema"
              }
            }
          }
        }
      """
    Then the response code will be 201
    And the response will contain
      """
      {
        "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "name": "Terran",
              "permissions": {
                "user-testing-we": "ADMIN"
              },
              "schema": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "Health": {
                      "type": "integer"
                    }
                  },
                  "additionalProperties": false,
                  "required": [
                    "Unit"
                  ]
                },
                "type": "jsonschema"
              }
            },
            "meta": {
              "created-by": "user-testing-we",
              "modified-by": "user-testing-we",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/StarCraft/collections/Terran/documents",
                  "related": "http://localhost:50325/v1/namespaces/StarCraft/collections/Terran/documents"
                }
              }
            }
          }
      }
      """


  Scenario: Bad initial schema
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we POST "/v1/namespaces/StarCraft/collections"
      """
        {
          "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "schema": {
                "schema": 1,
                "type": "Not found"
              }
            }
          }
        }
      """
    Then the response code will be 400
    And the response will be
      """
        {
          "errors": [{
            "code": "C400",
            "status": "400",
            "title": "Invalid schema type",
            "detail": "\"Not found\" is not a valid schema type"
          }]
        }
      """


  Scenario Outline: Bad jsonschema
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we POST "/v1/namespaces/StarCraft/collections"
      """
        {
          "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "schema": <SCHEMA>
            }
          }
        }
      """
    Then the response code will be 400
    And the response will be
      """
        {
          "errors": [{
            "code": "C400",
            "status": "400",
            "title": "Invalid schema",
            "detail": "The supplied data was an invalid jsonschema schema"
          }]
        }
        """

    Examples:
      | SCHEMA                               |
      | {"schema": 1, "type": "jsonschema"}  |
      | {"schema": "", "type": "jsonschema"} |


  Scenario Outline: Bad schema
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we POST "/v1/namespaces/StarCraft/collections"
      """
        {
          "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "schema": <SCHEMA>
            }
          }
        }
      """
    Then the response code will be 400

    Examples:
      | {"schema": {}, "type": 1}            |
      | {"schema": {}, "type": {}}           |
      | {}                                   |
      | "String"                             |
      | 2                                    |


  Scenario Outline: Malformed permissions
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we POST "/v1/namespaces/StarCraft/collections"
      """
        {
          "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "permissions": <PERMISSIONS>
            }
          }
        }
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "code": "S400",
            "status": "400",
            "title": "Schema validation failed"
          }]
        }
      """

    Examples:
      | PERMISSIONS                          |
      | {"schema": 1, "type": "jsonschema"}  |
      | {"schema": "", "type": "jsonschema"} |
      | {"schema": {}, "type": 1}            |
      | {"schema": {}, "type": {}}           |
      | "String"                             |
      | 2                                    |
