"""
Fix User Table Schema for Better Auth
Drops and recreates user table with camelCase column names
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import SQLModel, text
from src.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.todo import Todo

def fix_user_table():
    print("Fixing user table schema for Better Auth compatibility...")
    print(f"Database URL: {engine.url}")
    
    try:
        with engine.connect() as conn:
            # Drop tables in correct order (foreign keys first)
            print("Dropping task and todo tables...")
            conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS todo CASCADE"))
            
            print("Dropping user table...")
            conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
            
            conn.commit()
            print("✅ Tables dropped")
        
        # Recreate all tables with correct schema
        print("Creating tables with camelCase columns...")
        SQLModel.metadata.create_all(engine)
        print("✅ Tables created successfully!")
        
        # Verify the schema
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user' 
                ORDER BY ordinal_position
            """))
            columns = [row[0] for row in result]
            print(f"\nUser table columns: {columns}")
            
            if "createdAt" in columns and "updatedAt" in columns:
                print("✅ Schema verified: camelCase columns present")
            else:
                print("❌ Warning: Expected camelCase columns not found")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_user_table()
