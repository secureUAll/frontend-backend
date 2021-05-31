
  Feature: Welcome page interaction

    Scenario: New user form visible
      Given browser at "/login"
      And user "new@test.pt" admin "false" logged in
      Then url without data is "/welcome/"
      And element with css "h4.card-title" text is "Request access to machines vulnerabilities data"
      And element with css "div.border-warning p.text-warning" text contains "You don't have access to the dashboard!"
      And element with id "id_email" attribute "value" has value "new@test.pt"
      And element with id "id_email" attribute "readonly" has value "true"

    Scenario: New user access request valid and feedback
      Given browser at "/login"
      And user "new@test.pt" admin "false" logged in
      When user types "Loren ipsum" at element with id "id_motive"
      And user types "abc.pt" at element with id "id_form-0-name"
      And user clicks at element with css "form button.btn-primary"
      Then url without data is "/welcome/"
      And element with css "h4.card-title" text is "Your requests"
      And element with css ".alert-success" text contains "An administrator will validate it. You will be notified by email when the request status change."
      And element with css "#requestsTable tbody tr td:nth-of-type(2)" text contains "abc.pt"
      And element with css "#requestsTable tbody tr td:nth-of-type(3)" text contains "Subscriber"
      And element with css "#requestsTable tbody tr td:nth-of-type(4)" text contains "Pending approval"

    Scenario: New user access request invalid and feedback
      Given browser at "/login"
      And user "new@test.pt" admin "false" logged in
      When user types "Loren ipsum" at element with id "id_motive"
      And user types "125.2." at element with id "id_form-0-name"
      And user types "abc{¬4238/823)(.ua.pt" at element with id "id_form-1-name"
      And user clicks at element with css "form button.btn-primary"
      Then url without data is "/welcome/"
      And element with css "h4.card-title" text is "Request access to machines vulnerabilities data"
      And element with css ".alert-danger" text contains "Please make sure you have filled the motive and at least one machines data with valid names/IPs."
      And element with xpath "//*[@id='id_form-0-name']//parent::div//i" attribute "title" has value "This is not a valid DNS nor IP address."
      And element with xpath "//*[@id='id_form-1-name']//parent::div//i" attribute "title" has value "This is not a valid DNS nor IP address."

    Scenario: User with denied request has feedback and form to send a new one
      Given browser at "/login"
      And user "user@test.pt" admin "false" logged in
      And user has access request "denied"
      And refresh
      Then url without data is "/welcome/"
      And element with css "h4.card-title:nth-of-type(1)" text is "Your requests"
      And element with xpath "//div[contains(@class, 'col-md-4')]/div[2]//h4" text is "Your requests"
      And element with css "#requestsTable tbody tr td:nth-of-type(4)" text contains "Denied"
      And element with xpath "//div[contains(@class, 'col-md-4')]/div[3]//h4" text is "Request access to machines vulnerabilities data"
      And element with css "form div.form-group" is visible
      And element with css "form table.table-discreet" is visible

    Scenario: User with machines is redirected to dashboard
      Given browser at "/login"
      And user "user@test.pt" admin "false" logged in
      And user has machine
      And refresh
      Then url without data is "/"

    Scenario: Admin is redirected to dashboard
      Given browser at "/login"
      And user "admin@test.pt" admin "true" logged in
      And refresh
      Then url without data is "/"
