Feature: Reading a document

  Scenario: Document does not exist
    Given namespace SHARE exists
    And collection providers exists in namespace SHARE
    And we have ADMIN permissions to namespace SHARE
    When we GET "/v1/namespaces/SHARE/collections/providers/documents/arXiv"
    Then the response code will be 404
    And the response will contain
      """
        {
          "errors": [{
            "code": "D404",
            "status": "404",
            "title": "Document not found",
            "detail": "Document \"arXiv\" was not found"
          }]
        }
        """

  Scenario: Document id return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have READ permissions to namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "hp": 100,
        "hasMinerals": false,
        "statusEffects": [null]
      }
      """
    When we GET "/v1/namespaces/StarCraft/collections/Protoss/documents/Probe"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "StarCraft.Protoss.Probe",
            "type": "documents",
            "attributes": {
              "hp": 100,
              "hasMinerals": false,
              "statusEffects": [null]
            },
            "meta": {
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "history": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/StarCraft/collections/Protoss/documents/Probe/history",
                  "related": "http://localhost:50325/v1/namespaces/StarCraft/collections/Protoss/documents/Probe/history"
                }
              }
            }
          }
        }
        """

  Scenario: Document hierachical return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have READ permissions to namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "hp": 100,
        "hasMinerals": false,
        "statusEffects": [null]
      }
      """
    When we GET "/v1/id/documents/StarCraft.Protoss.Probe"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "StarCraft.Protoss.Probe",
            "type": "documents",
            "attributes": {
              "hp": 100,
              "hasMinerals": false,
              "statusEffects": [null]
            },
            "meta": {
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "history": {
                "links": {
                  "self": "http://localhost:50325/v1/id/documents/StarCraft.Protoss.Probe/history",
                  "related": "http://localhost:50325/v1/id/documents/StarCraft.Protoss.Probe/history"
                }
              }
            }
          }
        }
        """

  Scenario Outline: Insufficient permissions
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have <permission> permissions to <rtype> <resource>
    And document Probe exists in StarCraft/Protoss
    When we GET "/v1/namespaces/StarCraft/collections/Protoss/documents/Probe"
    Then the response code will be 403

    Examples:
    | permission | rtype      | resource   |
    | NONE       | namespace  | StarCraft  |
    | UPDATE     | namespace  | StarCraft  |
    | DELETE     | namespace  | StarCraft  |
    | CREATE     | namespace  | StarCraft  |
    | DELETE     | namespace  | StarCraft  |
    | NONE       | collection | Protoss    |
    | UPDATE     | collection | Protoss    |
    | DELETE     | collection | Protoss    |
    | CREATE     | collection | Protoss    |
    | DELETE     | collection | Protoss    |

  Scenario Outline: Sufficient permissions
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have <permission> permissions to <rtype> <resource>
    And document Probe exists in StarCraft/Protoss
    When we GET "/v1/namespaces/StarCraft/collections/Protoss/documents/Probe"
    Then the response code will be 200

    Examples:
    | permission | rtype      | resource   |
    | READ       | namespace  | StarCraft  |
    | READ       | collection | Protoss    |

  Scenario: Creator can read document
    Given namespace StarCraft exists
    And collection Protoss exists in namespace StarCraft
    And we have CREATE permissions to collection Protoss
    When we create document Probe in StarCraft/Protoss
    And we GET "/v1/namespaces/StarCraft/collections/Protoss/documents/Probe"
    Then the response code will be 200
