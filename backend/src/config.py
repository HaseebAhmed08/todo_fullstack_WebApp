import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # Authentication settings
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "mySuperSecretBetterAuthSecret32Chars")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Application settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Todo App Backend API"
    VERSION: str = "1.0.0"

    # CORS settings
    BACKEND_CORS_ORIGINS: str = os.getenv("BACKEND_CORS_ORIGINS", "*")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings instance
settings = Settings()