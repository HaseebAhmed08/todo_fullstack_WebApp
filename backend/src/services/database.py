from sqlmodel import create_engine, Session
from sqlalchemy import event
import os
from urllib.parse import urlparse
import logging

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("NEON_DB_URL"))

# Handle the neon.tech URL format properly
if DATABASE_URL and "neon.tech" in DATABASE_URL:
    # For Neon, we may need to adjust the connection parameters
    parsed = urlparse(DATABASE_URL)
    # Create engine with appropriate settings for Neon
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "sslmode": "require",
            "channel_binding": "require"
        },
        pool_recycle=300,
        pool_pre_ping=True,
    )
else:
    engine = create_engine(DATABASE_URL) if DATABASE_URL else create_engine("sqlite:///default.db")


def get_session():
    with Session(engine) as session:
        yield session


def get_session_with_error_handling():
    """
    Get database session with error handling and logging.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logging.error(f"Database session error: {str(e)}")
        raise


def handle_database_error(error: Exception, operation: str = "database operation"):
    """
    Log database errors appropriately.
    """
    logging.error(f"Database error during {operation}: {str(error)}")
    raise error