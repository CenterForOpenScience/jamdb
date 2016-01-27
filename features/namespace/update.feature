@wip
Feature: Updating a namespace

  Scenario: Updating Permissions via jsonpatch
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft"
      """
        [{
          "op": "add",
          "path": "/permissions/jam-Starcraft.Terran-*",
          "value": "ADMIN"
        }]
      """
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": {
            "id": "Starcraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "ADMIN",
                "jam-Starcraft.Terran-*": "ADMIN"
              }
            }
          }
        }
      """

  Scenario: Invalid Permissions
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft"
      """
        [{
          "op": "add",
          "path": "/permissions/jam-Starcraft.Terran-*",
          "value": "OVERLORD"
        }]
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [null]
        }
      """

  Scenario: Incorrect Permissions
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft"
      """
        [{
          "op": "add",
          "path": "/permissions/jam-Starcraft.Terran-*",
          "value": 42
        }]
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [null]
        }
      """

  Scenario: Invalid user selector
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft"
      """
        [{
          "op": "add",
          "path": "/permissions/justsomejumbleduptext",
          "value": "READ"
        }]
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [null]
        }
        """

  Scenario: Can not add additional properties
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft"
      """
        [{
          "op": "add",
          "path": "/SomeOtherKey",
          "value": {"A new": "Hope"}
        }]
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [null]
        }
        """
