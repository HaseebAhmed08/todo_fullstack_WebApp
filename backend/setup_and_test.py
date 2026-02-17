# Filename: setup_and_test.py
# Purpose: Full reset and setup script for FastAPI backend with SQLite + SQLModel
# Functionality:
# 1. Delete the old SQLite database if it exists.
# 2. Create new database tables for User, Todo, and Task with correct table names.
# 3. Verify the tables are created.
# 4. Test signup via HTTP request to your FastAPI backend.

import os
import sys
import uuid
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional

# -------------------------------
# 1. Paths & Database Setup
# -------------------------------
BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "todo_app_dev.db"  # This is the SQLite DB file

# Delete old database (if it exists) to start fresh
if DB_FILE.exists():
    try:
        os.remove(DB_FILE)
        print(f"Old database '{DB_FILE.name}' deleted successfully.")
    except Exception as e:
        print(f"Could not delete database: {e}")
else:
    print("No existing database file found. Starting fresh.")

# Ensure 'src' folder is in path for model imports
sys.path.append(str(BASE_DIR / "src"))

# -------------------------------
# 2. SQLModel / SQLAlchemy Imports
# -------------------------------
from sqlmodel import SQLModel, Field, create_engine
from sqlalchemy import inspect

# -------------------------------
# 3. Define Models
# -------------------------------
# User table (avoid reserved SQL keywords by using 'users')
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str
    name: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Todo table
class Todo(SQLModel, table=True):
    __tablename__ = "todo"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")  # Foreign key to 'users' table
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Task table
class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    title: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------
# 4. Create Engine & Tables
# -------------------------------
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)  # SQLite engine
SQLModel.metadata.create_all(engine)  # Creates all tables
print("Tables created successfully!")

# -------------------------------
# 5. Verify Tables
# -------------------------------
insp = inspect(engine)
tables = insp.get_table_names()
print("Existing tables:", tables)

# Check specific tables
for t in ["users", "todo", "task"]:
    if t in tables:
        print(f"Table '{t}' exists")
    else:
        print(f"Table '{t}' does NOT exist. Check your models!")

# -------------------------------
# 6. Test Signup Endpoint
# -------------------------------
# Make sure your FastAPI backend is running on this URL
SIGNUP_URL = "http://127.0.0.1:5000/api/auth/signup"

payload = {
    "email": "test@example.com",
    "password": "123456",
    "name": "Test User"
}

try:
    resp = requests.post(SIGNUP_URL, json=payload)
    print("🔹 Signup response:", resp.status_code, resp.text)
except requests.exceptions.ConnectionError:
    print("⚠️ Could not connect to the server. Is FastAPI running on port 5000?")
except Exception as e:
    print("⚠️ An error occurred during signup request:", e)

# -------------------------------
# ✅ Instructions:
# -------------------------------
# 1. Stop your FastAPI server before running this script.
# 2. Run this script using:
#    python setup_and_test.py
# 3. It will delete your old database, create new tables, and test signup.
# 4. Check console output to ensure tables exist and signup works.
# 5. Start FastAPI server after running this if needed.