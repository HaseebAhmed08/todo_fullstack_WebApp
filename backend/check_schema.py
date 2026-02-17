"""
Check Database Schema for Better Auth Compatibility
Verifies all required columns exist with correct names
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import text
from src.database import engine

def check_schema():
    print("Checking database schema for Better Auth compatibility...\n")
    
    try:
        with engine.connect() as conn:
            # Check user table columns
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'user' 
                ORDER BY ordinal_position
            """))
            
            columns = list(result)
            
            print("User table columns:")
            print("-" * 60)
            for col in columns:
                print(f"  {col[0]:<20} {col[1]:<20} Nullable: {col[2]}")
            
            # Check for required Better Auth columns
            column_names = [col[0] for col in columns]
            required_columns = ['id', 'email', 'name', 'password', 'createdAt', 'updatedAt']
            
            print("\n" + "=" * 60)
            print("Required Better Auth Columns Check:")
            print("=" * 60)
            
            all_present = True
            for req_col in required_columns:
                if req_col in column_names:
                    print(f"  ✅ {req_col}")
                else:
                    print(f"  ❌ {req_col} - MISSING")
                    all_present = False
            
            if all_present:
                print("\n✅ All required columns present!")
            else:
                print("\n❌ Some required columns are missing!")
                
            # Check for duplicate columns
            if len(column_names) != len(set(column_names)):
                print("\n⚠️  WARNING: Duplicate columns detected!")
                from collections import Counter
                duplicates = [col for col, count in Counter(column_names).items() if count > 1]
                print(f"   Duplicates: {duplicates}")
                
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_schema()
