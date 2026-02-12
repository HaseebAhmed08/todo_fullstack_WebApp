"""
Inspect User and Account Records
Checks if user exists and has a corresponding credential account
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import text
from src.database import engine

def inspect_user(email):
    print(f"Inspecting records for: {email}")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # 1. Check user table
            print("\n[1] Checking 'user' table...")
            result = conn.execute(text('SELECT * FROM "user" WHERE email = :email'), {"email": email})
            user = result.fetchone()
            
            if user:
                user_dict = dict(user._mapping)
                print(f"    ✅ User record found:")
                for k, v in user_dict.items():
                    print(f"      - {k}: {v}")
                user_id = user_dict['id']
                
                # 2. Check account table
                print("\n[2] Checking 'account' table for user ID...")
                result = conn.execute(text('SELECT * FROM account WHERE "userId" = :user_id'), {"user_id": user_id})
                account = result.fetchone()
                
                if account:
                    account_dict = dict(account._mapping)
                    print(f"    ✅ Account record found:")
                    for k, v in account_dict.items():
                        # Mask password
                        val = "********" if k == 'password' and v else v
                        print(f"      - {k}: {val}")
                else:
                    print(f"    ❌ No account record found for user ID: {user_id}")
            else:
                print(f"    ❌ No user record found for email: {email}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "wiki33@gmail.com"
    inspect_user(email)
