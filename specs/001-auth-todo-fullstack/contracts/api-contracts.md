# API Contracts: Authentication-first Todo App

## Authentication APIs

### POST /api/auth/register
**Purpose**: Register a new user account

**Request**:
- Method: POST
- Endpoint: `/api/auth/register`
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "name": "string (required)",
    "email": "string (required, valid email format)",
    "password": "string (required, minimum 8 characters)"
  }
  ```

**Response**:
- Success (201):
  ```json
  {
    "id": "string (user ID)",
    "name": "string (user name)",
    "email": "string (user email)",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)"
  }
  ```
- Error (400, 409):
  ```json
  {
    "detail": "string (error message)"
  }
  ```

### POST /api/auth/login
**Purpose**: Authenticate user and return JWT token

**Request**:
- Method: POST
- Endpoint: `/api/auth/login`
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (required)"
  }
  ```

**Response**:
- Success (200):
  ```json
  {
    "access_token": "string (JWT token)",
    "token_type": "string (bearer)",
    "user": {
      "id": "string (user ID)",
      "name": "string (user name)",
      "email": "string (user email)"
    }
  }
  ```
- Error (401):
  ```json
  {
    "detail": "Incorrect email or password"
  }
  ```

### POST /api/auth/logout
**Purpose**: Invalidate user session

**Request**:
- Method: POST
- Endpoint: `/api/auth/logout`
- Headers: `Authorization: Bearer {token}`
- Body: Empty

**Response**:
- Success (200):
  ```json
  {
    "message": "Successfully logged out"
  }
  ```
- Error (401):
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

## Todo APIs

### GET /api/todos
**Purpose**: Retrieve authenticated user's todo items

**Request**:
- Method: GET
- Endpoint: `/api/todos`
- Headers: `Authorization: Bearer {token}`

**Response**:
- Success (200):
  ```json
  [
    {
      "id": "string (todo ID)",
      "title": "string (todo title)",
      "completed": "boolean (completion status)",
      "user_id": "string (owner user ID)",
      "created_at": "string (ISO date)",
      "updated_at": "string (ISO date)"
    }
  ]
  ```
- Error (401):
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

### POST /api/todos
**Purpose**: Create a new todo item for authenticated user

**Request**:
- Method: POST
- Endpoint: `/api/todos`
- Headers: `Authorization: Bearer {token}`, `Content-Type: application/json`
- Body:
  ```json
  {
    "title": "string (required, todo text)",
    "completed": "boolean (optional, default: false)"
  }
  ```

**Response**:
- Success (201):
  ```json
  {
    "id": "string (todo ID)",
    "title": "string (todo title)",
    "completed": "boolean (completion status)",
    "user_id": "string (owner user ID)",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)"
  }
  ```
- Error (400, 401):
  ```json
  {
    "detail": "string (error message)"
  }
  ```

### PUT /api/todos/{id}
**Purpose**: Update an existing todo item

**Request**:
- Method: PUT
- Endpoint: `/api/todos/{id}`
- Headers: `Authorization: Bearer {token}`, `Content-Type: application/json`
- Body:
  ```json
  {
    "title": "string (optional, todo text)",
    "completed": "boolean (optional, completion status)"
  }
  ```

**Response**:
- Success (200):
  ```json
  {
    "id": "string (todo ID)",
    "title": "string (todo title)",
    "completed": "boolean (completion status)",
    "user_id": "string (owner user ID)",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)"
  }
  ```
- Error (401, 403, 404):
  ```json
  {
    "detail": "string (error message)"
  }
  ```

### PATCH /api/todos/{id}/toggle
**Purpose**: Toggle completion status of a todo item

**Request**:
- Method: PATCH
- Endpoint: `/api/todos/{id}/toggle`
- Headers: `Authorization: Bearer {token}`

**Response**:
- Success (200):
  ```json
  {
    "id": "string (todo ID)",
    "title": "string (todo title)",
    "completed": "boolean (updated completion status)",
    "user_id": "string (owner user ID)",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)"
  }
  ```
- Error (401, 403, 404):
  ```json
  {
    "detail": "string (error message)"
  }
  ```

### DELETE /api/todos/{id}
**Purpose**: Delete a todo item

**Request**:
- Method: DELETE
- Endpoint: `/api/todos/{id}`
- Headers: `Authorization: Bearer {token}`

**Response**:
- Success (200):
  ```json
  {
    "message": "Todo deleted successfully"
  }
  ```
- Error (401, 403, 404):
  ```json
  {
    "detail": "string (error message)"
  }
  ```

## Frontend Integration Requirements

### Authentication Flow
- Frontend must redirect to login page after successful signup
- Frontend must redirect to todo dashboard after successful login
- Frontend must store JWT token securely and include it in API requests
- Frontend must redirect to login page if JWT token expires or is invalid

### Todo Dashboard Requirements
- Frontend must fetch todos from `/api/todos` endpoint when authenticated
- Frontend must use `/api/todos` endpoints for all CRUD operations
- Frontend must ensure typed todo text displays in black color
- Frontend must handle loading, success, and error states appropriately