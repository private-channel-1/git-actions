#!/usr/bin/env python3
"""
Test runner script for Behave integration tests.
Provides easy commands to run different test suites locally.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Installing dependencies"
    )

def run_all_tests():
    """Run all integration tests"""
    return run_command(
        ["behave", "--format=pretty", "--outfile=test-reports/all-tests.txt"],
        "Running all integration tests"
    )

def run_user_management_tests():
    """Run user management tests only"""
    return run_command(
        ["behave", "features/user_management.feature", "--format=pretty", "--outfile=test-reports/user-management-tests.txt"],
        "Running user management tests"
    )

def run_api_integration_tests():
    """Run API integration tests only"""
    return run_command(
        ["behave", "features/api_integration.feature", "--format=pretty", "--outfile=test-reports/api-integration-tests.txt"],
        "Running API integration tests"
    )

def run_smoke_tests():
    """Run smoke tests (if tagged)"""
    return run_command(
        ["behave", "--tags=@smoke", "--format=pretty", "--outfile=test-reports/smoke-tests.txt"],
        "Running smoke tests"
    )

def run_with_html_report():
    """Run tests with HTML report"""
    return run_command(
        ["behave", "--format=pretty,html", "--outfile=test-reports/behave-report.txt,test-reports/behave-report.html"],
        "Running tests with HTML report"
    )

def run_with_junit_report():
    """Run tests with JUnit XML report"""
    return run_command(
        ["behave", "--format=pretty,junit", "--outfile=test-reports/behave-report.txt", "--junit-directory=test-reports"],
        "Running tests with JUnit XML report"
    )

def run_verbose():
    """Run tests with verbose output"""
    return run_command(
        ["behave", "--verbose", "--format=pretty"],
        "Running tests with verbose output"
    )

def run_dry_run():
    """Run dry run to see all steps"""
    return run_command(
        ["behave", "--dry-run"],
        "Running dry run (showing all steps)"
    )

def create_test_reports_dir():
    """Create test reports directory"""
    reports_dir = Path("test-reports")
    reports_dir.mkdir(exist_ok=True)
    print(f"✅ Test reports directory created: {reports_dir.absolute()}")

def show_help():
    """Show help information"""
    help_text = """
Python Behave Integration Test Runner

Usage:
    python run_tests.py [command] [options]

Commands:
    install          Install Python dependencies
    all              Run all integration tests
    user-mgmt        Run user management tests only
    api              Run API integration tests only
    smoke            Run smoke tests (if tagged)
    html             Run tests with HTML report
    junit            Run tests with JUnit XML report
    verbose          Run tests with verbose output
    dry-run          Show all test steps without running
    help             Show this help message

Examples:
    python run_tests.py install
    python run_tests.py all
    python run_tests.py user-mgmt
    python run_tests.py api --verbose
    python run_tests.py html

Options:
    --verbose        Enable verbose output for any command
    --help           Show help message
    """
    print(help_text)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Python Behave Integration Test Runner")
    parser.add_argument("command", nargs="?", default="help", 
                       choices=["install", "all", "user-mgmt", "api", "smoke", "html", "junit", "verbose", "dry-run", "help"],
                       help="Command to run")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Create test reports directory
    create_test_reports_dir()
    
    # Handle commands
    if args.command == "help":
        show_help()
        return
    
    success = False
    
    if args.command == "install":
        success = install_dependencies()
    elif args.command == "all":
        success = run_all_tests()
    elif args.command == "user-mgmt":
        success = run_user_management_tests()
    elif args.command == "api":
        success = run_api_integration_tests()
    elif args.command == "smoke":
        success = run_smoke_tests()
    elif args.command == "html":
        success = run_with_html_report()
    elif args.command == "junit":
        success = run_with_junit_report()
    elif args.command == "verbose":
        success = run_verbose()
    elif args.command == "dry-run":
        success = run_dry_run()
    
    # Exit with appropriate code
    if success:
        print("\n🎉 All operations completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some operations failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 