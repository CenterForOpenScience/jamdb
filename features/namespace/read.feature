Feature: Getting a Namespace
  Scenario: Non-existant namespace
    Given namespace foobar does not exist
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 404
    And the response will contain
      """
        {
          "errors": [{
            "code": "N404",
            "status": "404",
            "title": "Namespace not found",
            "detail": "Namespace \"foobar\" was not found"
          }]
        }
      """
  Scenario: Invalid Namespace name
    Given namespace !@#$%^&*()-+ does exist
    When we GET "/v1/namespaces/!@#$%^&*()-+"
    Then the response code will be 404
    And the response will contain
      """
        {
          "errors": [{
            "status": "404",
            "detail": "Not Found"
          }]
        }
      """
  Scenario: Lack of permissions
    Given namespace foobar does exist
    And we have NONE permissions to namespace foobar
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 403

  Scenario Outline: Lack of permissions
    Given namespace foobar does exist
    And we have <permission> permissions to namespace foobar
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 403
    And the response will contain
      """
        {
          "errors": [{
            "code": "403",
            "status": "403",
            "title": "Forbidden",
            "detail": "READ permission or higher is required to perform this action"
          }]
        }
      """

    Examples: Permissions
      | permission |
      | CREATE     |
      | UPDATE     |
      | DELETE     |
      | CU         |
      | CUD        |


  Scenario Outline: Correct permissions
    Given namespace foobar does exist
    And we have <permission> permissions to namespace foobar
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 200

    Examples:
      | permission |
      | READ       |
      | RU         |
      | CRU        |
      | RUD        |
      | CRUD       |
      | READ_WRITE |


  Scenario: Not logged in
    Given namespace barfoo does exist
    And we are not logged in
    When we GET "/v1/namespaces/barfoo"
    Then the response code will be 401


  Scenario: Namespace hierachical return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we GET "/v1/namespaces/StarCraft"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "name": "StarCraft",
              "permissions": {
                "user-testing-we": "ADMIN",
                "user-testing-system": "ADMIN"
              }
            },
            "meta": {
              "permissions": "ADMIN",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "collections": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/StarCraft/collections",
                  "related": "http://localhost:50325/v1/namespaces/StarCraft/collections"
                }
              }
            }
          }
        }
        """


  Scenario: Namespace id return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we GET "/v1/id/namespaces/StarCraft"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "name": "StarCraft",
              "permissions": {
                "user-testing-we": "ADMIN",
                "user-testing-system": "ADMIN"
              }
            },
            "meta": {
              "permissions": "ADMIN",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "collections": {
                "links": {
                  "self": "http://localhost:50325/v1/id/namespaces/StarCraft/collections",
                  "related": "http://localhost:50325/v1/id/namespaces/StarCraft/collections"
                }
              }
            }
          }
        }
        """
