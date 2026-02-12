# Quickstart Guide: Authentication and Persistence Fixes

## Overview
Quickstart guide for implementing authentication and persistence fixes in the Todo Full-Stack Web Application. This guide provides essential information for developers to quickly understand and contribute to the project.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)
- Git version control

### Environment Setup
1. Clone the repository
2. Install frontend dependencies: `npm install` in the frontend directory
3. Install backend dependencies: `pip install -r requirements.txt` in the backend directory
4. Set up environment variables (see Environment Variables section)

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://neondb_owner:npg_snHZf25tqdux@ep-autumn-king-ahhytk19-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=your_better_auth_url
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Project Structure
```
todo-fullstack-app/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   └── user_service.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   └── database/
│   │       └── database.py
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── login.tsx
│   │   │   │   └── signup.tsx
│   │   │   └── tasks/
│   │   │       └── index.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── lib/
│   │       └── auth.ts
│   └── tests/
└── specs/
    └── 001-auth-data-persistence/
        ├── spec.md
        ├── plan.md
        ├── research.md
        └── data-model.md
```

## Running the Application

### Backend (FastAPI)
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the development server: `uvicorn src.main:app --reload`
4. The API will be available at `http://localhost:8000`

### Frontend (Next.js)
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. The application will be available at `http://localhost:3000`

## Key Features Implementation

### Authentication Flow
1. User signs up/logins through Better Auth
2. JWT token is issued and stored securely
3. Token is sent with all API requests to backend
4. Backend verifies token and extracts user information

### User Persistence
1. When a user authenticates for the first time:
   - Backend checks if user exists in database
   - If not, creates new user record based on JWT information
2. Subsequent requests use existing user record

### Task Operations
1. All task operations require valid JWT authentication
2. Tasks are filtered by authenticated user's ID
3. Users can only create, read, update, and delete their own tasks

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User signup
- `POST /api/auth/logout` - User logout

### Tasks
- `GET /api/tasks` - Get authenticated user's tasks
- `POST /api/tasks` - Create a new task for authenticated user
- `PUT /api/tasks/{task_id}` - Update a task (user must own the task)
- `DELETE /api/tasks/{task_id}` - Delete a task (user must own the task)
- `PATCH /api/tasks/{task_id}/complete` - Mark task as complete/incomplete

## Testing

### Backend Tests
Run backend tests with: `pytest`

### Frontend Tests
Run frontend tests with: `npm run test`

## Troubleshooting

### Common Issues
1. **JWT Validation Fails**: Check that Better Auth secret is correctly configured
2. **Database Connection Issues**: Verify DATABASE_URL is properly set
3. **User Not Persisting**: Ensure auth middleware is correctly implemented

### Debugging Tips
- Enable detailed logging in development
- Check that JWT tokens are being passed correctly in headers
- Verify database indexes for performance issues