#!/usr/bin/env python3
"""
Test script to verify password hashing behavior
"""
from passlib.context import CryptContext

# Test the current password hashing implementation
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    """Current implementation"""
    return pwd_context.hash(password[:72])

def test_password_hashing():
    """Test various password lengths"""
    test_passwords = [
        "short",  # Short password
        "Hamza12345",  # Your example password (10 chars)
        "A" * 50,  # 50 chars
        "A" * 72,  # Exactly 72 chars
        "A" * 73,  # 73 chars (over the limit)
        "A" * 100,  # 100 chars (way over the limit)
    ]

    print("Testing password hashing implementation...")

    for i, password in enumerate(test_passwords):
        try:
            print(f"\nTest {i+1}: Password length = {len(password)}")
            print(f"Original password: {password[:20]}{'...' if len(password) > 20 else ''}")

            # Test the truncation
            truncated = password[:72]
            print(f"Truncated to: {len(truncated)} chars")

            # Test the hashing
            hashed = get_password_hash(password)
            print(f"✅ Hashing successful: {hashed[:30]}...")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_manual_truncation():
    """Test manual truncation approach"""
    print("\n" + "="*50)
    print("Testing manual truncation approach...")

    long_password = "A" * 80  # Definitely over 72 chars

    print(f"Original password length: {len(long_password)}")

    # Try direct bcrypt hash without manual truncation (this might fail)
    try:
        direct_hash = pwd_context.hash(long_password)
        print(f"Direct hash succeeded: {direct_hash[:30]}...")
    except Exception as e:
        print(f"Direct hash failed (expected): {str(e)}")

    # Try with manual truncation
    try:
        manual_truncated = long_password[:72]
        manual_hash = pwd_context.hash(manual_truncated)
        print(f"Manual truncation succeeded: {manual_hash[:30]}...")
    except Exception as e:
        print(f"Manual truncation failed: {str(e)}")

if __name__ == "__main__":
    test_password_hashing()
    test_manual_truncation()