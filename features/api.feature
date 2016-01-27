Feature: Global API Features

  @wip
  Scenario Outline: Endpoint Fuzzing
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document drone exists in StarCraft/Zerg
    And we have ADMIN permissions to namespace StarCraft
    When we <METHOD> "<URL>"
      """
        <DATA>
      """
    Then the response code will be <CODE>

    Examples: Cases
      | METHOD | URL                                                               | CODE | DATA            |
      | POST   | /v1/namespaces                                                    | 400  | 2               |
      | POST   | /v1/namespaces                                                    | 400  | {}              |
      | POST   | /v1/namespaces                                                    | 400  | "Datum"         |
      | POST   | /v1/namespaces                                                    | 400  | not json        |
      | POST   | /v1/namespaces                                                    | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces                                                    | 400  | 2               |
      | PATCH  | /v1/namespaces                                                    | 501  | {}              |
      | PATCH  | /v1/namespaces                                                    | 501  | {"data": 4}     |
      | PATCH  | /v1/namespaces                                                    | 501  | {"data": {}}    |
      | PATCH  | /v1/namespaces                                                    | 501  | {"data": "str"} |
      | PATCH  | /v1/namespaces                                                    | 400  | "Datum"         |
      | PATCH  | /v1/namespaces                                                    | 400  | not json        |
      | PATCH  | /v1/namespaces                                                    | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces                                                    | 400  | 2               |
      | PUT    | /v1/namespaces                                                    | 501  | {}              |
      | PUT    | /v1/namespaces                                                    | 400  | "Datum"         |
      | PUT    | /v1/namespaces                                                    | 400  | not json        |
      | PUT    | /v1/namespaces                                                    | 400  | 84ni013*)       |
      | POST   | /v1/namespaces/StarCraft                                          | 400  | 2               |
      | POST   | /v1/namespaces/StarCraft                                          | 405  | {}              |
      | POST   | /v1/namespaces/StarCraft                                          | 400  | "Datum"         |
      | POST   | /v1/namespaces/StarCraft                                          | 400  | not json        |
      | POST   | /v1/namespaces/StarCraft                                          | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | 2               |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | {}              |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | {"data": 4}     |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | {"data": {}}    |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | {"data": "str"} |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | "Datum"         |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | not json        |
      | PATCH  | /v1/namespaces/StarCraft                                          | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces/StarCraft                                          | 400  | 2               |
      | PUT    | /v1/namespaces/StarCraft                                          | 501  | {}              |
      | PUT    | /v1/namespaces/StarCraft                                          | 400  | "Datum"         |
      | PUT    | /v1/namespaces/StarCraft                                          | 400  | not json        |
      | PUT    | /v1/namespaces/StarCraft                                          | 400  | 84ni013*)       |
      | POST   | /v1/namespaces/StarCraft/collections                              | 400  | 2               |
      | POST   | /v1/namespaces/StarCraft/collections                              | 400  | {}              |
      | POST   | /v1/namespaces/StarCraft/collections                              | 400  | "Datum"         |
      | POST   | /v1/namespaces/StarCraft/collections                              | 400  | not json        |
      | POST   | /v1/namespaces/StarCraft/collections                              | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | 2               |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | {}              |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | {"data": 4}     |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | {"data": {}}    |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | {"data": "str"} |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | "Datum"         |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | not json        |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces/StarCraft/collections                              | 400  | 2               |
      | PUT    | /v1/namespaces/StarCraft/collections                              | 501  | {}              |
      | PUT    | /v1/namespaces/StarCraft/collections                              | 400  | "Datum"         |
      | PUT    | /v1/namespaces/StarCraft/collections                              | 400  | not json        |
      | PUT    | /v1/namespaces/StarCraft/collections                              | 400  | 84ni013*)       |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | 2               |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | {}              |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | "Datum"         |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | not json        |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | 2               |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | {}              |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | {"data": 4}     |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | {"data": {}}    |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | {"data": "str"} |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | "Datum"         |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | not json        |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | 2               |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg                         | 501  | {}              |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | "Datum"         |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | not json        |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg                         | 400  | 84ni013*)       |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | 2               |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | {}              |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | "Datum"         |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | not json        |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | 2               |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | {}              |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | {"data": 4}     |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | {"data": {}}    |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | {"data": "str"} |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | "Datum"         |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | not json        |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | 2               |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents               | 501  | {}              |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | "Datum"         |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | not json        |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents               | 400  | 84ni013*)       |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | 2               |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | {}              |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | "Datum"         |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | not json        |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | 2               |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | {}              |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | {"data": 4}     |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | {"data": {}}    |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | {"data": "str"} |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | "Datum"         |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | not json        |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | 2               |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 501  | {}              |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | "Datum"         |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | not json        |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone         | 400  | 84ni013*)       |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | 2               |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | {}              |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | "Datum"         |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | not json        |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | 84ni013*)       |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | 2               |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | {}              |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | {"data": 4}     |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | {"data": {}}    |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | {"data": "str"} |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | "Datum"         |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | not json        |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | 84ni013*)       |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | 2               |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 501  | {}              |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | "Datum"         |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | not json        |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 400  | 84ni013*)       |


  Scenario Outline: Many resource points dont respond to DELETE, PATCH or PUT
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document drone exists in StarCraft/Zerg
    And we have ADMIN permissions to namespace StarCraft
    When we <METHOD> "<URL>"
    Then the response code will be <CODE>

    Examples:
      | METHOD | URL                                                               | CODE |
      | DELETE | /v1/namespaces/                                                   | 405  |
      | PUT    | /v1/namespaces/                                                   | 405  |
      | PATCH  | /v1/namespaces/                                                   | 501  |
      | DELETE | /v1/namespaces/StarCraft/collections                              | 405  |
      | PUT    | /v1/namespaces/StarCraft/collections                              | 405  |
      | PATCH  | /v1/namespaces/StarCraft/collections                              | 501  |
      | DELETE | /v1/namespaces/StarCraft/collections/Zerg/documents               | 405  |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents               | 405  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents               | 501  |
      | DELETE | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 405  |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 405  |
      | PATCH  | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history | 501  |


  Scenario Outline: Single resource endpoints dont respond to POST or PUT
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And document drone exists in StarCraft/Zerg
    And we have ADMIN permissions to namespace StarCraft
    When we <METHOD> "<URL>"
    Then the response code will be <CODE>

    Examples:
      | METHOD | URL                                                                         | CODE |
      | POST   | /v1/namespaces/StarCraft                                                    | 405  |
      | PUT    | /v1/namespaces/StarCraft                                                    | 405  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg                                   | 405  |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg                                   | 405  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone                   | 405  |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone                   | 405  |
      | POST   | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history/historyid | 405  |
      | PUT    | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history/historyid | 405  |


  Scenario Outline: All endpoints respond with CORS headers to OPTIONS
    When we OPTIONS "<URL>"
    Then the response code will be 204
    And the headers will contain
    """
      {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET, PUT, PATCH, POST, DELETE",
        "Access-Control-Expose-Headers": "Content-Length, Content-Encoding",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Cache-Control"
      }
    """

    Examples:
      | URL                                                                         |
      | /doesnt/exist                                                               |
      | /v1/auth                                                                    |
      | /v1/namespaces                                                              |
      | /v1/namespaces/StarCraft                                                    |
      | /v1/namespaces/StarCraft/collections                                        |
      | /v1/namespaces/StarCraft/collections/Zerg                                   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents                         |
      | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone                   |
      | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history           |
      | /v1/namespaces/StarCraft/collections/Zerg/documents/Drone/history/historyid |



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
