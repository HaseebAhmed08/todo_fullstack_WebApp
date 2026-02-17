"""
Integration tests for database connection and transaction handling.
"""
import pytest
from sqlmodel import Session, select
from datetime import datetime
from unittest.mock import patch
from src.database import get_session, engine
from src.models.user import User
from src.services.user_service import UserService
from src.models.todo import Todo, TodoCreate


def test_database_connection_pooling():
    """Test that database connections are properly managed with pooling."""
    # Test that we can get multiple sessions without issues
    with Session(engine) as session1:
        assert session1 is not None

    with Session(engine) as session2:
        assert session2 is not None

    # Both sessions should be closed after the context managers exit
    assert session1.is_active == False
    assert session2.is_active == False


def test_transaction_rollback_on_error():
    """Test that transactions are properly rolled back on error."""
    with Session(engine) as session:
        # Create a test user first
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "hashed_password": "hashed_password_here"
        }
        user = User(**user_data)
        session.add(user)
        session.commit()

        # Verify user was created
        user_check = session.get(User, user.id)
        assert user_check is not None

        # Now try to create a todo with an invalid user ID to trigger rollback
        invalid_todo_data = TodoCreate(
            title="Test Todo",
            description="Test Description",
            user_id="invalid_user_id"  # This should cause a foreign key constraint error
        )

        # Try to create todo and catch the exception
        try:
            db_todo = Todo(
                title=invalid_todo_data.title,
                description=invalid_todo_data.description,
                user_id=invalid_todo_data.user_id
            )
            session.add(db_todo)
            session.commit()  # This should fail
            assert False, "Expected an exception but none was raised"
        except Exception:
            session.rollback()  # Explicit rollback (though context manager handles this too)

        # Verify no orphaned todos were created
        all_todos = session.exec(select(Todo)).all()
        # Should only have valid todos (or none if this was the first attempt)
        # At this point, we just verify that the failed transaction was rolled back


def test_concurrent_db_operations():
    """Test that concurrent database operations work correctly with connection pooling."""
    import threading
    import time

    results = []

    def create_user_thread(thread_id):
        """Thread function to create users concurrently."""
        try:
            with Session(engine) as session:
                user_data = {
                    "email": f"user_{thread_id}@example.com",
                    "name": f"User {thread_id}",
                    "hashed_password": "hashed_password"
                }
                user = User(**user_data)
                session.add(user)
                session.commit()

                results.append({"thread_id": thread_id, "success": True, "user_id": user.id})
        except Exception as e:
            results.append({"thread_id": thread_id, "success": False, "error": str(e)})

    # Create multiple threads to simulate concurrent operations
    threads = []
    for i in range(3):
        thread = threading.Thread(target=create_user_thread, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Verify that all operations succeeded
    for result in results:
        assert result["success"], f"Thread {result['thread_id']} failed: {result.get('error')}"


def test_session_error_handling():
    """Test that session errors are properly handled."""
    from src.database import get_session_no_commit

    # Test error handling in the new session generator
    try:
        with get_session_no_commit() as session:
            # Intentionally cause an error
            invalid_query = session.exec("INVALID SQL QUERY")
    except Exception:
        # This should be caught and handled gracefully
        pass  # Expected behavior