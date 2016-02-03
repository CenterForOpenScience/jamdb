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

  Scenario Outline: See only see READ
    Given namespace StarCraft exists
    And namespace WarCraft exists
    And we have <PERMISSIONS1> permissions to namespace WarCraft
    And we have <PERMISSIONS2> permissions to namespace StarCraft
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
                "user-testing-we": "<PERMISSIONS2>"
              }
            }
        }]
      }
      """

    Examples:
      | PERMISSIONS1 | PERMISSIONS2 |
      | CREATE       | READ         |
      | CU           | READ         |
      | UPDATE       | READ         |
      | DELETE       | READ         |
      | CUD          | READ         |
      | CD           | READ         |


  Scenario Outline: See many with at least READ access
    Given namespace WarCraft exists
    And namespace StarCraft exists
    And we have <PERMISSIONS> permissions to namespace WarCraft
    And we have <PERMISSIONS> permissions to namespace StarCraft
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
                "user-testing-we": "<PERMISSIONS>"
              }
            }
          },{
            "id": "WarCraft",
            "type": "namespaces",
            "attributes": {
              "permissions": {
                "user-testing-we": "<PERMISSIONS>"
              }
            }
        }]
      }
      """

    Examples:
      | PERMISSIONS |
      | READ        |
      | ADMIN       |
      | RUD         |
      | RU          |
      | CRU         |
      | RD          |


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
