Feature: Updating a document

  Scenario: Missing document
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And we have UPDATE permissions to collection Terran
    When we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/SCV"
    Then the response code will be 404

  Scenario: Deleted document
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And document SCV exists in StarCraft/Terran
    And we have CRUD permissions to collection Terran
    When we DELETE "/v1/namespaces/StarCraft/collections/Terran/documents/SCV"
    And we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/SCV"
    Then the response code will be 404

  Scenario: Add Field
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And document Raven exists in StarCraft/Terran
    And we have CRUD permissions to collection Terran
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/Raven"
    """
      [{
          "op": "add",
          "path": "/Health",
          "value": 180
      }]
    """
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": {
            "id": "StarCraft.Terran.Raven",
            "type": "documents",
            "attributes": {
              "Health": 180
            }
          }
        }
      """

  Scenario: Via document
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And document Raven exists in StarCraft/Terran
    And we have CRUD permissions to collection Terran
    When we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/Raven"
    """
      {
        "data": {
            "id": "StarCraft.Terran.Raven",
            "type": "documents",
            "attributes": {
              "Health": 180
            }
          }
      }
    """
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": {
            "id": "StarCraft.Terran.Raven",
            "type": "documents",
            "attributes": {
              "Health": 180
            }
          }
        }
      """

  Scenario: Document can not be used with jsonpatch extension
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And document Raven exists in StarCraft/Terran
    And we have CRUD permissions to collection Terran
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/Raven"
    """
      {
        "data": {
            "id": "StarCraft.Terran.Raven",
            "type": "documents",
            "attributes": {
              "Health": 180
            }
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
            "title": "Invalid type",
            "detail": "Expected field  to be of type List. Got Object"
          }]
        }
      """

  Scenario: Multiple Operation
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And document Raven exists in StarCraft/Terran
    And we have CRUD permissions to collection Terran
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/Raven"
    """
      [{
          "op": "add",
          "path": "/Health",
          "value": 180
      },{
          "op": "add",
          "path": "/Defence",
          "value": 12
      }]
    """
    Then the response code will be 200
    And the response will contain
      """
        {
          "data": {
            "id": "StarCraft.Terran.Raven",
            "type": "documents",
            "attributes": {
              "Health": 180,
              "Defence": 12
            }
          }
        }
      """

  Scenario: Failed test
    Given namespace StarCraft exists
    And collection Terran exists in namespace StarCraft
    And document Raven exists in StarCraft/Terran
    And we have CRUD permissions to collection Terran
    When the content type is application/vnd.api+json; ext="jsonpatch";
    And we PATCH "/v1/namespaces/StarCraft/collections/Terran/documents/Raven"
    """
      [{
          "op": "test",
          "path": "/Health",
          "value": 180
      },{
          "op": "add",
          "path": "/Defence",
          "value": 12
      }]
    """
    Then the response code will be 412
    And the response will contain
    """
      {
        "errors": [{
            "code": "412",
            "status": "412",
            "title": "Json patch test failed",
            "detail": "member 'Health' not found in {}"
        }]
      }
    """
