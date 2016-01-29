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
            "id": "meatspace.cow.steak",
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
            "id": "meatspace.cow.steak",
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

  @wip
  Scenario: Bulk document creation
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace things-that-make-me exists
    And collection happy exists in namespace things-that-make-me
    And we have ADMIN permissions to namespace things-that-make-me
    When the content type is application/vnd.api+json; ext="bulk";
    When we POST "/v1/namespaces/things-that-make-me/collections/happy/documents"
      """
      {
        "data": [
          {
            "id": "Nothing",
            "type": "documents",
            "attributes": {}
          }
        ]
      }
      """
    Then the response code will be 201
    And the response will contain
      """
      {
        "errors": [null],
        "data": [{
            "id": "things-that-make-me.happy.Nothing",
            "type": "documents",
            "attributes": {
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
                  "self": "http://localhost:50325/v1/namespaces/things-that-make-me/collections/happy/documents/Nothing/history",
                  "related": "http://localhost:50325/v1/namespaces/things-that-make-me/collections/happy/documents/Nothing/history"
                }
              }
            }
          }]
        }
        """

  Scenario: Bulk document creation missing extension
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace things-that-make-me exists
    And collection happy exists in namespace things-that-make-me
    And we have ADMIN permissions to namespace things-that-make-me
    When the content type is application/vnd.api+json;
    When we POST "/v1/namespaces/things-that-make-me/collections/happy/documents"
      """
      {
        "data": [
          {
            "id": "Nothing",
            "type": "documents",
            "attributes": {}
          }
        ]
      }
      """
    Then the response code will be 415
    And the response will contain
      """
      {
        "errors": [{
            "code": "415",
            "status": "415",
            "title": "Missing extension",
            "detail": "Expected Content-Type to contain ext=\"bulk\";"
        }]
      }
      """

  Scenario: Bulk document creation with bad data
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace things-that-make-me exists
    And collection happy exists in namespace things-that-make-me
    And we have ADMIN permissions to namespace things-that-make-me
    When the content type is application/vnd.api+json; ext="bulk";
    When we POST "/v1/namespaces/things-that-make-me/collections/happy/documents"
      """
      {
        "data": [
          {
            "id": "NotMuch",
            "type": "documents",
            "attributes": {}
          }, {
            "type": "documents"
          }, {
            "id": "Nothing",
            "type": "documents",
            "attributes": {}
          }
        ]
      }
      """
    Then the response code will be 201
    And the response will contain
      """
      {
      "errors": [null, {"detail": "Malformed data", "title": "Malformed data", "status": "400", "code": "400"}, null],
      "data": [{
            "id": "things-that-make-me.happy.NotMuch",
            "type": "documents",
            "attributes": {
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
                  "self": "http://localhost:50325/v1/namespaces/things-that-make-me/collections/happy/documents/NotMuch/history",
                  "related": "http://localhost:50325/v1/namespaces/things-that-make-me/collections/happy/documents/NotMuch/history"
                }
              }
            }
          },
          null,
          {
            "id": "things-that-make-me.happy.Nothing",
            "type": "documents",
            "attributes": {
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
                  "self": "http://localhost:50325/v1/namespaces/things-that-make-me/collections/happy/documents/Nothing/history",
                  "related": "http://localhost:50325/v1/namespaces/things-that-make-me/collections/happy/documents/Nothing/history"
                }
              }
            }
          }]
        }
        """

  # Scenario: Can create single via PATCH
  #   Given namespace StarCraft exists
  #   And collection Zerg exists in namespace StarCraft
  #   And we have CRUD permissions to collection Zerg
  #   When we PATCH "/v1/namespaces/StarCraft/collections/Zerg/documents"
  #   """
  #     [{
  #       "data": [{
  #         "id": "Zergling",
  #         "type": "documents",
  #         "attributes": {
  #           "Health": 100
  #         }
  #       }]
  #     }]
  #   """
  #   Then the response code will be 200
  #   And the content type will be "application/vnd.api+json; ext=jsonpatch"
  #   And the response will contain
  #   """
  #     [{
  #       "data": [{
  #         "id": "Zergling",
  #         "type": "documents",
  #         "attributes": {
  #           "Health": 100
  #         }
  #       }]
  #     }]
  #     """

  # Scenario: Can create many via PATCH
  #   Given namespace StarCraft exists
  #   And collection Zerg exists in namespace StarCraft
  #   And we have CRUD permissions to collection Zerg
  #   When we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents"
  #   """
  #     [{
  #       "data": [{
  #         "id": "Roach",
  #         "type": "documents",
  #         "attributes": {
  #           "Health": 110
  #         }
  #       }]
  #     }, {
  #       "data": [{
  #         "id": "Baneling",
  #         "type": "documents",
  #         "attributes": {
  #           "Health": 80
  #         }
  #       }]
  #     }]
  #   """
  #   Then the response code will be 200
  #   And the content type will be "application/vnd.api+json; ext=jsonpatch"
  #   And the response will contain
  #   """
  #     [{
  #       "data": [{
  #         "id": "Marine",
  #         "type": "documents",
  #         "attributes": {
  #           "Health": 110
  #         }
  #       }]
  #     }, {
  #       "data": [{
  #         "id": "Reaper",
  #         "type": "documents",
  #         "attributes": {
  #           "Health": 80
  #         }
  #       }]
  #     }]
  #     """

  Scenario: Invalid Id
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When we create document foo.bar in StarCraft/Zerg
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "code": "400",
            "status": "400",
            "title": "Invalid id",
            "detail": "Expected data.id to match the Regex [\\d\\w\\-]{3,64}, optionally prefixed by its parents ids seperated via ."
          }]
        }
      """

  Scenario: Parent Ids
    Given namespace StarCraft exists
    And collection Zerg exists in namespace StarCraft
    And we have ADMIN permissions to namespace StarCraft
    When we create document StarCraft.Zerg.Baneling in StarCraft/Zerg
    Then the response code will be 201
