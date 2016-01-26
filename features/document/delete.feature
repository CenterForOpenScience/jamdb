Feature: Deleting a document

  Scenario: Deleted documents 404
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document Drone exists in StarCraft/Zerg
    And we have DELETE permissions to collection Zerg
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg/documents/Drone"
    And we DELETE "/v1/namespaces/StarCraft/collections/Zerg/documents/Drone"
    Then the response code will be 404

  Scenario Outline: Allowed permissions
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document Drone exists in StarCraft/Zerg
    And we have <permission> permissions to <rtype> <resource>
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg/documents/Drone"
    Then the response code will be 204

    Examples:
      | permission | rtype      | resource  |
      | ADMIN      | namespace  | StarCraft |
      | CRUD       | namespace  | StarCraft |
      | DELETE     | namespace  | StarCraft |
      | ADMIN      | collection | Zerg      |
      | CRUD       | collection | Zerg      |
      | DELETE     | collection | Zerg      |


  Scenario Outline: Allowed permissions
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document Drone exists in StarCraft/Zerg
    And we have <permission> permissions to <rtype> <resource>
    When we DELETE "/v1/namespaces/StarCraft/collections/Zerg/documents/Drone"
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

  Scenario: Creator can delete document
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have CREATE permissions to collection Zerg
    When we create document Drone in StarCraft/Zerg
    And we DELETE "/v1/namespaces/StarCraft/collections/Zerg/documents/Drone"
    Then the response code will be 204

  @wip
  Scenario: Can delete one via PATCH
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have CREATE permissions to collection Zerg
    And document Drone exists in StarCraft/Zerg
    When we PATCH "/v1/namespaces/StarCraft/collections/Zerg/documents"
      """
        [{
          "op": "remove",
          "path": "",
          "value": [{"type": "documents", "id": "Drone"}]
        }]
      """
    Then the response code will be 204
    And the content type will be "application/vnd.api+json; ext=jsonpatch"

  @wip
  Scenario: Can delete many via PATCH
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have CREATE permissions to collection Zerg
    And document Drone exists in StarCraft/Zerg
    And document Roach exists in StarCraft/Zerg
    And document Mutalisk exists in StarCraft/Zerg
    When we PATCH "/v1/namespaces/StarCraft/collections/Zerg/documents"
      """
        [{
          "op": "remove",
          "path": "",
          "value": [
            {"type": "documents", "id": "Drone"},
            {"type": "documents", "id": "Roach"},
            {"type": "documents", "id": "Mutalisk"},
          ]
        }]
      """
    Then the response code will be 204
    And the content type will be "application/vnd.api+json; ext=jsonpatch"
