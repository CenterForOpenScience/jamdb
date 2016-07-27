Feature: Collection plugins

  Scenario: Plugin must be active
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    When we GET "/v1/id/collections/StarCraft.Terran/user"
    Then the response code will be 412
    And the response will be
      """
      {
        "errors": [{
          "code": "412",
          "status": "412",
          "title": "Plugin not enabled",
          "detail": "Plugin \"user\" is not enabled on this collection"
        }]
      }
      """

  Scenario: Implicit plugins
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    When we GET "/v1/id/collections/StarCraft.Terran/_search"
    Then the response code will be 400
    And the response will be
      """
      {
        "errors": [{
          "code": "400",
          "status": "400",
          "title": "Bad Request",
          "detail": "This collection does not support searching"
        }]
      }
      """

  Scenario: Plugin schemas (Good)
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/id/collections/StarCraft.Terran"
      """
      [{
        "op": "add",
        "path": "/plugins/user",
        "value": {
          "createdIsOwner": true
        }
      }]
      """
    Then the response code will be 200

  Scenario: Plugin schemas (Bad)
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/id/collections/StarCraft.Terran"
      """
      [{
        "op": "add",
        "path": "/plugins/user",
        "value": {
          "Additional": "key",
          "creatorIsOwner": true
        }
      }]
      """
    Then the response code will be 400

  Scenario: No such plugin
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    When we GET "/v1/id/collections/StarCraft.Terran/fixitol"
    Then the response code will be 404
    # And the response will be
    #   """
    #   {
    #     "errors": [{
    #       "code": "404",
    #       "status": "404",
    #       "title": "No such plugin",
    #       "detail": "Plugin \"fixitol\" does not exist"
    #     }]
    #   }
    #   """
    #

  Scenario: Plugin info
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Terran exists in namespace StarCraft
    And the user plugin is enabled for collection StarCraft.Terran
      """
      {
          "createdIsOwner": true
      }
      """
    When we GET "/v1/id/collections/StarCraft.Terran"
    Then the response code will be 200
    And the response will be
      """
      {
        "data": {
            "id": "StarCraft.Terran",
            "type": "collections",
            "attributes": {
              "name": "Terran",
              "schema": null,
              "plugins": {
                "user": {
                  "createdIsOwner": true
                }
              },
              "permissions": {
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
                  "self": "http://localhost:50325/v1/id/namespaces/StarCraft",
                  "related": "http://localhost:50325/v1/id/namespaces/StarCraft"
                }
              },
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/id/collections/StarCraft.Terran/documents",
                  "related": "http://localhost:50325/v1/id/collections/StarCraft.Terran/documents"
                }
              }
            }
          }
      }
      """

