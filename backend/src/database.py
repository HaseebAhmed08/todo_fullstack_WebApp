from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
import logging

# Load environment variables
load_dotenv()

# Get database URL from environment - prioritize DATABASE_URL first
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DB_URL")

# Fallback to SQLite only if neither environment variable is set
if not DATABASE_URL:
    print("WARNING: No database URL found in environment variables. Using SQLite for development.")
    DATABASE_URL = "sqlite:///./todo_app.db"
else:
    print(f"Using database: {DATABASE_URL}")

# Determine if using PostgreSQL or SQLite to set appropriate connection args
if DATABASE_URL.startswith("postgresql://"):
    # PostgreSQL-specific connection arguments
    connect_kwargs = {
        "connect_timeout": 10,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 3,
        "sslmode": "require"
    }
else:
    # SQLite-specific connection arguments
    connect_kwargs = {"check_same_thread": False}

# Create the engine with connection pooling for Neon Serverless
engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args=connect_kwargs
)

def get_session() -> Generator[Session, None, None]:
    """
    Generator function to provide database sessions with proper error handling.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise
    finally:
        session.close()

def get_session_no_commit() -> Generator[Session, None, None]:
    """
    Generator function to provide database sessions without auto-commit.
    This allows for explicit transaction control in services.
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            logging.error(f"Database error occurred: {str(e)}")
            raise