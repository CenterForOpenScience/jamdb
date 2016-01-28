Feature: Updating a collection

  Scenario: Updating Permissions
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When we PATCH "/v1/namespaces/StarCraft/collections/Protoss"
      """
      {
        "data": {
            "id": "StarCraft.Protoss",
            "type": "collections",
            "attributes": {
              "permissions": {
                "jam-Starcraft.Terran-*": "ADMIN"
              }
            }
          }
        }
      """
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": {
            "id": "StarCraft.Protoss",
            "type": "collections",
            "attributes": {
              "permissions": {
                "jam-Starcraft.Terran-*": "ADMIN"
              }
            }
          }
        }
      """

  Scenario: Updating Permissions via jsonpatch
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Protoss"
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
            "id": "StarCraft.Protoss",
            "type": "collections",
            "attributes": {
              "permissions": {
                "jam-Starcraft.Terran-*": "ADMIN"
              }
            }
          }
        }
      """

  Scenario: Invalid Permissions
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Protoss"
      """
        [{
          "op": "add",
          "path": "/permissions/jam-Starcraft.Terran-*",
          "value": "Reaver"
        }]
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "code": "P400",
            "status": "400",
            "title": "Invalid permission",
            "detail": "\"Reaver\" is not a valid permission level"
          }]
        }
      """

  Scenario: Incorrect Permissions
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Protoss"
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
          "errors": [{
            "code": "P400",
            "status": "400",
            "title": "Invalid permission",
            "detail": "\"42\" is not a valid permission level"
          }]
        }
      """

  Scenario: Invalid user selector
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Protoss"
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
          "errors": [{
            "code": "S400",
            "status": "400",
            "title": "Schema validation failed",
            "detail": "Validation error \"Additional properties are not allowed ('justsomejumbleduptext' was unexpected)\" at \"permissions\" against schema \"{\"additionalProperties\": false, \"patternProperties\": {\"^(\\\\*|[^\\\\s\\\\-\\\\*]+\\\\-\\\\*|[^\\\\s\\\\-\\\\*]+\\\\-[^\\\\s\\\\-\\\\*]+\\\\-\\\\*|[^\\\\s\\\\-\\\\*]+\\\\-[^\\\\s\\\\-\\\\*]+\\\\-[^\\\\s\\\\-\\\\*]+)$\": {\"type\": \"integer\"}}, \"type\": \"object\"}\""
          }]
        }
      """


  Scenario: Can not add additional properties
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Protoss"
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
          "errors": [{
            "code": "400",
            "status": "400",
            "title": "Invalid field",
            "detail": "Values at \"/SomeOtherKey\" may not be altered"
          }]
        }
      """
