Feature: Listing Documents

  Scenario: Document id return value
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
    When we GET "/v1/id/collections/StarCraft.Protoss/documents"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
          "id": "StarCraft.Protoss.Archon",
          "attributes": {
            "psi": 4,
            "hp": 10,
            "shields": 350
          }
        }, {
          "id": "StarCraft.Protoss.Probe",
          "attributes": {
            "psi": 1,
            "hp": 20,
            "shields": 20
          }
        }, {
          "id": "StarCraft.Protoss.Zealot",
          "attributes": {
            "psi": 2,
            "hp": 100,
            "shields": 60
          }
        }],
        "meta": {
          "total": 3
        }
      }
      """


  Scenario: Filter documents
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
    When we GET "/v1/id/collections/StarCraft.Protoss/documents?filter[psi]=2"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
          "id": "StarCraft.Protoss.Zealot",
          "attributes": {
            "psi": 2,
            "hp": 100,
            "shields": 60
          }
        }],
        "meta": {
          "total": 1
        }
      }
      """


  Scenario: Sort documents default ascending
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
      When we GET "/v1/id/collections/StarCraft.Protoss/documents?sort=hp"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
          "id": "StarCraft.Protoss.Archon",
          "attributes": {
            "psi": 4,
            "hp": 10,
            "shields": 350
          }
        }, {
          "id": "StarCraft.Protoss.Probe",
          "attributes": {
            "psi": 1,
            "hp": 20,
            "shields": 20
          }
        }, {
          "id": "StarCraft.Protoss.Zealot",
          "attributes": {
            "psi": 2,
            "hp": 100,
            "shields": 60
          }
        }],
        "meta": {
          "total": 3
        }
      }
      """


  Scenario: Sort documents ascending
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
    When we GET "/v1/id/collections/StarCraft.Protoss/documents?sort=+psi"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
          "id": "StarCraft.Protoss.Probe",
          "attributes": {
            "psi": 1,
            "hp": 20,
            "shields": 20
          }
        }, {
          "id": "StarCraft.Protoss.Zealot",
          "attributes": {
            "psi": 2,
            "hp": 100,
            "shields": 60
          }
        }, {
          "id": "StarCraft.Protoss.Archon",
          "attributes": {
            "psi": 4,
            "hp": 10,
            "shields": 350
          }
        }],
        "meta": {
          "total": 3
        }
      }
      """


  Scenario: Sort documents decending
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
    When we GET "/v1/id/collections/StarCraft.Protoss/documents?sort=-shields"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": [{
          "id": "StarCraft.Protoss.Archon",
          "attributes": {
            "psi": 4,
            "hp": 10,
            "shields": 350
          }
        }, {
          "id": "StarCraft.Protoss.Zealot",
          "attributes": {
            "psi": 2,
            "hp": 100,
            "shields": 60
          }
        }, {
          "id": "StarCraft.Protoss.Probe",
          "attributes": {
            "psi": 1,
            "hp": 20,
            "shields": 20
          }
        }],
        "meta": {
          "total": 3
        }
      }
      """


  Scenario: Sort on bad key
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
    When we GET "/v1/id/collections/StarCraft.Protoss/documents?sort=-armo:r"
    Then the response code will be 400


  Scenario: Sort on non-existant key
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
    When we GET "/v1/id/collections/StarCraft.Protoss/documents?sort=-armor"
    Then the response code will be 200
    And the response will contain
      """
      {
        "meta": {
          "total": 3
        }
      }
      """


  Scenario: Filter on non-existant key
    Given namespace StarCraft exists
    And we have ADMIN permissions to namespace StarCraft
    And collection Protoss exists in namespace StarCraft
    And document Probe exists in StarCraft/Protoss
      """
      {
        "psi": 1,
        "hp": 20,
        "shields": 20
      }
      """
    And document Zealot exists in StarCraft/Protoss
      """
      {
        "psi": 2,
        "hp": 100,
        "shields": 60
      }
      """
    And document Archon exists in StarCraft/Protoss
      """
      {
        "psi": 4,
        "hp": 10,
        "shields": 350
      }
      """
    When we GET "/v1/id/collections/StarCraft.Protoss/documents?filter[armor]=10"
    Then the response code will be 200
    And the response will contain
      """
      {
        "meta": {
          "total": 0
        }
      }
      """
