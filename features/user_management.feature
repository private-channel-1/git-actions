Feature: User Management
  As a system administrator
  I want to manage users
  So that I can control access to the system

  Background:
    Given the user management system is running
    And I am logged in as an administrator

  Scenario: Create a new user
    Given I have user details for "john.doe@example.com"
    When I create a new user with the following details:
      | Field    | Value           |
      | email    | john.doe@example.com |
      | name     | John Doe        |
      | role     | user            |
    Then the user should be created successfully
    And the user should receive a welcome email
    And the user should appear in the user list

  Scenario: Update user information
    Given a user "john.doe@example.com" exists in the system
    When I update the user's name to "John Smith"
    Then the user's name should be updated to "John Smith"
    And the change should be logged in the audit trail

  Scenario: Delete a user
    Given a user "john.doe@example.com" exists in the system
    When I delete the user "john.doe@example.com"
    Then the user should be removed from the system
    And the user should not appear in the user list
    And the deletion should be logged in the audit trail

  Scenario Outline: Validate user email format
    Given I have user details with email "<email>"
    When I attempt to create a user with the email
    Then the system should "<result>"

    Examples:
      | email                    | result           |
      | valid@example.com        | accept the email |
      | invalid-email            | reject the email |
      | @example.com             | reject the email |
      | test@                   | reject the email | 