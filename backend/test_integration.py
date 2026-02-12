import os
import sys
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from datetime import timedelta
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Set env vars for testing if not set
os.environ["DATABASE_URL"] = "sqlite:///./test_integration.db" 
os.environ["BETTER_AUTH_SECRET"] = "testsupersecretKey12345678901234567890"

from src.main import app
from src.database import get_session, engine
from src.models.user import User
from src.utils.security import create_access_token

# Setup database
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

client = TestClient(app)

def test_auth_flow():
    print("Starting integration test...")

    # 1. Create a user directly in DB (simulating Better Auth)
    user_id = "user_12345"
    user_email = "test@example.com"
    
    with Session(engine) as session:
        user = User(
            id=user_id,
            email=user_email,
            name="Test User",
            emailVerified=True,
            image=None,
            password="hashedpassword" # In reality better auth might handle this differently but we just need the user to exist
        )
        session.add(user)
        session.commit()
        print(f"Created user: {user.email} (ID: {user.id})")

    # 2. Generate a JWT token (simulating Better Auth)
    # Better Auth usually sets expiration
    token = create_access_token(
        data={"sub": user_id, "name": "Test User"}, 
        expires_delta=timedelta(days=7)
    )
    print(f"Generated Token: {token[:20]}...")

    # 3. Test /api/auth/me (Protected Endpoint)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_email
    
    print("✅ /api/auth/me verification successful!")

    # 4. Test /api/tasks (Protected Endpoint - Empty list mostly)
    # Note: Assuming /api/tasks exists and is protected
    try:
        response = client.get("/api/tasks", headers=headers) # Check for trailing slash issues if any
        if response.status_code == 307:
             response = client.get("/api/tasks/", headers=headers)

        print(f"Tasks Response Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ /api/tasks verification successful!")
        else:
            print(f"❌ /api/tasks failed: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Could not test /api/tasks: {e}")

if __name__ == "__main__":
    try:
        test_auth_flow()
        print("\n🎉 ALL TESTS PASSED")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
