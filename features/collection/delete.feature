Feature: Deleting a collection

  Scenario: Deleted collections 404 on DELETE
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have DELETE permissions to namespace StarCraft
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg"
    And we DELETE "/v1/namespaces/StarCraft/collections/Zerg"
    Then the response code will be 404

  Scenario: Deleted collections 404 on GET
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have DELETE, READ permissions to namespace StarCraft
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg"
    And we GET "/v1/namespaces/StarCraft/collections/Zerg"
    Then the response code will be 404

  Scenario: Deleted responds no content
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg"
    Then the response code will be 204

  Scenario Outline: Allowed permissions
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have <permission> permissions to <rtype> <resource>
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg"
    Then the response code will be 204

    Examples:
      | permission | rtype      | resource  |
      | ADMIN      | namespace  | StarCraft |
      | ADMIN      | collection | Zerg      |
      | CRUD       | namespace  | StarCraft |
      | DELETE     | namespace  | StarCraft |


  Scenario Outline: Insufficient permissions
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have <permission> permissions to <rtype> <resource>
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg"
    Then the response code will be 403

    Examples:
      | permission | rtype      | resource  |
      | READ       | namespace  | StarCraft |
      | UPDATE     | namespace  | StarCraft |
      | NONE       | namespace  | StarCraft |
      | CREATE     | namespace  | StarCraft |
      | READ       | collection | Zerg      |
      | UPDATE     | collection | Zerg      |
      | NONE       | collection | Zerg      |
      | CREATE     | collection | Zerg      |
      | CRUD       | collection | Zerg      |
      | DELETE     | collection | Zerg      |
