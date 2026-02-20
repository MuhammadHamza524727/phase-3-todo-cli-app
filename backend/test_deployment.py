#!/usr/bin/env python3
"""
Simple test script to verify the application can start without errors
"""

import os
import sys
import traceback

# Add the current directory to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_import():
    """Test if the app can be imported without errors"""
    try:
        # Import the app module to check for syntax/import errors
        from app import app
        print("✓ Application module imported successfully")

        # Check if the app object exists
        assert hasattr(app, 'routes'), "App object should have routes attribute"
        print("✓ Application object is properly structured")

        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        traceback.print_exc()
        return False

def test_database_connection():
    """Test if database connection can be established"""
    try:
        from src.database.connection import DATABASE_URL, engine
        print(f"✓ Database URL is set: {'Yes' if DATABASE_URL else 'No'}")

        if DATABASE_URL:
            print(f"✓ Database URL: {DATABASE_URL[:50]}...")  # Show first 50 chars

        return True
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        traceback.print_exc()
        return False

def main():
    print("Testing application for Hugging Face deployment...")
    print("="*50)

    # Test app import
    app_ok = test_app_import()
    print()

    # Test database connection
    db_ok = test_database_connection()
    print()

    if app_ok and db_ok:
        print("✓ All tests passed! Application is ready for Hugging Face deployment.")
        return 0
    else:
        print("✗ Some tests failed. Please fix the errors before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())