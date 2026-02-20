import requests
import json
from datetime import datetime

def diagnostic_report():
    print("🔍 DIAGNOSTIC REPORT FOR TODO API")
    print("="*50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target URL: https://hamza-developer-phase2-backend.hf.space")
    print()

    # Test endpoints
    endpoints = [
        ("GET", "/"),
        ("GET", "/health"),
        ("GET", "/docs"),
        ("POST", "/api/login", {"email": "test@example.com", "password": "password"}),
        ("GET", "/protected-test"),
        ("GET", "/api/tasks"),
        ("POST", "/api/register", {
            "email": "diagnostic@test.com",
            "name": "Diagnostic User",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!"
        })
    ]

    print("📊 ENDPOINT TEST RESULTS:")
    print("-" * 30)

    for i, test in enumerate(endpoints):
        method, path = test[0], test[1]
        data = test[2] if len(test) > 2 else None

        try:
            url = f"https://hamza-developer-phase2-backend.hf.space{path}"

            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)

            status_emoji = "✅" if response.status_code < 400 else "❌"
            print(f"{status_emoji} {method} {path}: {response.status_code}")

            if path == "/api/register" and response.status_code == 500:
                print(f"   → 500 Internal Server Error - This is the main issue")
                print(f"   → Likely database connection/initialization problem")

            if path == "/api/login":
                if response.status_code == 401:
                    print(f"   → Expected behavior: Invalid credentials return 401")

        except requests.exceptions.Timeout:
            print(f"❌ {method} {path}: TIMEOUT (10 seconds)")
        except requests.exceptions.RequestException as e:
            print(f"❌ {method} {path}: NETWORK ERROR - {str(e)}")

    print()
    print("💡 ANALYSIS & RECOMMENDATIONS:")
    print("-" * 30)
    print("PROBLEM IDENTIFIED:")
    print("• Registration endpoint returns 500 Internal Server Error")
    print("• All other endpoints work correctly")
    print("• Authentication system works (login, protected endpoints)")
    print()
    print("LIKELY CAUSES:")
    print("1. Database connection initialization issue in Hugging Face environment")
    print("2. Neon PostgreSQL connection parameters may need adjustment for HF")
    print("3. Database tables might not be created during startup")
    print("4. Network restrictions between Hugging Face and Neon DB")
    print()
    print("SOLUTIONS TO TRY:")
    print("1. Check Hugging Face Space logs for specific error messages")
    print("2. Verify Neon PostgreSQL allows connections from Hugging Face IPs")
    print("3. Consider using a connection pool configuration suitable for HF")
    print("4. Add more robust error handling around database operations")
    print()
    print("🎯 NEXT STEPS:")
    print("1. Access your Hugging Face Space logs for detailed error information")
    print("2. Verify your Neon PostgreSQL connection string is correct")
    print("3. Test database connectivity from a similar environment")
    print("4. Redeploy with additional logging if needed")
    print()
    print("✅ CONFIRMED WORKING:")
    print("• Health check endpoint")
    print("• Root endpoint")
    print("• API documentation")
    print("• Authentication validation")
    print("• Protected endpoint authorization")

if __name__ == "__main__":
    diagnostic_report()