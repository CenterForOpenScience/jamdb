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
            "code": "N404",
            "status": "404",
            "title": "Namespace not found",
            "detail": "Namespace \"!@#$%^&*()-+\" was not found"
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
            "detail": "ADMIN permission or higher is required to perform this action"
          }]
        }
      """

    Examples: Permissions
      | permission |
      | CREATE     |
      | READ       |
      | UPDATE     |
      | DELETE     |
      | CRUD       |
      | READ_WRITE |

  Scenario: Not logged in
    Given namespace barfoo does exist
    And we are not logged in
    When we GET "/v1/namespaces/barfoo"
    Then the response code will be 401

  Scenario: Get with namespace admin permissions
    Given namespace foobar does exist
    And we have ADMIN permissions to namespace foobar
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 200

  Scenario: Get namespace read permissions
    Given namespace foobar does exist
    And we have READ permissions to namespace foobar
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 403
