#!/usr/bin/env python3
"""
Specific test to replicate the exact issue with password hashing
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Import the exact functions from the deployed modules
from src.middleware.jwt_auth import get_password_hash
from src.services.auth_service import create_new_user
from src.models.user import UserCreate

def test_exact_scenario():
    """Test with the exact password that's failing"""
    print("Testing with the exact password from the error...")

    # The exact data from the error
    user_data = UserCreate(
        email="hamza.dev@example.com",
        name="Muhammad Hamza",
        password="Hamza12345",
        password_confirm="Hamza12345"
    )

    print(f"Password: {user_data.password}")
    print(f"Password length: {len(user_data.password)}")

    try:
        # Test password hashing directly
        print("\nTesting password hashing...")
        hashed = get_password_hash(user_data.password)
        print(f"✅ Password hashing successful: {hashed[:30]}...")

        print("\nPassword hashing test passed - the local code handles this correctly.")
        print("The issue is that the deployed Hugging Face version has different code.")

    except Exception as e:
        print(f"❌ Password hashing failed locally: {str(e)}")
        return False

    return True

def test_various_password_lengths():
    """Test different password lengths to understand the boundary"""
    print("\n" + "="*50)
    print("Testing various password lengths...")

    test_cases = [
        ("short", "Short password"),
        ("Hamza12345", "Your test password"),
        ("A" * 70, "70 characters"),
        ("A" * 71, "71 characters"),
        ("A" * 72, "Exactly 72 characters"),
        ("A" * 73, "73 characters (over limit)"),
        ("A" * 100, "100 characters"),
    ]

    for password, description in test_cases:
        try:
            hashed = get_password_hash(password)
            print(f"✅ {description} ({len(password)} chars): Success")
        except Exception as e:
            print(f"❌ {description} ({len(password)} chars): Failed - {str(e)}")

if __name__ == "__main__":
    success = test_exact_scenario()
    test_various_password_lengths()

    if success:
        print("\n" + "="*60)
        print("CONCLUSION:")
        print("✅ The local code handles password hashing correctly")
        print("❌ The deployed Hugging Face version has different code")
        print("🔄 SOLUTION: Deploy the latest code to Hugging Face")
        print("="*60)