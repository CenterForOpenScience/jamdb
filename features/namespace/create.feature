Feature: Creating a namespace

  Scenario: New Namespace
    Given the time is 2015-01-01T00:00:00.0000Z
    And we are a system user
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {}
          }
        }
      """
    Then the response code will be 201
    And the response will be
      """
        {
          "data": {
              "id": "StarCraft",
              "type": "namespaces",
              "attributes": {
                "name": "StarCraft",
                "permissions": {
                  "system-system-we": "ADMIN"
                }
              },
              "meta": {
                "permissions": "ADMIN",
                "created-by": "system-system-we",
                "modified-by": "system-system-we",
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

  Scenario: Namespace Exists
    Given namespace StarCraft exists
    And we are a system user
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {}
          }
        }
      """
    Then the response code will be 409
    And the response will be
      """
      {
        "errors": [{
          "code": "N409",
          "status": "409",
          "title": "Namespace already exists",
          "detail": "Namespace \"StarCraft\" already exists"
        }]
      }
      """

  Scenario: Invalid Name
    Given we are a system user
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "Star-Craft",
            "type": "namespaces",
            "attributes": {}
          }
        }
      """
    Then the response code will be 400
    And the response will be
      """
      {
        "errors": [{
          "code": "400",
          "status": "400",
          "title": "Invalid id",
          "detail": "Expected data.id to match the Regex [\\d\\w]{3,64}, optionally prefixed by its parents ids seperated via ."
        }]
      }
      """

  Scenario: No Permissions
    Given we are not logged in
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {}
          }
        }
      """
    Then the response code will be 401
    And the response will be
      """
      {
        "errors": [{
          "code": "401",
          "status": "401",
          "title": "Unauthorized",
          "detail": "Unauthorized"
        }]
      }
      """

  Scenario Outline: Insufficient Permissions
    Given we have <PERMISSION> permissions
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {}
          }
        }
      """
    Then the response code will be 403
    And the response will be
      """
      {
        "errors": [{
          "code": "403",
          "status": "403",
          "title": "Forbidden",
          "detail": "CREATE permission or higher is required to perform this action"
        }]
      }
      """

    Examples: Permissions
      | PERMISSION |
      | READ       |
      | UPDATE     |
      | DELETE     |

  Scenario: Initial Permissions
    Given we are a system user
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "ADMIN"
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
              "id": "StarCraft",
              "type": "namespaces",
              "attributes": {
                "name": "StarCraft",
                "permissions": {
                  "user-testing-we": "ADMIN",
                  "system-system-we": "ADMIN"
                }
              }
            }
        }
      """

  Scenario: Malformed Data
    Given we are a system user
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "Some": ["Other", "Attrs"]
            }
          }
        }
      """
    Then the response code will be 400
    And the response will be
      """
        {
          "errors": [{
            "code": "400",
            "status": "400",
            "title": "Invalid field",
            "detail": "Values at \"Some\" may not be altered"
          }]
        }
      """

  Scenario: Malformed Permissions
    Given we are a system user
    When we POST to "/v1/namespaces"
      """
        {
          "data": {
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": {},
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
            "code": "P400",
            "status": "400",
            "title": "Invalid permission",
            "detail": "\"{}\" is not a valid permission level"
          }]
        }
      """
