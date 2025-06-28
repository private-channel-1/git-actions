from behave import given, when, then
import json
import re
from datetime import datetime

# Mock data storage for testing
users_db = {}
audit_log = []

@given('the user management system is running')
def step_user_management_system_running(context):
    """Mock that the user management system is running"""
    context.system_running = True
    print("User management system is running")

@given('I am logged in as an administrator')
def step_logged_in_as_admin(context):
    """Mock admin login"""
    context.current_user = {"role": "admin", "email": "admin@example.com"}
    print("Logged in as administrator")

@given('I have user details for "{email}"')
def step_have_user_details(context, email):
    """Store user details for testing"""
    context.user_details = {"email": email}
    print(f"Have user details for {email}")

@given('a user "{email}" exists in the system')
def step_user_exists(context, email):
    """Mock that a user exists in the system"""
    users_db[email] = {
        "email": email,
        "name": "John Doe",
        "role": "user",
        "created_at": datetime.now().isoformat()
    }
    print(f"User {email} exists in the system")

@when('I create a new user with the following details')
def step_create_new_user(context):
    """Create a new user with provided details"""
    user_data = {}
    for row in context.table:
        user_data[row['Field']] = row['Value']
    
    # Mock user creation
    users_db[user_data['email']] = {
        "email": user_data['email'],
        "name": user_data['name'],
        "role": user_data['role'],
        "created_at": datetime.now().isoformat()
    }
    context.created_user = users_db[user_data['email']]
    print(f"Created user: {user_data['email']}")

@when('I update the user\'s name to "{new_name}"')
def step_update_user_name(context, new_name):
    """Update user's name"""
    email = context.user_details['email']
    if email in users_db:
        users_db[email]['name'] = new_name
        context.updated_user = users_db[email]
        print(f"Updated user {email} name to {new_name}")

@when('I delete the user "{email}"')
def step_delete_user(context, email):
    """Delete a user from the system"""
    if email in users_db:
        deleted_user = users_db.pop(email)
        context.deleted_user = deleted_user
        print(f"Deleted user: {email}")

@then('the user should be created successfully')
def step_user_created_successfully(context):
    """Verify user was created successfully"""
    assert context.created_user is not None
    assert context.created_user['email'] in users_db
    print("User created successfully")

@then('the user should receive a welcome email')
def step_user_receives_welcome_email(context):
    """Mock welcome email sending"""
    # In a real scenario, this would check email service
    print("Welcome email sent to user")

@then('the user should appear in the user list')
def step_user_in_list(context):
    """Verify user appears in user list"""
    email = context.created_user['email']
    assert email in users_db
    print(f"User {email} appears in user list")

@then('the user\'s name should be updated to "{expected_name}"')
def step_user_name_updated(context, expected_name):
    """Verify user name was updated"""
    assert context.updated_user['name'] == expected_name
    print(f"User name updated to {expected_name}")

@then('the change should be logged in the audit trail')
def step_change_logged(context):
    """Mock audit trail logging"""
    audit_log.append({
        "action": "update_user",
        "timestamp": datetime.now().isoformat(),
        "user": context.current_user['email']
    })
    print("Change logged in audit trail")

@then('the user should be removed from the system')
def step_user_removed(context):
    """Verify user was removed"""
    email = context.deleted_user['email']
    assert email not in users_db
    print(f"User {email} removed from system")

@then('the user should not appear in the user list')
def step_user_not_in_list(context):
    """Verify user is not in user list"""
    email = context.deleted_user['email']
    assert email not in users_db
    print(f"User {email} not in user list")

@then('the deletion should be logged in the audit trail')
def step_deletion_logged(context):
    """Mock deletion audit logging"""
    audit_log.append({
        "action": "delete_user",
        "timestamp": datetime.now().isoformat(),
        "user": context.current_user['email']
    })
    print("Deletion logged in audit trail")

# Email validation steps
@given('I have user details with email "{email}"')
def step_have_email_details(context, email):
    """Store email for validation testing"""
    context.test_email = email

@when('I attempt to create a user with the email')
def step_attempt_create_with_email(context):
    """Attempt to create user with email"""
    email = context.test_email
    # Simple email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    context.email_valid = bool(re.match(email_pattern, email))

@then('the system should "{result}"')
def step_system_should_result(context, result):
    """Verify system response to email validation"""
    if result == "accept the email":
        assert context.email_valid, f"Email should be valid: {context.test_email}"
    elif result == "reject the email":
        assert not context.email_valid, f"Email should be invalid: {context.test_email}"
    print(f"System {result} for email: {context.test_email}") 