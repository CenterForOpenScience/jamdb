Feature: Listing collections

  Scenario: Namespace permission trickles
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    And collection Zerg exists in namespace StarCraft
    When we GET "/v1/namespaces/StarCraft/collections"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }, {
            "id": "StarCraft.Zerg",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }]
      }
      """


  Scenario: Collection permissions suffucient
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to collection Zerg
    And we have ADMIN permissions to collection Terran
    When we GET "/v1/namespaces/StarCraft/collections"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }, {
            "id": "StarCraft.Zerg",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }]
      }
      """


  Scenario: Collection permissions sufficient
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to collection Zerg
    And we have ADMIN permissions to collection Terran
    When we GET "/v1/namespaces/StarCraft/collections"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }, {
            "id": "StarCraft.Zerg",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }]
      }
      """


  Scenario: Collections filtered by permission
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to collection Zerg
    When we GET "/v1/namespaces/StarCraft/collections"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft.Zerg",
            "type": "collections",
            "attributes": {
              "permissions": {}
            }
        }]
      }
      """

  Scenario: Empty when no access
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to collection Zerg
    When we GET "/v1/namespaces/StarCraft/collections"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": []
      }
      """


  Scenario: No auth 403
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And collection Zerg exists in namespace StarCraft
    And we are not logged in
    When we GET "/v1/namespaces/StarCraft/collections"
    Then the response code will be 401


  Scenario: 403 with insufficient access
    Given namespace StarCraft exists
    When we GET "/v1/id/namespaces/WarCraft/collections"
    Then the response code will be 404
