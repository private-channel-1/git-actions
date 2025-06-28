#!/usr/bin/env python3
"""
Local GitHub Actions testing script using Act.
This script helps you test your GitHub Actions workflow locally before pushing to GitHub.
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

def check_act_installation():
    """Check if Act is installed"""
    try:
        result = subprocess.run(["act", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Act is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Act is not properly installed")
            return False
    except FileNotFoundError:
        print("❌ Act is not installed. Please install it first:")
        print("   Windows: winget install nektos.act")
        print("   macOS: brew install act")
        print("   Linux: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash")
        return False

def test_workflow_dry_run():
    """Test workflow with dry run (no actual execution)"""
    return run_command(
        ["act", "--dry-run"],
        "Testing workflow with dry run (no actual execution)"
    )

def test_workflow_full():
    """Test workflow with full execution"""
    return run_command(
        ["act", "--verbose"],
        "Testing workflow with full execution"
    )

def test_workflow_push():
    """Test workflow simulating a push event"""
    return run_command(
        ["act", "push", "--verbose"],
        "Testing workflow simulating a push event"
    )

def test_workflow_pr():
    """Test workflow simulating a pull request event"""
    return run_command(
        ["act", "pull_request", "--verbose"],
        "Testing workflow simulating a pull request event"
    )

def test_workflow_manual():
    """Test workflow with manual dispatch"""
    return run_command(
        ["act", "workflow_dispatch", "--verbose"],
        "Testing workflow with manual dispatch"
    )

def test_workflow_with_input():
    """Test workflow with specific input"""
    test_suite = input("Enter test suite to run (all/user_management/api_integration/smoke): ").strip()
    if not test_suite:
        test_suite = "all"
    
    return run_command(
        ["act", "workflow_dispatch", "-e", f"-", "--input", f"test_suite={test_suite}", "--verbose"],
        f"Testing workflow with manual dispatch and test_suite={test_suite}"
    )

def list_available_events():
    """List available workflow events"""
    print("\n📋 Available workflow events:")
    print("  - push: Simulates a push to main/develop")
    print("  - pull_request: Simulates a pull request")
    print("  - workflow_dispatch: Simulates manual trigger")
    print("  - schedule: Simulates scheduled runs")
    print("\n💡 Use 'act --list' to see all available events")

def show_help():
    """Show help information"""
    help_text = """
GitHub Actions Local Testing with Act

Usage:
    python test_workflow_local.py [command] [options]

Commands:
    check           Check if Act is installed
    dry-run         Test workflow with dry run (no execution)
    full            Test workflow with full execution
    push            Test workflow simulating a push event
    pr              Test workflow simulating a pull request
    manual          Test workflow with manual dispatch
    input           Test workflow with custom input
    list            List available workflow events
    help            Show this help message

Examples:
    python test_workflow_local.py check
    python test_workflow_local.py dry-run
    python test_workflow_local.py push
    python test_workflow_local.py input

Prerequisites:
    - Docker Desktop installed and running
    - Act installed (winget install nektos.act)

Notes:
    - Act requires Docker to run GitHub Actions locally
    - Some actions may not work exactly the same locally
    - Use dry-run first to check for issues
    """
    print(help_text)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Local GitHub Actions Testing with Act")
    parser.add_argument("command", nargs="?", default="help", 
                       choices=["check", "dry-run", "full", "push", "pr", "manual", "input", "list", "help"],
                       help="Command to run")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "help":
        show_help()
        return
    
    success = False
    
    if args.command == "check":
        success = check_act_installation()
    elif args.command == "dry-run":
        success = test_workflow_dry_run()
    elif args.command == "full":
        success = test_workflow_full()
    elif args.command == "push":
        success = test_workflow_push()
    elif args.command == "pr":
        success = test_workflow_pr()
    elif args.command == "manual":
        success = test_workflow_manual()
    elif args.command == "input":
        success = test_workflow_with_input()
    elif args.command == "list":
        list_available_events()
        return
    
    # Exit with appropriate code
    if success:
        print("\n🎉 Workflow testing completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Workflow testing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 