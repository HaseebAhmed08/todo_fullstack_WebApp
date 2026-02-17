import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv
load_dotenv()

from sqlmodel import SQLModel, text
from src.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.todo import Todo

def init_db():
    print("Initializing database tables on Neon DB...")
    print(f"Database URL: {engine.url}")
    try:
        # Drop the task table to fix schema mismatch (ID type integer -> string)
        # Also drop todo table as it might have similar issues or FK constraints
        print("Dropping 'task' and 'todo' tables to ensure schema alignment...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS todo CASCADE"))
            conn.commit()
            
        print("Creating new tables...")
        SQLModel.metadata.create_all(engine)
        print("✅ Tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
