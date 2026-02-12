"""
Create Better Auth JWKS Table
Manually creates the jwks table required for the JWT plugin
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import text
from src.database import engine

def create_jwks_table():
    print("Creating jwks table for Better Auth JWT plugin...")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # Create jwks table
            print("\n[1] Creating jwks table...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS jwks (
                    id TEXT PRIMARY KEY,
                    "publicKey" TEXT NOT NULL,
                    "privateKey" TEXT NOT NULL,
                    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("    ✅ jwks table created")
            
            conn.commit()
            
            # Verify table exists
            print("\n[2] Verifying table...")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'jwks'
            """))
            table_found = result.fetchone()
            
            if table_found:
                print("\n✅ JWKS table created successfully!")
            else:
                print("\n❌ JWKS table creation failed!")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_jwks_table()
