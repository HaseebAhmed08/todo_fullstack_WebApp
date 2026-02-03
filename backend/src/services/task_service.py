from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from datetime import datetime
import logging

class TaskService:
    """
    Service layer for Task operations.
    Handles all business logic related to task management with user association.
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        """
        Create a new task for a specific user.
        """
        try:
            # Create task object with user association
            db_task = Task(
                title=task_data.title,
                description=task_data.description,
                completed=task_data.completed,
                user_id=task_data.user_id  # Ensure the task is linked to the correct user
            )

            # Add to session and commit
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return db_task
        except Exception as e:
            logging.error(f"Error creating task for user {task_data.user_id}: {str(e)}")
            session.rollback()
            raise e

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str) -> List[Task]:
        """
        Retrieve all tasks for a specific user.
        """
        try:
            statement = select(Task).where(Task.user_id == user_id)
            tasks = session.exec(statement).all()
            return tasks
        except Exception as e:
            logging.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
            raise e

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by ID for a specific user.
        """
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()
            return task
        except Exception as e:
            logging.error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
            raise e

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a specific task for a specific user.
        """
        try:
            # Get the task and ensure it belongs to the user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            # Update fields that are provided
            if task_update.title is not None:
                db_task.title = task_update.title
            if task_update.description is not None:
                db_task.description = task_update.description
            if task_update.completed is not None:
                db_task.completed = task_update.completed

            db_task.updated_at = datetime.utcnow()

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return db_task
        except Exception as e:
            logging.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            session.rollback()
            raise e

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a specific task for a specific user.
        """
        try:
            # Get the task and ensure it belongs to the user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return False

            session.delete(db_task)
            session.commit()

            return True
        except Exception as e:
            logging.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            session.rollback()
            raise e

    @staticmethod
    def update_task_completion(session: Session, task_id: str, user_id: str, completed: bool) -> Optional[Task]:
        """
        Update the completion status of a specific task for a specific user.
        """
        try:
            # Get the task and ensure it belongs to the user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            # Update completion status
            db_task.completed = completed
            db_task.updated_at = datetime.utcnow()

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return db_task
        except Exception as e:
            logging.error(f"Error updating completion for task {task_id} for user {user_id}: {str(e)}")
            session.rollback()
            raise e