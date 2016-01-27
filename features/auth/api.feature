Feature: Auth error handling

  Scenario Outline: Bad Data
    When we POST "/v1/auth"
    """
      <DATA>
    """
    Then the response code will be 400
    And the response will contain
      """
        {
          "errors": [{
            "code": "400",
            "status": "400",
            "title": "Malformed data",
            "detail": "Malformed data"
          }]
        }
      """

    Examples:
      | DATA      |
      | {}        |
      | 12        |
      | "foo"     |
      | {"x":"y"} |


  Scenario Outline: Only responds to POSTS
    When we <METHOD> "/v1/auth"
    """
      {
        "attributes": {
          "provider": "jam",
          "username": "user",
          "password": "password"
        }
      }
    """
    Then the response code will be 405
    And the response will contain
      """
        {
          "errors": [{
            "status": "405",
            "detail": "Method Not Allowed"
          }]
        }
      """

    Examples:
      | METHOD |
      | GET    |
      | PUT    |
      | PATCH  |
      | DELETE |
