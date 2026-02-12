import os
import sys
import requests
import time
from datetime import timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.utils.security import create_access_token

# Configuration
API_URL = "http://localhost:8000/api"
SECRET = os.getenv("BETTER_AUTH_SECRET", "testsupersecretKey12345678901234567890")

print(f"Testing against Backend API: {API_URL}")

def test_full_flow():
    # 1. Simulate "Frontend" Login / Token Generation
    # Since we can't easily hit the Next.js auth endpoints from here without browser cookies/headers,
    # we will VALIDATE the backend by minting a token exactly like Better Auth would.
    print("\n[1] Simulating Frontend Login (Minting Token)...")
    user_id = "wiki_user_id_123" # Simulating the ID Better Auth would assign
    user_email = "wiki332@gmail.com"
    user_name = "wiki"
    
    # We need to ensure this user exists in the DB first for the backend to accept the token
    # (Since backend checks DB for user_id)
    # We will use a direct DB insert to "signup" this user if they don't exist
    from sqlmodel import Session, select
    from src.database import engine
    from src.models.user import User
    
    try:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == user_email)).first()
            if not user:
                print(f"    User {user_email} not found, creating manually...")
                user = User(
                    id=user_id,
                    email=user_email,
                    name=user_name,
                    emailVerified=True,
                    image=None,
                    password="hashedpassword_placeholder"
                )
                session.add(user)
                session.commit()
                print("    User created in DB.")
            else:
                user_id = user.id
                print(f"    User found: {user.id}")
                
    except Exception as e:
        print(f"    ❌ DB Connection failed: {e}")
        return

    token = create_access_token(
        data={"sub": user_id, "name": user_name}, 
        expires_delta=timedelta(days=7)
    )
    headers = {"Authorization": f"Bearer {token}"}
    print("    Token generated.")

    # 2. Test Backend API: Get Tasks
    print("\n[2] Testing GET /api/tasks...")
    try:
        response = requests.get(f"{API_URL}/tasks", headers=headers)
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            print("    ✅ Success")
            print(f"    Tasks: {response.json()}")
        else:
            print(f"    ❌ Failed: {response.text}")
    except Exception as e:
        print(f"    ❌ Connection failed: {e}")

    # 3. Test Backend API: Create Task
    print("\n[3] Testing POST /api/tasks...")
    task_payload = {
        "title": "Integration Verify Task",
        "description": "Created via simulation script",
        "user_id": user_id # Included based on schema, though backend often infers from token
    }
    try:
        response = requests.post(f"{API_URL}/tasks", json=task_payload, headers=headers)
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            print("    ✅ Success")
            task_data = response.json()
            print(f"    Created Task ID: {task_data.get('id')}")
            
            # 4. Clean up (Delete Task)
            print("\n[4] Testing DELETE /api/tasks/{id}...")
            del_response = requests.delete(f"{API_URL}/tasks/{task_data.get('id')}", headers=headers)
            if del_response.status_code == 200:
                 print("    ✅ Task Deleted")
            else:
                 print(f"    ❌ Delete Failed: {del_response.text}")

        else:
            print(f"    ❌ Failed: {response.text}")
    except Exception as e:
         print(f"    ❌ Create Task Failed: {e}")

if __name__ == "__main__":
    test_full_flow()
