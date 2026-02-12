# Quickstart Guide: Authentication-first Todo App

## Overview
This guide provides the essential steps to get the authentication-first Todo app up and running with Neon PostgreSQL database integration.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.9+ for backend development
- PostgreSQL client tools (for Neon connection)
- Git for version control

## Initial Setup

### 1. Project Structure
The application follows a monorepo structure:
```
├── frontend/           # Next.js application
│   ├── app/           # App Router pages
│   ├── components/    # Reusable components
│   ├── lib/           # Utilities and services
│   └── public/        # Static assets
├── backend/           # FastAPI application
│   ├── src/           # Source code
│   │   ├── api/       # API route definitions
│   │   ├── models/    # Database models
│   │   ├── services/  # Business logic
│   │   └── utils/     # Utility functions
│   └── tests/         # Test files
└── specs/             # Specification files
```

### 2. Environment Configuration
Create `.env` files in both frontend and backend directories:

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-key
```

**Backend (.env):**
```
NEON_DB_URL=postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Setup
1. Sign up for Neon PostgreSQL account
2. Create a new project
3. Copy the connection string to your backend `.env` file
4. Run database migrations to create the required tables

## Development Workflow

### 1. Starting the Backend
```bash
cd backend
pip install -r requirements.txt
python -m src.main  # or uvicorn src.main:app --reload
```

### 2. Starting the Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. API Development
- All authentication APIs should be defined in `/backend/src/api/auth.py`
- All todo APIs should be defined in `/backend/src/api/todos.py`
- Use JWT middleware for protecting routes that require authentication
- Follow the API contracts defined in `/specs/contracts/api-contracts.md`

### 4. Frontend Development
- Authentication flow starts at `/app/page.tsx` (entry point)
- Login form at `/app/login/page.tsx`
- Signup form at `/app/signup/page.tsx`
- Todo dashboard at `/app/todos/page.tsx`
- Use Tailwind CSS for styling according to the design requirements

## Key Implementation Points

### Authentication Flow
1. User visits the site and sees login/signup options
2. User can sign up with name, email, and password
3. After signup, user is redirected to login page
4. After successful login, user is redirected to todo dashboard
5. All todo operations require authentication

### Data Persistence
- All todo operations must be persisted in Neon PostgreSQL
- Users can only access their own todos
- Proper foreign key relationships ensure data integrity
- Passwords are securely hashed before storage

### Security Measures
- JWT tokens are validated on all protected endpoints
- Passwords use industry-standard hashing algorithms
- Input validation is performed on both frontend and backend
- SQL injection prevention through parameterized queries

## Testing Approach
- Write unit tests for backend API endpoints
- Write integration tests for authentication flow
- Test multi-user data isolation
- Validate all error handling scenarios
- Verify protected route enforcement