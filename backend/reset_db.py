import sqlite3
import os

# Get the database path
db_path = os.path.join(os.path.dirname(__file__), 'todo_app.db')

# Delete the database if it exists
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted {db_path}")

# Create a new database with the correct schema
from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.todo import Todo
from src.models.task import Task

engine = create_engine("sqlite:///./todo_app.db")

print("Creating new database schema...")
SQLModel.metadata.create_all(engine)
print("Database schema created successfully!")

# Verify the user table
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(user)")
columns = cursor.fetchall()

print("\nUser table columns:")
for col in columns:
    print(f"  {col[1]}: {col[2]} (max_length: {col[5]})")

conn.close()
