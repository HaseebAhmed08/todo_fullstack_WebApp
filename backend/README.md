# Todo App Backend

Backend API for the Phase II Todo App with authentication and todo management.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT with Better Auth integration
- **Language**: Python 3.9+

## Features

- User authentication (register, login, logout)
- Todo CRUD operations (Create, Read, Update, Delete)
- Todo filtering and sorting
- Bulk operations on todos
- JWT-based authentication and authorization

## Installation

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Set up environment variables in `.env` file

## Environment Variables

Copy `.env.example` to `.env` and update the values:

- `NEON_DB_URL`: PostgreSQL database URL
- `BETTER_AUTH_SECRET`: Secret key for JWT signing
- `BETTER_AUTH_URL`: Better Auth service URL
- `NEXT_PUBLIC_API_URL`: Public API URL

## Running the Application

1. Make sure your environment is activated
2. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```
3. The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, API documentation is available at:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Running Tests

To run the tests:

```bash
pytest tests/
```

## Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/logout` - Logout

### Todos
- `GET /api/todos/` - Get user's todos with optional filtering
- `POST /api/todos/` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status
- `POST /api/todos/bulk` - Perform bulk operations

## Database Migrations

To run database migrations:

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "Migration message"
```

## Deployment

The application can be deployed using Docker:

```bash
docker build -t todo-backend .
docker run -p 8000:8000 todo-backend
```