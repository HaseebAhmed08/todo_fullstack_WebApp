from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from src.api import auth, tasks, todos, users
from src.config import settings
from src.database import create_db_and_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

# CORS Configuration - Vercel ke liye
allowed_origins = [
    "http://localhost:3000",
    os.getenv("BETTER_AUTH_URL", "http://localhost:3000"),
    os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(todos.router, prefix="/api/todos", tags=["Todos"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Todo App API is running on Vercel"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Vercel serverless function handler
handler = app
