from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo, TodoCreate, TodoUpdate
from datetime import datetime

class TodoService:
    """
    Service layer for Todo operations.
    Handles all business logic related to todo management.
    """



    @staticmethod
    def get_todos_by_user(
        session: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = 'asc'
    ) -> List[Todo]:
        """
        Retrieve todos for a specific user with optional filtering and pagination.
        """
        statement = select(Todo).where(Todo.user_id == user_id)

        # Apply status filter if provided
        if status:
            if status.lower() == 'active':
                statement = statement.where(Todo.completed == False)
            elif status.lower() == 'completed':
                statement = statement.where(Todo.completed == True)

        # Apply sorting
        if sort_by:
            if sort_by.lower() == 'date':
                if sort_order.lower() == 'desc':
                    statement = statement.order_by(Todo.created_at.desc())
                else:
                    statement = statement.order_by(Todo.created_at.asc())
            elif sort_by.lower() == 'priority':
                if sort_order.lower() == 'desc':
                    statement = statement.order_by(Todo.priority.desc())
                else:
                    statement = statement.order_by(Todo.priority.asc())
            elif sort_by.lower() == 'title':
                if sort_order.lower() == 'desc':
                    statement = statement.order_by(Todo.title.desc())
                else:
                    statement = statement.order_by(Todo.title.asc())

        # Apply pagination
        statement = statement.offset(skip).limit(limit)

        todos = session.exec(statement).all()
        return todos

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: str, user_id: str) -> Optional[Todo]:
        """
        Retrieve a specific todo by ID for a specific user.
        """
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()
        return todo

    @staticmethod
    def update_todo(session: Session, todo_id: str, user_id: str, todo_update: TodoUpdate) -> Optional[Todo]:
        """
        Update a todo item if it belongs to the user.
        """
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return None

        # Update fields that are provided
        if todo_update.title is not None:
            db_todo.title = todo_update.title
        if todo_update.description is not None:
            db_todo.description = todo_update.description
        if todo_update.completed is not None:
            db_todo.completed = todo_update.completed
        if todo_update.priority is not None:
            db_todo.priority = todo_update.priority
        if todo_update.due_date is not None:
            db_todo.due_date = todo_update.due_date

        db_todo.updated_at = datetime.utcnow()

        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return db_todo

    @staticmethod
    def delete_todo(session: Session, todo_id: str, user_id: str) -> bool:
        """
        Delete a todo item if it belongs to the user.
        """
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return False

        session.delete(db_todo)
        session.commit()

        return True

    @staticmethod
    def toggle_todo_completion(session: Session, todo_id: str, user_id: str) -> Optional[Todo]:
        """
        Toggle the completion status of a todo item.
        """
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return None

        # Toggle the completed status
        db_todo.completed = not db_todo.completed
        db_todo.updated_at = datetime.utcnow()

        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return db_todo

    @staticmethod
    def get_user_todos_count(session: Session, user_id: str) -> int:
        """
        Get the total count of todos for a user.
        """
        statement = select(Todo).where(Todo.user_id == user_id)
        count = session.exec(statement).count()
        return count

    @staticmethod
    def bulk_update_todos(session: Session, todo_ids: List[str], user_id: str, update_data: TodoUpdate) -> int:
        """
        Update multiple todos at once for a user.
        """
        statement = select(Todo).where(Todo.id.in_(todo_ids), Todo.user_id == user_id)
        todos = session.exec(statement).all()

        updated_count = 0
        for todo in todos:
            if update_data.title is not None:
                todo.title = update_data.title
            if update_data.description is not None:
                todo.description = update_data.description
            if update_data.completed is not None:
                todo.completed = update_data.completed
            if update_data.priority is not None:
                todo.priority = update_data.priority
            if update_data.due_date is not None:
                todo.due_date = update_data.due_date

            todo.updated_at = datetime.utcnow()
            session.add(todo)
            updated_count += 1

        session.commit()
        return updated_count

    @staticmethod
    def bulk_delete_todos(session: Session, todo_ids: List[str], user_id: str) -> int:
        """
        Delete multiple todos at once for a user.
        """
        statement = select(Todo).where(Todo.id.in_(todo_ids), Todo.user_id == user_id)
        todos = session.exec(statement).all()

        deleted_count = 0
        for todo in todos:
            session.delete(todo)
            deleted_count += 1

        session.commit()
        return deleted_count