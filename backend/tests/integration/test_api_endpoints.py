"""
Integration tests for API endpoints with proper authentication and database handling.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.database import engine, get_session
from sqlmodel import Session, select
from src.models.user import User
from src.models.todo import Todo
from src.utils.jwt_utils import create_access_token
from datetime import timedelta


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user():
    """Create a test user."""
    user_data = {
        "email": "integration_test@example.com",
        "name": "Integration Test User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 'password' hashed
    }

    with Session(engine) as session:
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        yield user
        # Cleanup
        session.delete(user)
        session.commit()


def test_create_and_get_todos(client, test_user):
    """Test creating and retrieving todos with proper authentication."""
    # Create JWT token for the test user
    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": test_user.id, "email": test_user.email, "name": test_user.name},
        expires_delta=access_token_expires
    )

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Integration Test Todo",
            "description": "This is a test todo for integration testing",
            "user_id": test_user.id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_todo = response.json()
    assert created_todo["title"] == "Integration Test Todo"
    assert created_todo["user_id"] == test_user.id

    # Retrieve the todo
    response = client.get(
        f"/todos/{created_todo['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    retrieved_todo = response.json()
    assert retrieved_todo["id"] == created_todo["id"]
    assert retrieved_todo["title"] == "Integration Test Todo"


def test_update_todo(client, test_user):
    """Test updating a todo with proper authentication."""
    # Create JWT token for the test user
    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": test_user.id, "email": test_user.email, "name": test_user.name},
        expires_delta=access_token_expires
    )

    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Original Title",
            "description": "Original Description",
            "user_id": test_user.id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    todo = response.json()

    # Update the todo
    response = client.put(
        f"/todos/{todo['id']}",
        json={
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["title"] == "Updated Title"
    assert updated_todo["completed"] is True


def test_delete_todo(client, test_user):
    """Test deleting a todo with proper authentication."""
    # Create JWT token for the test user
    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": test_user.id, "email": test_user.email, "name": test_user.name},
        expires_delta=access_token_expires
    )

    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Todo to Delete",
            "description": "This will be deleted",
            "user_id": test_user.id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    todo = response.json()

    # Delete the todo
    response = client.delete(
        f"/todos/{todo['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Verify the todo is gone
    response = client.get(
        f"/todos/{todo['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_auth_required_for_todos(client, test_user):
    """Test that authentication is required for todo operations."""
    # Try to create a todo without authentication
    response = client.post(
        "/todos/",
        json={
            "title": "Unauthorized Todo",
            "description": "This should fail",
            "user_id": test_user.id
        }
    )
    assert response.status_code == 403  # Should be 403 or 401 depending on middleware

    # Try with invalid token
    response = client.post(
        "/todos/",
        json={
            "title": "Unauthorized Todo",
            "description": "This should fail",
            "user_id": test_user.id
        },
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_database_error_handling(client, test_user):
    """Test that database errors are handled gracefully."""
    # Create JWT token for the test user
    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": test_user.id, "email": test_user.email, "name": test_user.name},
        expires_delta=access_token_expires
    )

    # Try to create a todo with an invalid user ID (should fail gracefully)
    response = client.post(
        "/todos/",
        json={
            "title": "Todo with Invalid User",
            "description": "This should fail gracefully",
            "user_id": "invalid_user_id"  # This should cause an error
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    # Should return a 500 or 400 error, not crash the server
    assert response.status_code in [400, 403, 500]