Feature: Creating a document

  Scenario: Document exists
    Given namespace doomoven exists
    And collection doomstove exists in namespace doomoven
    And we have ADMIN permissions to namespace doomoven
    And document quetzal exists in doomoven/doomstove
    When we create document quetzal in doomoven/doomstove
    Then the response code will be 409
    And the response will contain
    """
      {
        "errors": [{
            "code": "D409",
            "status": "409",
            "title": "Document already exists",
            "detail": "Document \"quetzal\" already exists"
          }]
        }
      """

      # """
      #   {
      #     "errors": [{
      #       "code": "D409",
      #       "status": "409",
      #       "title": "Document already exists",
      #       "detail": "Document \"quetzal\" already exists in collection \"foo\""
      #     }]
      #   }
      #   """

  Scenario: New document
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace meatspace exists
    And collection cow exists in namespace meatspace
    And we have ADMIN permissions to namespace meatspace
    When we create document steak in meatspace/cow
    Then the response code will be 201
    And the response will contain
      """
      {
        "data": {
            "id": "steak",
            "type": "documents",
            "attributes": {},
            "meta": {
              "created-by": "user-testing-we",
              "modified-by": "user-testing-we",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "history": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/meatspace/collections/cow/documents/steak/history",
                  "related": "http://localhost:50325/v1/namespaces/meatspace/collections/cow/documents/steak/history"
                }
              }
            }
          }
        }
      """

  Scenario: New document with data
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace meatspace exists
    And collection cow exists in namespace meatspace
    And we have ADMIN permissions to namespace meatspace
    When we create document steak in meatspace/cow
      """
      {
        "isRare": 1,
        "isCooked": true,
        "isFrozen": "False"
      }
      """
    Then the response code will be 201
    And the response will contain
      """
      {
        "data": {
            "id": "steak",
            "type": "documents",
            "attributes": {
              "isRare": 1,
              "isCooked": true,
              "isFrozen": "False"
            },
            "meta": {
              "created-by": "user-testing-we",
              "modified-by": "user-testing-we",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "history": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/meatspace/collections/cow/documents/steak/history",
                  "related": "http://localhost:50325/v1/namespaces/meatspace/collections/cow/documents/steak/history"
                }
              }
            }
          }
        }
        """


  Scenario Outline: Allowed permissions
    Given namespace meatspace exists
    And collection cow exists in namespace meatspace
    And we have <permission> permissions to <rtype> <resource>
    When we create document steak in meatspace/cow
    Then the response code will be 201

      Examples: Permissions
        | permission | rtype      | resource  |
        | ADMIN      | namespace  | meatspace |
        | CRUD       | namespace  | meatspace |
        | CREATE     | namespace  | meatspace |
        | READ_WRITE | namespace  | meatspace |
        | ADMIN      | collection | cow       |
        | CRUD       | collection | cow       |
        | CREATE     | collection | cow       |
        | READ_WRITE | collection | cow       |


  Scenario Outline: Insufficient permissions
    Given namespace meatspace exists
    And collection cow exists in namespace meatspace
    And we have <permission> permissions to <rtype> <resource>
    When we create document steak in meatspace/cow
    Then the response code will be 403

      Examples: Permissions
        | permission | rtype      | resource  |
        | READ       | namespace  | meatspace |
        | UPDATE     | namespace  | meatspace |
        | DELETE     | namespace  | meatspace |
        | NONE       | namespace  | meatspace |
        | NONE       | collection | cow       |
        | READ       | collection | cow       |
        | UPDATE     | collection | cow       |
        | DELETE     | collection | cow       |

  Scenario Outline: Bad data
    Given namespace meatspace exists
    And collection cow exists in namespace meatspace
    And we have ADMIN permissions to namespace meatspace
    When we POST "/v1/namespaces/meatspace/collections/cow/documents"
      """
      <data>
      """
    Then the response code will be 400
    And the response will contain
      """
      <response>
      """

    Examples:
      | data    | response                                                               |
      | ""      | {"errors":[{"code":"400","status":"400","title":"Malformed data"}]}    |
      | 193     | {"errors":[{"code":"400","status":"400","title":"Malformed data"}]}    |
      | invalid | {"errors":[{"code":"400","status":"400","title":"Malformed data"}]}    |
      | {{{{{}}}}} | {"errors":[{"code":"400","status":"400","title":"Malformed data"}]} |
