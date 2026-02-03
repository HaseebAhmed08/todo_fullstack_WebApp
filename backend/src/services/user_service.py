from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate
from ..utils.jwt_utils import get_password_hash
from datetime import datetime

class UserService:
    """
    Service layer for User operations.
    Handles all business logic related to user management.
    """

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user with hashed password.
        """
        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create user object with hashed password
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Retrieve a user by ID.
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        """
        user = UserService.get_user_by_email(session, email)
        if not user:
            return None

        # We would need to import verify_password here, but it's already in jwt_utils
        from ..utils.jwt_utils import verify_password
        if not verify_password(password, user.password_hash):
            return None

        # Update last login time
        user.last_login_at = datetime.utcnow()
        session.add(user)
        session.commit()

        return user

    @staticmethod
    def update_user(session: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """
        Update user information.
        """
        db_user = UserService.get_user_by_id(session, user_id)
        if not db_user:
            return None

        # Update fields that are provided
        if user_update.name is not None:
            db_user.name = user_update.name
        if user_update.email is not None:
            db_user.email = user_update.email

        db_user.updated_at = datetime.utcnow()

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def delete_user(session: Session, user_id: str) -> bool:
        """
        Mark a user as inactive (soft delete).
        """
        db_user = UserService.get_user_by_id(session, user_id)
        if not db_user:
            return False

        db_user.is_active = False
        db_user.updated_at = datetime.utcnow()

        session.add(db_user)
        session.commit()

        return True