from behave import given, when, then
import requests
import json
from unittest.mock import Mock, patch

# Mock API responses for testing
mock_api_responses = {
    "users": [
        {"id": 1, "email": "user1@example.com", "name": "User One", "role": "user"},
        {"id": 2, "email": "user2@example.com", "name": "User Two", "role": "admin"}
    ],
    "user_123": {"id": 123, "email": "test@example.com", "name": "Test User", "role": "user"},
    "created_user": {"id": 456, "email": "api.user@example.com", "name": "API User", "role": "user"}
}

@given('the API server is running on "{base_url}"')
def step_api_server_running(context, base_url):
    """Mock that the API server is running"""
    context.base_url = base_url
    context.api_server_running = True
    print(f"API server running on {base_url}")

@given('I have a valid API key')
def step_have_valid_api_key(context):
    """Mock valid API key"""
    context.api_key = "valid-api-key-12345"
    context.headers = {"Authorization": f"Bearer {context.api_key}", "Content-Type": "application/json"}
    print("Have valid API key")

@given('I have an invalid API key')
def step_have_invalid_api_key(context):
    """Mock invalid API key"""
    context.api_key = "invalid-api-key"
    context.headers = {"Authorization": f"Bearer {context.api_key}", "Content-Type": "application/json"}
    print("Have invalid API key")

@given('I want to retrieve all users')
def step_want_retrieve_users(context):
    """Prepare to retrieve users"""
    context.request_type = "GET"
    context.endpoint = "/api/users"
    print("Want to retrieve all users")

@given('I have user data for "{email}"')
def step_have_user_data(context, email):
    """Store user data for API testing"""
    context.user_data = {"email": email}
    print(f"Have user data for {email}")

@given('a user with ID "{user_id}" exists')
def step_user_with_id_exists(context, user_id):
    """Mock that a user with specific ID exists"""
    context.user_id = user_id
    context.user_exists = True
    print(f"User with ID {user_id} exists")

@given('I want to access a non-existent user')
def step_want_access_nonexistent_user(context):
    """Prepare to access non-existent user"""
    context.user_id = "999999"
    context.user_exists = False
    print("Want to access non-existent user")

@when('I send a GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    """Send GET request to API endpoint"""
    context.endpoint = endpoint
    context.request_type = "GET"
    
    # Mock the response based on endpoint
    if endpoint == "/api/users":
        context.response = Mock()
        context.response.status_code = 200
        context.response.json.return_value = mock_api_responses["users"]
        context.response.headers = {"Content-Type": "application/json"}
    elif endpoint == "/api/users/999999":
        context.response = Mock()
        context.response.status_code = 404
        context.response.json.return_value = {"error": "User not found"}
    
    print(f"Sent GET request to {endpoint}")

@when('I send a POST request to "{endpoint}" with the following data')
def step_send_post_request(context, endpoint):
    """Send POST request with data table"""
    context.endpoint = endpoint
    context.request_type = "POST"
    
    # Extract data from table
    request_data = {}
    for row in context.table:
        request_data[row['Field']] = row['Value']
    
    context.request_data = request_data
    
    # Mock successful creation
    context.response = Mock()
    context.response.status_code = 201
    context.response.json.return_value = mock_api_responses["created_user"]
    
    print(f"Sent POST request to {endpoint} with data: {request_data}")

@when('I send a PUT request to "{endpoint}" with updated name "{new_name}"')
def step_send_put_request(context, endpoint, new_name):
    """Send PUT request to update user"""
    context.endpoint = endpoint
    context.request_type = "PUT"
    context.new_name = new_name
    
    # Mock successful update
    context.response = Mock()
    context.response.status_code = 200
    updated_user = mock_api_responses["user_123"].copy()
    updated_user["name"] = new_name
    context.response.json.return_value = updated_user
    
    print(f"Sent PUT request to {endpoint} with new name: {new_name}")

@when('I send a DELETE request to "{endpoint}"')
def step_send_delete_request(context, endpoint):
    """Send DELETE request"""
    context.endpoint = endpoint
    context.request_type = "DELETE"
    
    # Mock successful deletion
    context.response = Mock()
    context.response.status_code = 204
    context.response.content = b""
    
    print(f"Sent DELETE request to {endpoint}")

@then('the response status should be {status_code:d}')
def step_response_status(context, status_code):
    """Verify response status code"""
    assert context.response.status_code == status_code, \
        f"Expected status {status_code}, got {context.response.status_code}"
    print(f"Response status is {status_code}")

@then('the response should contain a list of users')
def step_response_contains_users(context):
    """Verify response contains user list"""
    response_data = context.response.json()
    assert isinstance(response_data, list), "Response should be a list"
    assert len(response_data) > 0, "Response should contain users"
    print("Response contains list of users")

@then('the response should be in JSON format')
def step_response_is_json(context):
    """Verify response is JSON format"""
    content_type = context.response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected JSON content type, got {content_type}"
    print("Response is in JSON format")

@then('the response should contain the created user data')
def step_response_contains_created_user(context):
    """Verify response contains created user data"""
    response_data = context.response.json()
    assert "id" in response_data, "Response should contain user ID"
    assert "email" in response_data, "Response should contain user email"
    assert "name" in response_data, "Response should contain user name"
    print("Response contains created user data")

@then('the user should have an ID')
def step_user_has_id(context):
    """Verify user has an ID"""
    response_data = context.response.json()
    assert "id" in response_data, "User should have an ID"
    assert response_data["id"] is not None, "User ID should not be None"
    print(f"User has ID: {response_data['id']}")

@then('the user\'s name should be updated to "{expected_name}"')
def step_user_name_updated_via_api(context, expected_name):
    """Verify user name was updated via API"""
    response_data = context.response.json()
    assert response_data["name"] == expected_name, \
        f"Expected name {expected_name}, got {response_data['name']}"
    print(f"User name updated to {expected_name}")

@then('the user should be deleted from the system')
def step_user_deleted_via_api(context):
    """Verify user was deleted via API"""
    assert context.response.status_code == 204, "Delete should return 204 status"
    print("User deleted from system via API")

@then('the response should contain an error message')
def step_response_contains_error(context):
    """Verify response contains error message"""
    response_data = context.response.json()
    assert "error" in response_data, "Response should contain error message"
    print(f"Response contains error: {response_data['error']}")

# Helper function to simulate API calls
def mock_api_call(method, url, headers=None, json=None):
    """Mock API call function"""
    mock_response = Mock()
    
    if "invalid-api-key" in str(headers):
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API key"}
    elif method == "GET" and "/api/users" in url:
        if "999999" in url:
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "User not found"}
        else:
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_responses["users"]
            mock_response.headers = {"Content-Type": "application/json"}
    
    return mock_response 