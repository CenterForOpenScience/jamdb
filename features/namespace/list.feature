Feature: Listing namespaces

  Scenario: See one with ADMIN
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    When we GET "/v1/namespaces"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "ADMIN"
              }
            }
        }]
      }
      """

  Scenario: See only ADMIN
    Given namespace StarCraft exists
    And namespace WarCraft exists
    And we have READ permissions to namespace WarCraft
    And we have ADMIN permissions to namespace StarCraft
    When we GET "/v1/namespaces"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "ADMIN"
              }
            }
        }]
      }
      """

  Scenario: See many ADMIN
    Given namespace WarCraft exists
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace WarCraft
    And we have ADMIN permissions to namespace StarCraft
    When we GET "/v1/namespaces"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
            "id": "StarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "ADMIN"
              }
            }
          },{
            "id": "WarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "ADMIN"
              }
            }
        }]
      }
      """

  Scenario: No auth sees nothing
    Given namespace WarCraft exists
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace WarCraft
    And we have ADMIN permissions to namespace StarCraft
    And we are not logged in
    When we GET "/v1/namespaces"
    Then the response code will be 200
    And the response will be
      """
        {
          "data": [],
          "meta": {
            "total": 0,
            "perPage": 50
          },
          "links": {}
        }
      """
