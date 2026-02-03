from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any

class TodoAppException(Exception):
    """Base exception class for the Todo App."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(TodoAppException):
    """Exception raised for validation errors."""
    def __init__(self, message: str):
        super().__init__(message, 400)

class AuthenticationError(TodoAppException):
    """Exception raised for authentication errors."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)

class AuthorizationError(TodoAppException):
    """Exception raised for authorization errors."""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, 403)

class NotFoundError(TodoAppException):
    """Exception raised when a resource is not found."""
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", 404)

class ConflictError(TodoAppException):
    """Exception raised when there's a resource conflict."""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, 409)

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": exc.message
            }
        }
    )

async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    """Handle authentication exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "AUTHENTICATION_FAILED",
                "message": exc.message
            }
        }
    )

async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    """Handle authorization exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "INSUFFICIENT_PERMISSIONS",
                "message": exc.message
            }
        }
    )

async def not_found_exception_handler(request: Request, exc: NotFoundError):
    """Handle not found exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": exc.message
            }
        }
    )

async def conflict_exception_handler(request: Request, exc: ConflictError):
    """Handle conflict exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "CONFLICT",
                "message": exc.message
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred"
            }
        }
    )