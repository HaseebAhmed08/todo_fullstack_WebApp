# API Specifications for Phase II Todo App Backend

## Purpose
Define all REST API endpoints required by the frontend, including request/response contracts, authentication requirements, and error handling patterns.

## Scope
This specification covers all HTTP endpoints that the backend must expose to support the frontend functionality, following RESTful principles and aligning with the existing frontend API consumption patterns.

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/login
Authenticate user and return JWT token
- **Auth**: Public
- **Request Body**: `{email: string, password: string}`
- **Response**: `{token: string, user: {id, email, name}}`
- **Errors**: 401 for invalid credentials

#### POST /api/auth/register
Register new user account
- **Auth**: Public
- **Request Body**: `{email: string, password: string, name: string}`
- **Response**: `{token: string, user: {id, email, name}}`
- **Errors**: 409 for duplicate email

#### POST /api/auth/logout
End user session
- **Auth**: Protected (JWT required)
- **Request**: Empty
- **Response**: `{success: boolean}`
- **Errors**: 401 for invalid/expired token

### Todo Management Endpoints

#### GET /api/todos
Retrieve user's todo list
- **Auth**: Protected (JWT required)
- **Query Params**: `page?: number, limit?: number, status?: 'all'|'active'|'completed', sortBy?: 'date'|'priority'|'title', sortOrder?: 'asc'|'desc'`
- **Response**: `{todos: Array<Todo>, pagination: {total, page, limit, totalPages}}`
- **Errors**: 401 for invalid token

#### POST /api/todos
Create a new todo item
- **Auth**: Protected (JWT required)
- **Request Body**: `{title: string, description?: string, completed?: boolean, dueDate?: string, priority?: 'low'|'medium'|'high'}`
- **Response**: `{todo: Todo}`
- **Errors**: 400 for invalid data, 401 for invalid token

#### GET /api/todos/{id}
Retrieve specific todo item
- **Auth**: Protected (JWT required)
- **Params**: `id: string (todo id)`
- **Response**: `{todo: Todo}`
- **Errors**: 401 for invalid token, 404 for non-existent todo

#### PUT /api/todos/{id}
Update specific todo item
- **Auth**: Protected (JWT required)
- **Params**: `id: string (todo id)`
- **Request Body**: Partial `Todo` object
- **Response**: `{todo: Todo}`
- **Errors**: 400 for invalid data, 401 for invalid token, 404 for non-existent todo

#### DELETE /api/todos/{id}
Delete specific todo item
- **Auth**: Protected (JWT required)
- **Params**: `id: string (todo id)`
- **Response**: `{success: boolean}`
- **Errors**: 401 for invalid token, 404 for non-existent todo

#### PATCH /api/todos/{id}/toggle
Toggle completion status of specific todo
- **Auth**: Protected (JWT required)
- **Params**: `id: string (todo id)`
- **Request**: Empty or `{completed: boolean}`
- **Response**: `{todo: Todo}`
- **Errors**: 401 for invalid token, 404 for non-existent todo

### Bulk Operations

#### POST /api/todos/bulk
Perform bulk operations on multiple todos
- **Auth**: Protected (JWT required)
- **Request Body**: `{operation: 'update'|'delete'|'complete', ids: string[], data?: Partial<Todo>}`
- **Response**: `{success: boolean, affectedCount: number}`
- **Errors**: 400 for invalid operation/data, 401 for invalid token

## Request/Response Data Contracts

### Todo Object
```
{
  id: string (unique identifier),
  userId: string (owner identifier),
  title: string (non-empty),
  description?: string,
  completed: boolean (default: false),
  createdAt: string (ISO date),
  updatedAt: string (ISO date),
  dueDate?: string (ISO date),
  priority: 'low'|'medium'|'high' (default: 'medium')
}
```

### Authentication Response
```
{
  token: string (JWT),
  user: {
    id: string,
    email: string,
    name: string
  }
}
```

## Authentication and Authorization Rules

### Public Routes
- `/api/auth/login`
- `/api/auth/register`

### Protected Routes (JWT Required)
- All `/api/todos/*` endpoints
- `/api/auth/logout`

### Authorization Logic
- Users can only access/modify their own todos
- Access control enforced via JWT validation and user ID comparison
- Unauthorized access attempts return 401 status

## Error Scenarios and Failure Responses

### Standard Error Format
```
{
  error: {
    code: string,
    message: string,
    details?: object
  }
}
```

### Common Error Codes
- `INVALID_CREDENTIALS`: 401 - Login credentials are incorrect
- `UNAUTHORIZED_ACCESS`: 401 - JWT is invalid or user doesn't own the resource
- `VALIDATION_ERROR`: 400 - Request data doesn't match expected schema
- `RESOURCE_NOT_FOUND`: 404 - Requested resource doesn't exist
- `CONFLICT`: 409 - Resource conflict (e.g., duplicate email during registration)
- `INTERNAL_ERROR`: 500 - Unexpected server error

## Pagination, Filtering, and Sorting Expectations

### Pagination
- Default page size: 20 items
- Page size configurable via `limit` query parameter (max 100)
- Response includes pagination metadata
- Zero-indexed pages unless specified otherwise

### Filtering
- `status`: Filter by completion status ('all', 'active', 'completed')
- `dueDate`: Filter by due date range
- `priority`: Filter by priority level
- Default: All todos for the authenticated user

### Sorting
- Default sort: By creation date, newest first
- Sortable fields: `createdAt`, `updatedAt`, `dueDate`, `title`, `priority`
- Sort order: Ascending or descending (controlled by `sortOrder` parameter)