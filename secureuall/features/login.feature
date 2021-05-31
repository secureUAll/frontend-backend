
  Feature: Welcome page interaction

    Scenario: New user welcome page presents form
      Given browser at "/login"
      And user "new@test.pt" admin "false" logged in
      Then element with css "h4.card-title" text is "Request access to machines vulnerabilities data"
      And element with css "div.border-warning p.text-warning" text contains "You don't have access to the dashboard!"
      And element with id "id_email" attribute "value" has value "new@test.pt"
      And element with id "id_email" attribute "readonly" has value "true"

    Scenario: New user welcome page make access request
      Given browser at "/login"
      And user "new@test.pt" admin "false" logged in
      When user types "Loren ipsum" at element with id "id_motive"
      And user types "abc.pt" at element with id "id_form-0-name"
      And user clicks at element with css "form button.btn-primary"
      Then element with css "h4.card-title" text is "Your requests"
      And element with css ".alert-success" text contains "An administrator will validate it. You will be notified by email when the request status change."
      And element with css "#requestsTable tbody tr td:nth-of-type(2)" text contains "abc.pt"
      And element with css "#requestsTable tbody tr td:nth-of-type(3)" text contains "Subscriber"
      And element with css "#requestsTable tbody tr td:nth-of-type(3)" text contains "Pending approval"
