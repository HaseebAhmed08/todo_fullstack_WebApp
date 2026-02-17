import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session, select
from src.database import engine
from src.models.user import User

try:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print("--- Users Found ---")
        for user in users:
            print(f"Name: {user.name}, Email: {user.email}, ID: {user.id}")
        if not users:
            print("No users found yet.")
except Exception as e:
    print(f"Error querying users: {e}")
