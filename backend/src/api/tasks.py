from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..api.auth import get_current_user # Updated import
from ..database import get_session
from ..services.task_service import TaskService
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskComplete
from ..models.user import User # New import
import logging

router = APIRouter(prefix="/{user_id}/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own tasks")
        
    try:
        # Get tasks for the authenticated user using the service
        tasks = TaskService.get_tasks_by_user(session, current_user.id)
        return tasks
    except Exception as e:
        logging.error(f"Error retrieving tasks for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")


@router.post("/", response_model=TaskRead)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own tasks")
        
    try:
        # Create the task using the service, assigning user_id from current_user
        db_task = TaskService.create_task(session, task_data, user_id=current_user.id)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error creating task for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID for the authenticated user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own tasks")
        
    try:
        # Get the task using the service
        db_task = TaskService.get_task_by_id_and_user(session, task_id, current_user.id)

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task")


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own tasks")
        
    try:
        # Update the task using the service
        db_task = TaskService.update_task(session, task_id, current_user.id, task_data)

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return db_task
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.patch("/{task_id}/complete", response_model=TaskRead)
def update_task_completion(
    user_id: str,
    task_id: str,
    completion_data: TaskComplete,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session)
):
    """
    Update the completion status of a specific task.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own tasks")
        
    try:
        # Update the task completion using the service
        db_task = TaskService.update_task_completion(session, task_id, current_user.id, completion_data.completed) # Access .id directly

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return db_task
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating completion for task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update task completion")


@router.delete("/{task_id}")
def delete_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user.
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own tasks")
        
    try:
        # Delete the task using the service
        success = TaskService.delete_task(session, task_id, current_user.id) # Access .id directly

        if not success:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"success": True, "message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error deleting task {task_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete task")