# Python Behave Integration Tests with GitHub Actions

This repository demonstrates how to set up automated integration tests using Python Behave and GitHub Actions. The setup includes sample feature files, step definitions, and a comprehensive CI/CD pipeline.

## 📁 Project Structure

```
git-actions/
├── .github/
│   └── workflows/
│       └── integration-tests.yml    # GitHub Actions workflow
├── features/
│   ├── environment.py               # Behave environment setup
│   ├── user_management.feature      # User management test scenarios
│   ├── api_integration.feature      # API integration test scenarios
│   └── steps/
│       ├── user_management_steps.py # Step definitions for user management
│       └── api_integration_steps.py # Step definitions for API integration
├── requirements.txt                 # Python dependencies
├── behave.ini                      # Behave configuration
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub repository

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd git-actions
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests locally:**
   ```bash
   # Run all tests
   behave
   
   # Run specific feature
   behave features/user_management.feature
   
   # Run with tags
   behave --tags=@smoke
   
   # Run with different output formats
   behave --format=pretty --outfile=test-results.txt
   behave --format=html --outfile=test-results.html
   ```

## 📋 Test Features

### 1. User Management Tests (`user_management.feature`)

Tests user management functionality including:
- ✅ User creation with validation
- ✅ User information updates
- ✅ User deletion
- ✅ Email format validation
- ✅ Audit trail logging

**Sample Scenario:**
```gherkin
Scenario: Create a new user
  Given I have user details for "john.doe@example.com"
  When I create a new user with the following details:
    | Field    | Value           |
    | email    | john.doe@example.com |
    | name     | John Doe        |
    | role     | user            |
  Then the user should be created successfully
  And the user should receive a welcome email
```

### 2. API Integration Tests (`api_integration.feature`)

Tests API endpoints including:
- ✅ GET requests for user lists
- ✅ POST requests for user creation
- ✅ PUT requests for user updates
- ✅ DELETE requests for user removal
- ✅ Error handling (401, 404)
- ✅ JSON response validation

**Sample Scenario:**
```gherkin
Scenario: Get user list
  Given the API server is running on "http://localhost:8000"
  And I have a valid API key
  When I send a GET request to "/api/users"
  Then the response status should be 200
  And the response should contain a list of users
```

## 🔧 Configuration

### Behave Configuration (`behave.ini`)

```ini
[behave]
format=pretty,html
show_skipped=true
show_timings=true
verbose=true
outfiles=test-reports/behave-report.txt
junit=true
junit_directory=test-reports
```

### Environment Setup (`features/environment.py`)

The environment file provides:
- Test suite initialization
- Performance tracking
- Test result aggregation
- Custom tag handling
- Setup/teardown hooks

## 🚀 GitHub Actions Workflow

### Automatic Triggers

The workflow runs automatically on:
- **Push** to `main` or `develop` branches
- **Pull Request** to `main` or `develop` branches
- **Manual trigger** with test suite selection

### Manual Execution

You can manually trigger the workflow with specific test suites:

1. Go to **Actions** tab in your GitHub repository
2. Select **Integration Tests with Behave**
3. Click **Run workflow**
4. Choose test suite:
   - `all` - Run all tests
   - `user_management` - Run only user management tests
   - `api_integration` - Run only API integration tests
   - `smoke` - Run smoke tests (if tagged)

### Matrix Testing

The workflow tests against multiple Python versions:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

### Output and Reports

The workflow generates:
- **Console output** with test results
- **JUnit XML reports** for CI integration
- **HTML reports** for detailed analysis
- **Test artifacts** for download
- **PR comments** with test summaries

## 📊 Test Results

### Local Reports

After running tests locally, you'll find:
- `test-reports/behave-report.txt` - Text summary
- `test-reports/behave-report.html` - HTML report
- `test-reports/` - JUnit XML files

### GitHub Actions Reports

In GitHub Actions:
- **Artifacts** tab contains downloadable test reports
- **Actions** tab shows detailed execution logs
- **Pull Requests** get automatic test result comments

## 🏷️ Using Tags

You can organize tests with tags:

```gherkin
@smoke
Scenario: Quick smoke test
  Given the system is running
  When I perform a basic operation
  Then it should work correctly

@slow @api
Scenario: Complex API test
  Given I have complex test data
  When I perform multiple API calls
  Then all operations should succeed
```

Run tagged tests:
```bash
behave --tags=@smoke          # Run only smoke tests
behave --tags=~@slow          # Skip slow tests
behave --tags=@api --tags=~@slow  # Run API tests but skip slow ones
```

## 🔍 Debugging Tests

### Verbose Output

```bash
behave --verbose
```

### Stop on First Failure

```bash
behave --stop
```

### Dry Run (Show Steps)

```bash
behave --dry-run
```

### Debug Mode

```bash
behave --no-capture
```

## 📝 Adding New Tests

### 1. Create Feature File

```gherkin
# features/new_feature.feature
Feature: New Feature
  As a user
  I want to do something
  So that I can achieve a goal

  Scenario: Basic functionality
    Given some precondition
    When I perform an action
    Then I should see expected result
```

### 2. Create Step Definitions

```python
# features/steps/new_feature_steps.py
from behave import given, when, then

@given('some precondition')
def step_precondition(context):
    # Implementation here
    pass

@when('I perform an action')
def step_action(context):
    # Implementation here
    pass

@then('I should see expected result')
def step_verify_result(context):
    # Implementation here
    pass
```

### 3. Update Workflow (Optional)

Add specific test execution to `.github/workflows/integration-tests.yml`:

```yaml
- name: Run new feature tests
  if: github.event.inputs.test_suite == 'new_feature'
  run: |
    behave features/new_feature.feature --format=pretty --outfile=test-reports/new-feature-tests.txt
```

## 🛠️ Customization

### Environment Variables

Add environment variables to the workflow:

```yaml
env:
  TEST_ENVIRONMENT: staging
  API_BASE_URL: https://api.staging.example.com
  DEBUG_MODE: true
```

### Database Setup

For database tests, add setup steps:

```yaml
- name: Setup test database
  run: |
    # Database setup commands
    python scripts/setup_test_db.py
```

### Parallel Execution

Enable parallel test execution:

```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, 3.10, 3.11]
    test-suite: [user_management, api_integration, smoke]
```

## 📚 Best Practices

1. **Keep scenarios focused** - Each scenario should test one specific behavior
2. **Use descriptive names** - Make feature and scenario names clear and meaningful
3. **Implement proper setup/teardown** - Clean up test data in environment.py
4. **Mock external dependencies** - Don't rely on external services in tests
5. **Use tags for organization** - Tag tests by type, speed, or feature
6. **Generate meaningful reports** - Use multiple output formats for different audiences
7. **Handle test data properly** - Use factories or fixtures for test data
8. **Version control test artifacts** - Keep test reports in version control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your tests
4. Update documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include test logs and error messages

---

**Happy Testing! 🧪✨** 