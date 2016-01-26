Feature: Global API Features

  Scenario Outline: Incorrect types are rejected
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document Drone exists in StarCraft/Zerg
    And we have ADMIN permissions to namespace StarCraft
    When we <METHOD> "<URL>"
      """
        {
          "data": {
            "id": "<ID>",
            "attributes": {},
            "type": <TYPE>
          }
        }
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "detail": <DETAIL>
          }]
        }
      """

    Examples: Cases
      | METHOD | URL                                                       | ID        | TYPE         | DETAIL |
      | PATCH  | /v1/namespaces/StarCraft                                  | StarCraft | "namespace"  | empty  |
      | PATCH  | /v1/namespaces/StarCraft                                  | StarCraft | 12           | empty  |
      | PATCH  | /v1/namespaces/StarCraft                                  | StarCraft | null         | empty  |
      | PATCH  | /v1/namespaces/StarCraft                                  | StarCraft | {}           | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/                     | Protoss   | "collection" | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/                     | Protoss   | 12           | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/                     | Protoss   | null         | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/                     | Protoss   | {}           | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Zerg      | "collection" | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Zerg      | 12           | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Zerg      | null         | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Zerg      | {}           | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Overlord  | "collection" | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Overlord  | 12           | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Overlord  | null         | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Overlord  | {}           | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Drone     | "collection" | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Drone     | 12           | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Drone     | null         | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Drone     | {}           | empty  |


  Scenario Outline: Non-matching Ids are rejected
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document Drone exists in StarCraft/Zerg
    And we have ADMIN permissions to namespace StarCraft
    When we <METHOD> "<URL>"
      """
        {
          "data": {
            "id": "<ID>",
            "attributes": {},
            "type": "<TYPE>"
          }
        }
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "detail": <DETAIL>
          }]
        }
      """

    Examples: Cases
      | METHOD | URL                                                       | ID        | TYPE        | DETAIL |
      | PATCH  | /v1/namespaces/StarCraft                                  | WarCraft  | namespaces  | empty  |
      | PATCH  | /v1/namespaces/StarCraft                                  | WarCraft  | namespaces  | empty  |
      | PATCH  | /v1/namespaces/StarCraft                                  | WarCraft  | namespaces  | empty  |
      | PATCH  | /v1/namespaces/StarCraft                                  | WarCraft  | namespaces  | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Protoss   | collections | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Protoss   | collections | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Protoss   | collections | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                 | Protoss   | collections | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Drone     | documents   | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Drone     | documents   | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Drone     | documents   | empty  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents       | Drone     | documents   | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Overlord  | documents   | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Overlord  | documents   | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Overlord  | documents   | empty  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone | Overlord  | documents   | empty  |



  @wip
  Scenario Outline: Ids must be valid
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document Drone exists in StarCraft/Zerg
    And we have ADMIN permissions to namespace StarCraft
    When we POST "<URL>"
      """
        {
          "data": {
            "id": <ID>,
            "attributes": {},
            "type": "<TYPE>"
          }
        }
      """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "code": "400",
            "status": "400",
            "title": "Invalid id",
            "detail": "Expected detail to match the Regex [\\d\\w\\-]{3,64}, optionally prefixed by its parents ids seperated via ."
          }]
        }
      """

    Examples: Cases
      | URL                                                       | ID                      | TYPE        |
      | /v1/namespaces/StarCraft/collections/                     | "Inv#alid"              | collections |
      | /v1/namespaces/StarCraft/collections/                     | 12                      | collections |
      | /v1/namespaces/StarCraft/collections/                     | {}                      | collections |
      | /v1/namespaces/StarCraft/collections/                     | "Wrong.Parents"         | collections |
      | /v1/namespaces/StarCraft/collections/                     | "StarCraft.Inva#lid"    | collections |
      | /v1/namespaces/StarCraft/collections/                     | "StarCraft.In$a#lid"    | collections |
      | /v1/namespaces/StarCraft/collections/                     | "Still..invalid."       | collections |
      | /v1/namespaces/StarCraft/collections/                     | ""                      | collections |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | "Inv#alid"              | documents   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | 12                      | documents   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | {}                      | documents   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | ""                      | documents   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | "StarCraft.Inva#lid"    | documents   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | "StarCraft.In$a#lid"    | documents   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents       | "Still..invalid."       | documents   |
