from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .api.todos import router as todos_router
from .api.tasks import router as tasks_router
from .api.users import router as users_router
from .database import engine
# User model removed - Better Auth manages the user table
from .models.todo import Todo
from .models.task import Task
from sqlmodel import SQLModel
from .config import settings
from .utils.error_handlers import (
    TodoAppException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    validation_exception_handler,
    authentication_exception_handler,
    authorization_exception_handler,
    not_found_exception_handler,
    conflict_exception_handler,
    general_exception_handler
)

# Create the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for the Phase II Todo App with authentication and todo management",
    version=settings.VERSION
)

# Add CORS middleware
origins = []
if settings.BACKEND_CORS_ORIGINS == "*":
    origins.append("*")
else:
    origins.extend(settings.BACKEND_CORS_ORIGINS.split(","))

# Ensure http://localhost:3000 is always allowed for frontend development
if "http://localhost:3000" not in origins:
    origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix to match frontend expectations
app.include_router(auth_router, prefix="/api")
app.include_router(todos_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(users_router, prefix="/api")

# Register exception handlers
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(AuthenticationError, authentication_exception_handler)
app.add_exception_handler(AuthorizationError, authorization_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(ConflictError, conflict_exception_handler)
app.add_exception_handler(TodoAppException, general_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.on_event("startup")
def on_startup():
    """
    Initialize the database tables on startup.
    """
    print(f"Using database: {settings.DATABASE_URL}")
    print("Creating database tables...")
    try:
        # Create tables with checkfirst=False to force recreation if needed
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        import traceback
        traceback.print_exc()

@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    """
    return {"message": "Welcome to the Todo App Backend API"}

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "todo-backend-api"}


@app.get("/db-health")
def db_health_check():
    """
    Database health check endpoint.
    """
    try:
        # Test database connectivity by attempting a simple query
        from sqlmodel import select
        from .models.user import User
        from .database import Session

        with Session(engine) as session:
            # Execute a simple query to test connection
            result = session.exec(select(User).limit(1)).first()

        return {
            "status": "healthy",
            "service": "todo-backend-api",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "todo-backend-api",
            "database": "disconnected",
            "error": str(e)
        }


# Additional endpoints can be added here