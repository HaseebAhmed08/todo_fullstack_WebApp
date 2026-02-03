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
    NEON_DB_URL: str = os.getenv("NEON_DB_URL", "postgresql://user:password@localhost/dbname")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # Authentication settings
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3002")
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
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