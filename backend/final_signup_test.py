"""
Final Signup Test with Fresh Email
Tests signup with a new email to confirm everything works
"""
import requests
import json
import time

BETTER_AUTH_URL = "http://localhost:3000/api/auth/sign-up/email"

# Use timestamp to ensure unique email
test_user = {
    "email": f"finaltest{int(time.time())}@example.com",
    "password": "TestPassword123!",
    "name": "Final Test User"
}

print("Final Signup Test...")
print(f"Email: {test_user['email']}")

try:
    response = requests.post(
        BETTER_AUTH_URL,
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅✅✅ SIGNUP SUCCESSFUL! ✅✅✅")
        try:
            data = response.json()
            print(f"\nUser created:")
            print(f"  ID: {data.get('user', {}).get('id')}")
            print(f"  Email: {data.get('user', {}).get('email')}")
            print(f"  Name: {data.get('user', {}).get('name')}")
        except:
            pass
    else:
        print(f"❌ Signup failed: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Response: {response.text}")
            
except Exception as e:
    print(f"❌ Error: {e}")
