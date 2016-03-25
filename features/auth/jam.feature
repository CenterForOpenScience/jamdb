Feature: Jam authentication

  Scenario: Can login
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
      """
      {
        "schema": {
          "type": "jsonschema",
          "schema": {
            "type": "object",
            "required": ["password"],
            "properties": {
              "password": {
                "id": "password",
                "type": "string",
                "pattern": "^\\$2b\\$1[0-3]\\$\\S{53}$"
              }
            }
          }
        }
      }
      """
    And the user plugin is enabled for collection StarCraft.Protoss
    And document Arbiter exists in StarCraft.Protoss
      """
      {
        "password": "$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G"
      }
      """
    When we POST "/v1/auth"
      """
      {
        "data": {
          "id": "Arbiter",
          "type": "users",
          "attributes": {
            "provider": "self",
            "collection": "Protoss",
            "namespace": "StarCraft",
            "username": "Arbiter",
            "password": "password"
          }
        }
      }
      """
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": {
          "id": "jam-StarCraft:Protoss-Arbiter",
          "type": "users",
          "attributes": {
            "type": "jam",
            "id": "Arbiter",
            "provider": "StarCraft:Protoss"
          }
        }
      }
      """


  Scenario: No plugin
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
      """
      {
        "schema": {
          "type": "jsonschema",
          "schema": {
            "type": "object",
            "required": ["password"],
            "properties": {
              "password": {
                "id": "password",
                "type": "string",
                "pattern": "^\\$2b\\$1[0-3]\\$\\S{53}$"
              }
            }
          }
        }
      }
      """
    And document Arbiter exists in StarCraft.Protoss
      """
      {
        "password": "$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G"
      }
      """
    When we POST "/v1/auth"
      """
      {
        "data": {
          "id": "Arbiter",
          "type": "users",
          "attributes": {
            "provider": "self",
            "collection": "Protoss",
            "namespace": "StarCraft",
            "username": "Arbiter",
            "password": "password"
          }
        }
      }
      """
    Then the response code will be 412
    And the response will be
      """
      {
        "errors": [{
          "code": "412",
          "status": "412",
          "title": "Plugin not enabled",
          "detail": "Plugin \"user\" is not enabled on this collection"
        }]
      }
      """

  Scenario: No Schema
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
    And document Arbiter exists in StarCraft.Protoss
      """
      {
        "password": "$2b$12$iujjM4DtPMWVL1B2roWjBeHzjzxaNEP8HbXxdZwRha/j5Pc8E1n2G"
      }
      """
    When we POST "/v1/auth"
      """
      {
        "data": {
          "id": "Arbiter",
          "type": "users",
          "attributes": {
            "provider": "self",
            "collection": "Protoss",
            "namespace": "StarCraft",
            "username": "Arbiter",
            "password": "password"
          }
        }
      }
      """
    Then the response code will be 400
    And the response will contain
      """
      {
        "errors": [{
          "code": "400",
          "status": "400",
          "title": "Bad password schema"
        }]
      }
      """
