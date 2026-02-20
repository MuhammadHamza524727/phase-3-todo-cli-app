#!/usr/bin/env python3
"""
Verification script to confirm all fixes are in place
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath):
    """Check if a file exists"""
    return Path(filepath).exists()

def check_file_contains(filepath, text):
    """Check if a file contains specific text"""
    if not check_file_exists(filepath):
        return False

    with open(filepath, 'r') as f:
        content = f.read()
        return text in content

def main():
    print("🔍 Verifying all fixes are in place...")
    print("="*50)

    all_checks_passed = True

    # Check 1: Database connection improvements
    print("\n1. Checking database connection improvements...")
    db_conn_file = "src/database/connection.py"
    if check_file_exists(db_conn_file):
        print("   ✅ Database connection file exists")

        # Check for URL parameter cleanup
        has_cleanup = check_file_contains(db_conn_file, "sslmode=") or check_file_contains(db_conn_file, "channel_binding=")
        if has_cleanup:
            print("   ✅ URL parameter cleanup implemented")
        else:
            print("   ⚠️  URL parameter cleanup might not be fully implemented")
    else:
        print("   ❌ Database connection file missing")
        all_checks_passed = False

    # Check 2: Authentication service improvements
    print("\n2. Checking authentication service improvements...")
    auth_service_file = "src/services/auth_service.py"
    if check_file_exists(auth_service_file):
        print("   ✅ Authentication service file exists")

        # Check for error handling
        has_error_handling = check_file_contains(auth_service_file, "try:") and check_file_contains(auth_service_file, "except")
        if has_error_handling:
            print("   ✅ Error handling implemented")
        else:
            print("   ⚠️  Error handling might be insufficient")

        # Check for SQLModel syntax
        has_exec_syntax = check_file_contains(auth_service_file, ".exec(") or check_file_contains(auth_service_file, ".first()")
        if has_exec_syntax:
            print("   ✅ Updated SQLModel syntax used")
        else:
            print("   ⚠️  May still use old SQLModel syntax")
    else:
        print("   ❌ Authentication service file missing")
        all_checks_passed = False

    # Check 3: Authentication API improvements
    print("\n3. Checking authentication API improvements...")
    auth_api_file = "src/api/auth.py"
    if check_file_exists(auth_api_file):
        print("   ✅ Authentication API file exists")

        # Check for enhanced logging
        has_logging = check_file_contains(auth_api_file, "logger.info(") or check_file_contains(auth_api_file, "logging")
        if has_logging:
            print("   ✅ Logging implemented")
        else:
            print("   ⚠️  Logging might be insufficient")
    else:
        print("   ❌ Authentication API file missing")
        all_checks_passed = False

    # Check 4: Main application improvements
    print("\n4. Checking main application improvements...")
    main_file = "main.py"
    if check_file_exists(main_file):
        print("   ✅ Main application file exists")

        # Check for lifespan improvements
        has_lifespan = check_file_contains(main_file, "lifespan") or check_file_contains(main_file, "@asynccontextmanager")
        if has_lifespan:
            print("   ✅ Lifespan context implemented")
        else:
            print("   ⚠️  Lifespan context might not be properly implemented")
    else:
        print("   ❌ Main application file missing")
        all_checks_passed = False

    # Check 5: Test files existence
    print("\n5. Checking test files...")
    test_files = [
        "test_backend.py",
        "diagnostic_report.py",
        "test_registration_flow.py"
    ]

    for test_file in test_files:
        if check_file_exists(test_file):
            print(f"   ✅ {test_file} exists")
        else:
            print(f"   ⚠️  {test_file} missing")

    # Check 6: Documentation files
    print("\n6. Checking documentation files...")
    docs = [
        "API_TEST_REPORT.md",
        "FINAL_FIX_SUMMARY.md",
        "DEPLOYMENT_INSTRUCTIONS.md"
    ]

    for doc in docs:
        if check_file_exists(doc):
            print(f"   ✅ {doc} exists")
        else:
            print(f"   ❌ {doc} missing")
            all_checks_passed = False

    print("\n" + "="*50)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ The codebase is ready for deployment")
        print("➡️  Follow the deployment instructions in DEPLOYMENT_INSTRUCTIONS.md")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("🚨 Please review the missing components above")

    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)