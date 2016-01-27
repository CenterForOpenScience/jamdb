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
