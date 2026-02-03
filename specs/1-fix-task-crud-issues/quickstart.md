# Quickstart Guide: Task CRUD Issues Fix

## Prerequisites
- Node.js v18+ installed
- Python 3.11+ installed
- PostgreSQL-compatible database (Neon Serverless)
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Update .env with your Neon PostgreSQL connection details

# Run database migrations
python -m alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env
# Update .env with backend API URL

# Start the frontend development server
npm run dev
```

## Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Key Endpoints
- Backend API: http://localhost:8000/api/v1
- Frontend: http://localhost:3000

## Troubleshooting
- If text contrast issues persist, check that Tailwind CSS is properly configured
- For database connection issues, verify your Neon PostgreSQL credentials
- For authentication problems, ensure JWT secret is properly configured