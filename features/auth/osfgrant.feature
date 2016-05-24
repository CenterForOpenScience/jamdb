Feature: OSF Grant Authentication

  Scenario: Plugin must be enabled
    Given namespace Comments exists
    And collection juwia exists in namespace Comments
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "namespace": "Comments",
            "collection": "juwia",
            "provider": "osfgrant",
            "access_token": "TOKEN"
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
          "detail": "Plugin \"grant\" is not enabled on this collection"
        }]
      }
      """

  Scenario: Plugin must be configured
    Given namespace Comments exists
    And collection juwia exists in namespace Comments
    And the grant plugin is enabled for collection Comments.juwia
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "namespace": "Comments",
            "collection": "juwia",
            "provider": "osfgrant",
            "access_token": "TOKEN"
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
          "title": "Bad Request",
          "detail": "collection permissions must be provided via collection.plugins.grant.collection"
        }]
      }
      """

  Scenario: Can authenticate
    Given namespace Comments exists
    And collection juwia exists in namespace Comments
    And the grant plugin is enabled for collection Comments.juwia
      """
      {
        "collection": "NONE"
      }
      """
    And the URL "https://osf.io/api/v1/project/juwia/permissions" responds 200
      """
      {
        "permissions": []
      }
      """
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "collection": "juwia",
            "namespace": "Comments",
            "provider": "osfgrant",
            "access_token": "juwia"
          }
        }
      }
      """
    Then the response code will be 200
    And my JWT will contain
      """
      {
        "limit": false,
        "granted": {
          "Comments.juwia": 0
        },
        "sub": "grant-osf-juwia"
      }
      """

  Scenario Outline: Grants Permissions
    Given namespace Comments exists
    And collection juwia exists in namespace Comments
    And the grant plugin is enabled for collection Comments.juwia
      """
      {
        "collection": "ADMIN"
      }
      """
    And the URL "https://osf.io/api/v1/project/juwia/permissions" responds 200
      """
      {
        "permissions": <OSFPERMISSIONS>
      }
      """
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "provider": "osfgrant",
            "collection": "juwia",
            "namespace": "Comments",
            "access_token": "TOKEN",
            "permissions": <PERMISSIONS>
          }
        }
      }
      """
    Then the response code will be 200
    And my JWT will contain
      """
      {
        "limit": false,
        "granted": {
          "Comments.juwia": <GRANTED>
        },
        "sub": "grant-osf-juwia"
      }
      """
  Examples:
      | OSFPERMISSIONS             | PERMISSIONS                | GRANTED             |
      | ["read"]                   | ["read"]                   | 2                   |
      | ["write"]                  | ["write"]                  | 15                  |
      | ["read"]                   | ["write"]                  | 0                   |
      | ["admin"]                  | ["admin"]                  | 9223372036854775807 |
      | ["read", "write", "admin"] | ["read", "write", "admin"] | 9223372036854775807 |
      | ["read", "write", "admin"] | ["read"]                   | 2                   |
      | []                         | ["read", "write", "admin"] | 0                   |
      | ["read", "write", "admin"] | []                         | 0                   |
      | ["Junk"]                   | ["admin"]                  | 0                   |
