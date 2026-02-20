#!/usr/bin/env python3
"""
Test script for the register API endpoint
"""
import requests
import json
import sys

# Configuration
BASE_URL = "https://hamza-developer-phase2-backend.hf.space"
# BASE_URL = "http://localhost:8000"  # Uncomment for local testing

def test_register():
    """Test the register endpoint"""
    url = f"{BASE_URL}/api/register"
    
    # Test data
    test_user = {
        "email": f"test_{int(requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC').json()['unixtime'])}@example.com",
        "name": "Test User",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!"
    }
    
    print(f"Testing register endpoint: {url}")
    print(f"Request data: {json.dumps({**test_user, 'password': '***', 'password_confirm': '***'}, indent=2)}")
    
    try:
        response = requests.post(url, json=test_user, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Body (raw): {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Registration successful!")
            return True
        else:
            print(f"\n❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {str(e)}")
        return False

def test_health():
    """Test the health endpoint"""
    url = f"{BASE_URL}/health"
    print(f"\nTesting health endpoint: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("API Registration Test")
    print("=" * 60)
    
    # First check if the API is up
    if not test_health():
        print("\n⚠️  API health check failed. The service might be down.")
        sys.exit(1)
    
    # Test registration
    success = test_register()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Tests failed!")
        sys.exit(1)
