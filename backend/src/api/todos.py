from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_session_no_commit
from ..api.auth import get_current_user # Updated import
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ..services.todo_service import TodoService
from ..models.user import User # Imported User model for type hinting
import logging

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model=List[TodoRead])
def get_todos(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    sort_by: Optional[str] = "date",
    sort_order: Optional[str] = "asc",
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit)
):
    """
    Retrieve user's todo list with optional filtering and pagination.
    """
    user_id = current_user.id # Access .id directly

    try:
        todos = TodoService.get_todos_by_user(
            session=session,
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return todos
    except Exception as e:
        logging.error(f"Error retrieving todos: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todos")


@router.post("/", response_model=TodoRead)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit)
):
    """
    Create a new todo item.
    """
    user_id = current_user.id # Access .id directly

    try:
        # Create a Todo instance with the user_id from the authenticated user
        db_todo = Todo(
            **todo_data.dict(), # Unpack the TodoCreate data
            user_id=user_id # Assign the authenticated user's ID
        )
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    except Exception as e:
        session.rollback()
        logging.error(f"Error creating todo: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create todo")


@router.get("/{id}", response_model=TodoRead)
def get_todo(
    id: str,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit)
):
    """
    Retrieve specific todo item.
    """
    user_id = current_user.id # Access .id directly

    try:
        db_todo = TodoService.get_todo_by_id(session, id, user_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving todo: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todo")


@router.put("/{id}", response_model=TodoRead)
def update_todo(
    id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit)
):
    """
    Update specific todo item.
    """
    user_id = current_user.id # Access .id directly

    try:
        db_todo = TodoService.update_todo(session, id, user_id, todo_update)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        session.commit()
        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating todo: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update todo")


@router.delete("/{id}")
def delete_todo(
    id: str,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit)
):
    """
    Delete specific todo item.
    """
    user_id = current_user.id # Access .id directly

    try:
        success = TodoService.delete_todo(session, id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Todo not found")

        session.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error deleting todo: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete todo")


@router.patch("/{id}/toggle", response_model=TodoRead)
def toggle_todo_completion(
    id: str,
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit)
):
    """
    Toggle completion status of specific todo.
    """
    user_id = current_user.id # Access .id directly

    try:
        db_todo = TodoService.toggle_todo_completion(session, id, user_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        session.commit()
        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error toggling todo completion: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to toggle todo completion")


@router.post("/bulk")
def bulk_operations(
    operation: str,
    ids: List[str],
    current_user: User = Depends(get_current_user), # Updated type hint
    session: Session = Depends(get_session_no_commit),
    data: Optional[TodoUpdate] = None
):
    """
    Perform bulk operations on multiple todos.
    """
    user_id = current_user.id # Access .id directly

    try:
        if operation == "update":
            if not data:
                raise HTTPException(status_code=400, detail="Update data required for update operation")

            affected_count = TodoService.bulk_update_todos(session, ids, user_id, data)
            session.commit()
            return {"success": True, "affected_count": affected_count}

        elif operation == "delete":
            affected_count = TodoService.bulk_delete_todos(session, ids, user_id)
            session.commit()
            return {"success": True, "affected_count": affected_count}

        elif operation == "complete":
            # Special case: mark all as completed
            data = TodoUpdate(completed=True)
            affected_count = TodoService.bulk_update_todos(session, ids, user_id, data)
            session.commit()
            return {"success": True, "affected_count": affected_count}

        elif operation == "uncomplete":
            # Special case: mark all as not completed
            data = TodoUpdate(completed=False)
            affected_count = TodoService.bulk_update_todos(session, ids, user_id, data)
            session.commit()
            return {"success": True, "affected_count": affected_count}

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported operation: {operation}")
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logging.error(f"Error performing bulk operation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform bulk operation")