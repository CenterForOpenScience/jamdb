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
            "id": "bar",
            "type": "collections",
            "attributes": {
              "name": "bar",
              "permissions": {
                "user-testing-we": 9223372036854775807
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
