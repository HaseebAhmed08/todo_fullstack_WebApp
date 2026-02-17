#!/usr/bin/env python
"""Test script to debug signup functionality"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.user_service import UserService
from src.models.user import UserCreate
from src.database import engine, get_session
from sqlmodel import Session

def test_signup():
    print("Testing signup functionality...")
    
    # Create a new session
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Create test user data
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="password"
        )
        
        print("Attempting to create user...")
        user = UserService.create_user(session, user_data)
        print(f"User created successfully: {user.email}")
        print(f"User ID: {user.id}")
        
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            session.close()
        except:
            pass

if __name__ == "__main__":
    test_signup()