"""
Behave environment configuration for integration tests.
This file handles setup and teardown for test scenarios.
"""

import os
import sys
from datetime import datetime

def before_all(context):
    """Setup before all tests run"""
    print("=" * 60)
    print("Starting Integration Test Suite")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Add project root to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Initialize test context
    context.test_start_time = datetime.now()
    context.test_results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # Set up test configuration
    context.config = {
        "api_base_url": "http://localhost:8000",
        "test_timeout": 30,
        "retry_attempts": 3
    }
    
    print("Test environment initialized")

def before_feature(context, feature):
    """Setup before each feature"""
    print(f"\n--- Starting Feature: {feature.name} ---")
    context.feature_start_time = datetime.now()
    
    # Reset feature-specific context
    context.feature_data = {}
    context.api_responses = []

def before_scenario(context, scenario):
    """Setup before each scenario"""
    print(f"\n  Scenario: {scenario.name}")
    context.scenario_start_time = datetime.now()
    
    # Reset scenario-specific context
    context.scenario_data = {}
    context.current_user = None
    context.api_response = None

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    scenario_duration = datetime.now() - context.scenario_start_time
    
    if scenario.status == "passed":
        context.test_results["passed"] += 1
        print(f"    ✓ PASSED ({scenario_duration.total_seconds():.2f}s)")
    elif scenario.status == "failed":
        context.test_results["failed"] += 1
        print(f"    ✗ FAILED ({scenario_duration.total_seconds():.2f}s)")
    else:
        context.test_results["skipped"] += 1
        print(f"    - SKIPPED ({scenario_duration.total_seconds():.2f}s)")

def after_feature(context, feature):
    """Cleanup after each feature"""
    feature_duration = datetime.now() - context.feature_start_time
    print(f"\n--- Completed Feature: {feature.name} ({feature_duration.total_seconds():.2f}s) ---")

def after_all(context):
    """Cleanup after all tests complete"""
    total_duration = datetime.now() - context.test_start_time
    
    print("\n" + "=" * 60)
    print("Integration Test Suite Results")
    print("=" * 60)
    print(f"Total Duration: {total_duration.total_seconds():.2f} seconds")
    print(f"Passed: {context.test_results['passed']}")
    print(f"Failed: {context.test_results['failed']}")
    print(f"Skipped: {context.test_results['skipped']}")
    print(f"Total: {sum(context.test_results.values())}")
    
    if context.test_results['failed'] > 0:
        print("\n❌ Some tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
    
    print("=" * 60)

# Optional: Handle specific tags
def before_tag(context, tag):
    """Handle specific tags if needed"""
    if tag == "slow":
        print("  [SLOW TEST] This test may take longer to complete")
    elif tag == "api":
        print("  [API TEST] Testing external API integration")
    elif tag == "database":
        print("  [DATABASE TEST] Testing database operations")

def after_tag(context, tag):
    """Cleanup after specific tags if needed"""
    if tag == "database":
        # Clean up test database if needed
        pass 