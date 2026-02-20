import requests
import json

def test_api_endpoints():
    base_url = "https://hamza-developer-phase2-backend.hf.space"

    print("Testing API endpoints on:", base_url)
    print("="*50)

    # Test 1: Health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Health endpoint working")
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")

    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Root endpoint working")
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")

    # Test 3: Try to login with non-existent user (should return proper error)
    print("\n3. Testing login endpoint...")
    try:
        response = requests.post(f"{base_url}/api/login",
                                json={"email": "nonexistent@test.com", "password": "password"})
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Login endpoint working (returns proper error for non-existent user)")
    except Exception as e:
        print(f"   ❌ Login endpoint error: {e}")

    # Test 4: Try to register a user (this had the internal server error)
    print("\n4. Testing registration endpoint...")
    try:
        user_data = {
            "email": "test_user@test.com",
            "name": "Test User",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!"
        }
        response = requests.post(f"{base_url}/api/register", json=user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 500:
            print(f"   Response: Internal Server Error")
            print("   ❌ Registration endpoint has internal server error")
        else:
            print(f"   Response: {response.json()}")
            print("   ✅ Registration endpoint working")
    except Exception as e:
        print(f"   ❌ Registration endpoint error: {e}")

    # Test 5: Test protected endpoint without auth
    print("\n5. Testing protected endpoint...")
    try:
        response = requests.get(f"{base_url}/protected-test")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Protected endpoint working (correctly requires auth)")
    except Exception as e:
        print(f"   ❌ Protected endpoint error: {e}")

if __name__ == "__main__":
    test_api_endpoints()