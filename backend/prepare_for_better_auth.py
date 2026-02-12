"""
Let Better Auth Own the User Table
Drops user table and removes it from backend management
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import text
from src.database import engine

def prepare_for_better_auth():
    print("Preparing database for Better Auth ownership...")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # Drop all tables
            print("\n[1] Dropping all tables...")
            conn.execute(text('DROP TABLE IF EXISTS task CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS todo CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS session CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS account CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS verification CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
            conn.commit()
            print("    ✅ All tables dropped")
        
        print("\n[2] Better Auth will create the user table on next frontend start")
        print("    The backend will only manage task and todo tables")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE PREPARED")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Restart frontend (npm run dev)")
        print("2. Better Auth will auto-create user table")
        print("3. Backend will create task/todo tables on startup")
        print("4. Try signup again")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    prepare_for_better_auth()
