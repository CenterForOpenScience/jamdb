Feature: Getting a Namespace
  Scenario: Non-existant namespace
    Given namespace foobar does not exist
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 404

  Scenario: Invalid Namespace name
    Given namespace !@#$%^&*()-+ does exist
    When we GET "/v1/namespaces/!@#$%^&*()-+"
    Then the response code will be 404

  Scenario: Lack of permissions
    Given namespace foobar does exist
    And we have NONE permissions to foobar
    When we GET "/v1/namespaces/foobar"
    Then the response code will be 403

  Scenario: Not logged in
    Given namespace barfoo does exist
    And we are not logged in
    When we GET "/v1/namespaces/barfoo"
    Then the response code will be 401
