"""
Direct Better Auth Signup Test
Tests signup via Better Auth API to capture exact error
"""
import requests
import json

BETTER_AUTH_URL = "http://localhost:3000/api/auth/sign-up/email"

test_user = {
    "email": "debugtest@example.com",
    "password": "TestPassword123!",
    "name": "Debug Test User"
}

print("Testing Better Auth Signup...")
print(f"URL: {BETTER_AUTH_URL}")
print(f"Payload: {json.dumps(test_user, indent=2)}")

try:
    response = requests.post(
        BETTER_AUTH_URL,
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    try:
        response_data = response.json()
        print(f"\nResponse Body:")
        print(json.dumps(response_data, indent=2))
    except:
        print(f"\nResponse Text:")
        print(response.text)
        
    if response.status_code == 200:
        print("\n✅ Signup successful!")
    else:
        print(f"\n❌ Signup failed with status {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Request failed: {e}")
    import traceback
    traceback.print_exc()
