Feature: User Plugin

  Scenario: Must be enabled
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
    Then the response code will be 412

  Scenario Outline: Enabled checked first
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    When we <METHOD> "/v1/id/collections/StarCraft.Protoss/user"
    Then the response code will be 412
    And the response will be
      """
      {
        "errors": [{
          "code": "412",
          "detail": "Plugin \"user\" is not enabled on this collection",
          "status": "412",
          "title": "Plugin not enabled"
        }]
      }
      """

    Examples:
      | METHOD |
      | GET    |
      | PUT    |
      | PATCH  |
      | DELETE |

  Scenario Outline: Unsupported methods
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
    When we <METHOD> "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {}
        }
      }
      """
    Then the response code will be 405
    And the response will be
      """
      {
        "errors": [{
          "code": "405",
          "status": "405",
          "title": "Method Not Allowed",
          "detail": "<METHOD>s are not allowed at this endpoint"
        }]
      }
      """

    Examples:
      | METHOD |
      | GET    |
      | PUT    |
      | PATCH  |
      | DELETE |

  Scenario: MandrillKey must be set
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
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
          "detail": "mandrillKey must be provided via collection.plugins.mandrillKey"
        }]
      }
      """

  Scenario: Missing document reports success
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {
        "mandrillKey": "wert"
      }
      """
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
            "id": "(;´༎ຶД༎ຶ`)"
          }
        }
      }
      """
    Then the response code will be 201
    And the response will be
      """
      {
        "data": {
          "id": "(;´༎ຶД༎ຶ`)",
          "type": "reset",
          "attributes": {
            "status": "success"
          }
        }
      }
      """

  Scenario: Existing document reports success
    Given we mock jam.plugins.user.mandrill
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {
        "mandrillKey": "wert"
      }
      """
    And document (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ) exists in StarCraft.Protoss
      """
      {
        "email": "sandhya@dinosaurs.sexy"
      }
      """
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
            "id": "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)"
          }
        }
      }
      """
    Then the response code will be 201
    And the response will be
      """
      {
        "data": {
          "id": "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)",
          "type": "reset",
          "attributes": {
            "status": "success"
          }
        }
      }
      """

  Scenario: Handles missing data
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {"mandrillKey": "wert"}
      """
    And document ༼ ༎ຶ ෴ ༎ຶ༽ exists in StarCraft.Protoss
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
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
          "detail": "Id must be provided"
        }]
      }
      """

  Scenario: Handles no data
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {"mandrillKey": "wert"}
      """
    And document ༼ ༎ຶ ෴ ༎ຶ༽ exists in StarCraft.Protoss
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
    Then the response code will be 400
    And the response will be
      """
      {
        "errors": [{
          "code": "400",
          "status": "400",
          "detail": "Malformed data",
          "title": "Malformed data"
        }]
      }
      """

  Scenario: Calls mandrill with defaults
    Given we mock jam.plugins.user.mandrill
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {"mandrillKey": "wert"}
      """
    And document HighTemplar exists in StarCraft.Protoss
      """
      {
        "email": "foo@bar.baz"
      }
      """
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
            "id": "HighTemplar"
          }
        }
      }
      """
    Then the response code will be 201
    And mandrill will be called with
      """
      {
        "template_name": "password-reset",
        "template_content": [{"token": ""}],
        "message": {"to":[{"email": "foo@bar.baz"}]}
      }
      """

  Scenario: Calls mandrill with custom values
    Given we mock jam.plugins.user.mandrill
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {
        "mandrillKey": "wert",
        "emailField": "user_id",
        "template": "halpmausers"
      }
      """
    And document DarkTemplar exists in StarCraft.Protoss
      """
      {
        "user_id": "Zeratul@Protoss.Xelnaga"
      }
      """
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
            "id": "DarkTemplar"
          }
        }
      }
      """
    Then the response code will be 201
    And mandrill will be called with
      """
      {
        "template_name": "halpmausers",
        "template_content": [{"token": "<generated>"}],
        "message": {"to":[{"email": "Zeratul@Protoss.Xelnaga"}]}
      }
      """


  Scenario: Mandrill Error
    Given jam.plugins.user.mandrill.Mandrill will throw MandrillError
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {
        "mandrillKey": "wert"
      }
      """
    And document DarkTemplar exists in StarCraft.Protoss
      """
      {
        "email": "sandhya@dinosaurs.sexy"
      }
      """
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
            "id": "DarkTemplar"
          }
        }
      }
      """
    Then the response code will be 503
    And the response will be
      """
      {
        "errors": [{
          "code": "503",
          "status": "503",
          "title": "Service Unavailable",
          "detail": "Unable to submit request to mandrill"
        }]
      }
      """

  Scenario: Invalid Email
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Protoss
      """
      {
        "mandrillKey": "wert"
      }
      """
    And document DarkTemplar exists in StarCraft.Protoss
      """
      {
        "email": "---------------------"
      }
      """
    When we POST "/v1/id/collections/StarCraft.Protoss/user"
      """
      {
        "data": {
          "type": "reset",
          "attributes": {
            "id": "DarkTemplar"
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
          "detail": "\"---------------------\" at \"email\" is not a valid email"
        }]
      }
      """
