"""
Create Better Auth Required Tables
Manually creates user, session, account, and verification tables
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import text
from src.database import engine

def create_better_auth_tables():
    print("Creating Better Auth tables...")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # Create user table
            print("\n[1] Creating user table...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS "user" (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    "emailVerified" BOOLEAN NOT NULL DEFAULT FALSE,
                    name TEXT NOT NULL,
                    image TEXT,
                    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("    ✅ User table created")
            
            # Create session table
            print("\n[2] Creating session table...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS session (
                    id TEXT PRIMARY KEY,
                    "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                    "expiresAt" TIMESTAMP NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    "ipAddress" TEXT,
                    "userAgent" TEXT,
                    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("    ✅ Session table created")
            
            # Create account table
            print("\n[3] Creating account table...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS account (
                    id TEXT PRIMARY KEY,
                    "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                    "accountId" TEXT NOT NULL,
                    "providerId" TEXT NOT NULL,
                    "accessToken" TEXT,
                    "refreshToken" TEXT,
                    "idToken" TEXT,
                    "expiresAt" TIMESTAMP,
                    password TEXT,
                    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("    ✅ Account table created")
            
            # Create verification table
            print("\n[4] Creating verification table...")
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS verification (
                    id TEXT PRIMARY KEY,
                    identifier TEXT NOT NULL,
                    value TEXT NOT NULL,
                    "expiresAt" TIMESTAMP NOT NULL,
                    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("    ✅ Verification table created")
            
            conn.commit()
            
            # Verify tables exist
            print("\n[5] Verifying tables...")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('user', 'session', 'account', 'verification')
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            
            print(f"    Tables created: {tables}")
            
            required = ['account', 'session', 'user', 'verification']
            if all(t in tables for t in required):
                print("\n✅ All Better Auth tables created successfully!")
            else:
                missing = [t for t in required if t not in tables]
                print(f"\n❌ Missing tables: {missing}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_better_auth_tables()
