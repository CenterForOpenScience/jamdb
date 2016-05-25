Feature: Getting a collection
  Scenario: Collection does not exist
    Given namespace life does exist
    When we GET "/v1/namespaces/life/collections/happiness"
    Then the response code will be 404
    And the response will contain
      """
        {
          "errors": [{
            "code": "C404",
            "status": "404",
            "title": "Collection not found",
            "detail": "Collection \"happiness\" was not found in namespace \"life\""
          }]
        }
      """

  Scenario Outline: Insuffcient permissions to namespace
    Given namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have <permission> permissions to collection additional-pylons
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 403
    And the response will contain
      """
        {
          "errors": [{
            "code": "403",
            "status": "403",
            "title": "Forbidden",
            "detail": "READ permission or higher is required to perform this action"
          }]
        }
        """

    Examples: Permissions
      | permission |
      | CREATE     |
      | UPDATE     |
      | DELETE     |

  Scenario Outline: Namespace permissions trickle
    Given namespace construct exists
    And we have <permission> permissions to namespace construct
    And collection additional-pylons exists in namespace construct
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 200

    Examples: Permissions
      | permission |
      | ADMIN      |
      | READ       |
      | CRUD       |
      | READ_WRITE |

  Scenario Outline: Collection hierachical return value ADMIN on collection
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have ADMIN permissions to collection additional-pylons
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "construct.additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "schema": null,
              "plugins": {},
              "permissions": {
                "user-testing-we": "ADMIN",
                "user-testing-system": "ADMIN"
              }
            },
            "meta": {
              "permissions": "ADMIN",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "namespace": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct",
                  "related": "http://localhost:50325/v1/namespaces/construct"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents",
                  "related": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents"
                }
              }
            }
          }
      }
      """

  Scenario Outline: Collection hierachical return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have <PERMISSION> permissions to namespace construct
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "construct.additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "schema": null,
              "plugins": {},
              "permissions": {
                "user-testing-system": "ADMIN"
              }
            },
            "meta": {
              "permissions": "<PERMISSION>",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "namespace": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct",
                  "related": "http://localhost:50325/v1/namespaces/construct"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents",
                  "related": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents"
                }
              }
            }
          }
      }
      """

    Examples:
      | PERMISSION |
      | ADMIN      |
      | READ       |
      | RD         |
      | RU         |
      | RUD        |
      | CRU        |
      | CRUD       |

  Scenario Outline: Collection hierachical return value not ADMIN
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have <PERMISSION> permissions to <RESOURCE_TYPE> <RESOURCE>
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "construct.additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "schema": null
            },
            "meta": {
              "permissions": "READ",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "namespace": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct",
                  "related": "http://localhost:50325/v1/namespaces/construct"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents",
                  "related": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents"
                }
              }
            }
          }
      }
      """

    Examples:
      | PERMISSION | RESOURCE_TYPE | RESOURCE          |
      # | READ       | namespace     | construct         |
      # | RD         | namespace     | construct         |
      # | RU         | namespace     | construct         |
      # | RUD        | namespace     | construct         |
      # | CRU        | namespace     | construct         |
      # | CRUD       | namespace     | construct         |
      | READ       | collection    | additional-pylons |
      | RD         | collection    | additional-pylons |
      | RU         | collection    | additional-pylons |
      | RUD        | collection    | additional-pylons |
      | CRU        | collection    | additional-pylons |
      | CRUD       | collection    | additional-pylons |

  Scenario: Collection id return value ADMIN on collection
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have ADMIN permissions to collection additional-pylons
    When we GET "/v1/id/collections/construct.additional-pylons"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "construct.additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "schema": null,
              "plugins": {},
              "permissions": {
                "user-testing-we": "ADMIN",
                "user-testing-system": "ADMIN"
              }
            },
            "meta": {
              "permissions": "ADMIN",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "namespace": {
                "links": {
                  "self": "http://localhost:50325/v1/id/namespaces/construct",
                  "related": "http://localhost:50325/v1/id/namespaces/construct"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/id/collections/construct.additional-pylons/documents",
                  "related": "http://localhost:50325/v1/id/collections/construct.additional-pylons/documents"
                }
              }
            }
          }
      }
      """

  Scenario Outline: Collection id return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have <PERMISSION> permissions to namespace construct
    When we GET "/v1/id/collections/construct.additional-pylons"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "construct.additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "schema": null,
              "plugins": {},
              "permissions": {
                "user-testing-system": "ADMIN"
              }
            },
            "meta": {
              "permissions": "<PERMISSION>",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "namespace": {
                "links": {
                  "self": "http://localhost:50325/v1/id/namespaces/construct",
                  "related": "http://localhost:50325/v1/id/namespaces/construct"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/id/collections/construct.additional-pylons/documents",
                  "related": "http://localhost:50325/v1/id/collections/construct.additional-pylons/documents"
                }
              }
            }
          }
      }
      """

    Examples:
      | PERMISSION |
      | ADMIN      |
      | READ       |
      | RD         |
      | RU         |
      | RUD        |
      | CRU        |
      | CRUD       |

  Scenario Outline: Collection id return value not ADMIN
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have <PERMISSION> permissions to <RESOURCE_TYPE> <RESOURCE>
    When we GET "/v1/id/collections/construct.additional-pylons"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "construct.additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "schema": null
            },
            "meta": {
              "permissions": "READ",
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "namespace": {
                "links": {
                  "self": "http://localhost:50325/v1/id/namespaces/construct",
                  "related": "http://localhost:50325/v1/id/namespaces/construct"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/id/collections/construct.additional-pylons/documents",
                  "related": "http://localhost:50325/v1/id/collections/construct.additional-pylons/documents"
                }
              }
            }
          }
      }
      """

    Examples:
      | PERMISSION | RESOURCE_TYPE | RESOURCE          |
      | READ       | collection    | additional-pylons |
      | RD         | collection    | additional-pylons |
      | RU         | collection    | additional-pylons |
      | RUD        | collection    | additional-pylons |
      | CRU        | collection    | additional-pylons |
      | CRUD       | collection    | additional-pylons |
