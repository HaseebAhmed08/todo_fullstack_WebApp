import os
import sys
import traceback

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session
from src.database import engine
from src.services.task_service import TaskService
from src.models.task import TaskCreate
from src.models.user import User

def debug_create_task():
    print("Debugging Task Creation...")
    user_id = "wiki_user_id_123" # Must match the user we created
    
    task_data = TaskCreate(
        title="Debug Task",
        description="Testing creation",
        user_id=user_id
    )
    
    try:
        with Session(engine) as session:
            print(f"Attempting to create task for user: {user_id}")
            task = TaskService.create_task(session, task_data, user_id)
            print(f"✅ Task created: {task.id}")
            
            # Cleanup
            session.delete(task)
            session.commit()
            print("Cleanup: Task deleted.")
            
    except Exception:
        print("❌ Error creating task:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_create_task()
