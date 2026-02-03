# Enhanced Quickstart Guide: Task CRUD Issues Fix

## Overview
This guide provides setup instructions for the enhanced Task CRUD system with improved UI styling and data persistence reliability.

## Prerequisites
- Node.js v18+ installed
- Python 3.11+ installed
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git
- Docker (optional, for containerized deployment)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (FastAPI with SQLModel)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Update .env with your Neon PostgreSQL connection details:
# NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Next.js)
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env
# Update .env with backend API URL:
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Start the frontend development server
npm run dev
```

## Enhanced Features Configuration

### 1. Database Connection Pooling (Neon Serverless)
The system is configured with optimized connection pooling for Neon Serverless:
- Pool size: 5 connections
- Max overflow: 10 connections
- Connection timeout: 10 seconds
- Connection recycle: 300 seconds (5 minutes)

### 2. JWT Authentication Setup
- Token expiration: 30 minutes
- Algorithm: HS256
- Secret key: configured in environment variables
- Refresh mechanism: implemented for extended sessions

### 3. Text Contrast Compliance (WCAG AA)
The frontend implements improved text contrast ratios:
- Primary text: text-gray-900 (high contrast)
- Secondary text: text-gray-700 (adequate contrast)
- Background contrast ratio: minimum 4.5:1 for normal text

## Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
cd backend
pytest tests/integration/
```

## API Endpoints

### Main Endpoints
- Backend API: http://localhost:8000/api/v1
- Frontend: http://localhost:3000
- Health check: http://localhost:8000/health
- Database health: http://localhost:8000/db-health

### Authentication Endpoints
- Register: POST /auth/register
- Login: POST /auth/login
- Logout: POST /auth/logout

### Task Management Endpoints
- Get all tasks: GET /todos
- Create task: POST /todos
- Get task: GET /todos/{id}
- Update task: PUT /todos/{id}
- Toggle completion: PATCH /todos/{id}/toggle
- Delete task: DELETE /todos/{id}
- Bulk operations: POST /todos/bulk

## Development Commands

### Backend Development
```bash
# Run with auto-reload
uvicorn src.main:app --reload

# Run tests with coverage
pytest --cov=src

# Format code with black
black src/

# Run linter
flake8 src/
```

### Frontend Development
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Format code with prettier
npm run format

# Run linter
npm run lint
```

## Environment Variables

### Backend (.env)
```
NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

### Common Issues
1. **Text Contrast Issues**: Check that Tailwind CSS is properly configured and that the enhanced text color classes are applied correctly.

2. **Database Connection Problems**: Verify your Neon PostgreSQL credentials and ensure the connection string includes `sslmode=require`.

3. **Authentication Problems**: Ensure JWT secret is properly configured and that the token expiration settings are appropriate.

4. **Connection Pooling Issues**: Monitor the database health endpoint (`/db-health`) to verify connection pool status.

### Health Checks
- Check API health: `curl http://localhost:8000/health`
- Check database health: `curl http://localhost:8000/db-health`
- Monitor connection pool: Check the database health response for pool statistics

### Performance Monitoring
- Response times should be under 500ms for most operations
- Database connection pool should maintain 2-5 active connections under normal load
- Memory usage should remain stable during extended operation

## Deployment

### Production Build
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm start
```

### Docker Deployment (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Security Best Practices
- Never commit secrets to version control
- Use environment variables for all sensitive configuration
- Implement proper input validation and sanitization
- Regularly update dependencies
- Monitor authentication logs for suspicious activity
- Use HTTPS in production environments