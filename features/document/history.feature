Feature: Viewing document history

  Scenario: Has create entry
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    And the next ObjectIds will be pylons
    And document Larvae exists in StarCraft.Zerg
    When we GET "/v1/id/documents/StarCraft.Zerg.Larvae/history"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": [{
          "id": "StarCraft.Zerg.Larvae.pylons",
          "type": "history",
          "attributes": {
            "operation": "CREATE",
            "parameters": {},
            "record-id": "Larvae"
          },
          "relationships": {},
          "meta": {
            "permissions": "ADMIN",
            "created-by": "user-testing-system",
            "created-on": "2015-01-01T00:00:00",
            "modified-by": "user-testing-system",
            "modified-on": "2015-01-01T00:00:00"
          }
        }],
        "links": {},
        "meta": {"perPage": 50, "total": 1}
      }
      """
