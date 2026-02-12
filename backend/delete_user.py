"""
Delete User Data
Removes a user from the 'user' table and associated tables
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import text
from src.database import engine

def delete_user(email):
    print(f"Deleting all records for: {email}")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # First find the user ID
            result = conn.execute(text('SELECT id FROM "user" WHERE email = :email'), {"email": email})
            user = result.fetchone()
            
            if user:
                user_id = user[0]
                print(f"Found user ID: {user_id}")
                
                # Tables to clean (Better Auth tables handle cascade if set up, but let's be safe)
                # Note: session and account have userId columns with references
                
                print("Deleting from account...")
                conn.execute(text('DELETE FROM account WHERE "userId" = :user_id'), {"user_id": user_id})
                
                print("Deleting from session...")
                conn.execute(text('DELETE FROM session WHERE "userId" = :user_id'), {"user_id": user_id})
                
                print("Deleting from tasks...")
                conn.execute(text('DELETE FROM task WHERE user_id = :user_id'), {"user_id": user_id})
                
                print("Deleting from user...")
                conn.execute(text('DELETE FROM "user" WHERE id = :user_id'), {"user_id": user_id})
                
                conn.commit()
                print(f"\n✅ Successfully deleted user {email} and all related data.")
            else:
                print(f"❌ User with email {email} not found.")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "wiki33@gmail.com"
    delete_user(email)
