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
    And the URL "https://accounts.osf.io/oauth2/profile" responds 200
      """
      {
        "id": "juwia"
      }
      """
    And the URL "https://api.osf.io/v2/nodes/juwia/" responds 200
      """
      {
        "data": {
          "attributes": {
            "current_user_permissions": ["READ"]
          }
        }
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
            "permissions": "NONE",
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
        "sub": "user-osf-juwia"
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
    And the URL "https://accounts.osf.io/oauth2/profile" responds 200
      """
      {
        "id": "juwia"
      }
      """
    And the URL "https://api.osf.io/v2/nodes/juwia/" responds 200
      """
      {
        "data": {
          "attributes": {
            "current_user_permissions": <OSFPERMISSIONS>
          }
        }
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
        "sub": "user-osf-juwia"
      }
      """
  Examples:
      | OSFPERMISSIONS             | PERMISSIONS         | GRANTED             |
      | ["read"]                   | "READ"              | 2                   |
      | ["write"]                  | "CRUD"              | 15                  |
      | ["read"]                   | "CUD"               | 0                   |
      | ["admin"]                  | "ADMIN"             | 9223372036854775807 |
      | ["read", "write", "admin"] | "READ, CRUD, ADMIN" | 9223372036854775807 |
      | ["read", "write", "admin"] | "READ"              | 2                   |
      | []                         | "READ, CRUD, ADMIN" | 0                   |
      | ["read", "write", "admin"] | "NONE"              | 0                   |
      | ["Junk"]                   | "ADMIN"             | 0                   |

  Scenario Outline: Grants Permissions to requested
    Given namespace <NAMESPACE> exists
    And collection <COLLECTION> exists in namespace <NAMESPACE>
    And the grant plugin is enabled for collection <NAMESPACE>.<COLLECTION>
      """
      {
        "document": "NONE",
        "collection": "NONE"
      }
      """
    And the URL "https://accounts.osf.io/oauth2/profile" responds 200
      """
      {
        "id": "juwia"
      }
      """
    And the URL "https://api.osf.io/v2/nodes/<URL>/" responds 200
      """
      {
        "data": {
          "attributes": {
            "current_user_permissions": ["read", "write", "admin"]
          }
        }
      }
      """
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "permissions": "NONE",
            "document": <DOCUMENT>,
            "provider": "osfgrant",
            "access_token": "TOKEN",
            "namespace": "<NAMESPACE>",
            "collection": "<COLLECTION>"
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
          "<RESOURCE>": 0
        },
        "sub": "user-osf-juwia"
      }
      """
  Examples:
      | NAMESPACE | COLLECTION | DOCUMENT | URL     | RESOURCE                |
      | StarCraft | Protoss    | "Probe"  | Probe   | StarCraft.Protoss.Probe |
      | StarCraft | Protoss    | null     | Protoss | StarCraft.Protoss       |
      | StarCraft | Zerg       | null     | Zerg    | StarCraft.Zerg          |
      | StarCraft | Zerg       | "Drone"  | Drone   | StarCraft.Zerg.Drone    |


  Scenario: Must enable document
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And the grant plugin is enabled for collection StarCraft.Protoss
      """
      {
      }
      """
    And the URL "https://accounts.osf.io/oauth2/profile" responds 200
      """
      {
        "id": "juwia"
      }
      """
    And the URL "https://api.osf.io/v2/nodes/Probe/" responds 200
      """
      {
        "data": {
          "attributes": {
            "current_user_permissions": []
          }
        }
      }
      """
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "permissions": "NONE",
            "document": "Probe",
            "provider": "osfgrant",
            "access_token": "TOKEN",
            "namespace": "StarCraft",
            "collection": "Protoss"
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
          "detail": "document permissions must be provided via collection.plugins.grant.document"
        }]
      }
      """

  Scenario: Must enable collection
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And the grant plugin is enabled for collection StarCraft.Protoss
      """
      {
      }
      """
    And the URL "https://accounts.osf.io/oauth2/profile" responds 200
      """
      {
        "id": "juwia"
      }
      """
    And the URL "https://api.osf.io/v2/nodes/Protoss/" responds 200
      """
      {
        "data": {
          "attributes": {
            "current_user_permissions": []
          }
        }
      }
      """
    When I POST to "/v1/auth"
      """
      {
        "data": {
          "type": "users",
          "attributes": {
            "permissions": "NONE",
            "provider": "osfgrant",
            "access_token": "TOKEN",
            "namespace": "StarCraft",
            "collection": "Protoss"
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
