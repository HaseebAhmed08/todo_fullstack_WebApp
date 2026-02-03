#!/bin/bash

# Startup script for Todo App Backend

echo "Starting Todo App Backend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if requirements.txt is newer than venv
if [ ! -d "venv" ] || [ "requirements.txt" -nt "venv" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload