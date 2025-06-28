Feature: API Integration
  As a developer
  I want to test API endpoints
  So that I can ensure the API works correctly

  Background:
    Given the API server is running on "http://localhost:8000"
    And I have a valid API key

  Scenario: Get user list
    Given I want to retrieve all users
    When I send a GET request to "/api/users"
    Then the response status should be 200
    And the response should contain a list of users
    And the response should be in JSON format

  Scenario: Create user via API
    Given I have user data for "api.user@example.com"
    When I send a POST request to "/api/users" with the following data:
      | Field    | Value                |
      | email    | api.user@example.com |
      | name     | API User             |
      | role     | user                 |
    Then the response status should be 201
    And the response should contain the created user data
    And the user should have an ID

  Scenario: Update user via API
    Given a user with ID "123" exists
    When I send a PUT request to "/api/users/123" with updated name "Updated User"
    Then the response status should be 200
    And the user's name should be updated to "Updated User"

  Scenario: Delete user via API
    Given a user with ID "123" exists
    When I send a DELETE request to "/api/users/123"
    Then the response status should be 204
    And the user should be deleted from the system

  Scenario: Handle invalid API key
    Given I have an invalid API key
    When I send a GET request to "/api/users"
    Then the response status should be 401
    And the response should contain an error message

  Scenario: Handle non-existent resource
    Given I want to access a non-existent user
    When I send a GET request to "/api/users/999999"
    Then the response status should be 404
    And the response should contain an error message 