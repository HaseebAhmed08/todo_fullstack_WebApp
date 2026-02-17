"""
Clean User Table Recreation
Fixes duplicate column issue by completely dropping and recreating
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import SQLModel, text
from src.database import engine

def clean_recreate():
    print("Cleaning and recreating user table...")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # Drop all tables to ensure clean state
            print("\n[1] Dropping all tables...")
            conn.execute(text('DROP TABLE IF EXISTS task CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS todo CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS session CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS account CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS verification CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
            conn.commit()
            print("    ✅ All tables dropped")
        
        # Import models AFTER dropping to ensure fresh metadata
        print("\n[2] Importing models...")
        from src.models.user import User
        from src.models.task import Task
        from src.models.todo import Todo
        print("    ✅ Models imported")
        
        # Create tables with clean schema
        print("\n[3] Creating tables...")
        SQLModel.metadata.create_all(engine)
        print("    ✅ Tables created")
        
        # Verify schema
        print("\n[4] Verifying schema...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user' 
                ORDER BY ordinal_position
            """))
            columns = [row[0] for row in result]
            
            print(f"\n    User table columns ({len(columns)} total):")
            for col in columns:
                print(f"      - {col}")
            
            # Check for duplicates
            if len(columns) != len(set(columns)):
                print("\n    ❌ ERROR: Duplicate columns still present!")
                from collections import Counter
                duplicates = [col for col, count in Counter(columns).items() if count > 1]
                print(f"       Duplicates: {duplicates}")
                return False
            else:
                print("\n    ✅ No duplicate columns!")
            
            # Verify required columns
            required = ['id', 'email', 'name', 'password', 'createdAt', 'updatedAt', 'emailVerified', 'image']
            missing = [col for col in required if col not in columns]
            
            if missing:
                print(f"\n    ❌ Missing required columns: {missing}")
                return False
            else:
                print(f"\n    ✅ All required columns present!")
        
        print("\n" + "=" * 60)
        print("✅ SCHEMA RECREATION SUCCESSFUL!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = clean_recreate()
    sys.exit(0 if success else 1)
