# Data Model: Authentication-first Todo App

## Database Schema

### Users Table
- **id** (UUID/String): Primary key, unique identifier for each user
- **name** (String): User's full name or display name
- **email** (String): User's email address, must be unique
- **hashed_password** (String): Securely hashed password using industry-standard algorithm
- **created_at** (DateTime): Timestamp when user account was created
- **updated_at** (DateTime): Timestamp when user account was last updated
- **last_login_at** (DateTime, nullable): Timestamp of last successful login
- **is_active** (Boolean): Flag indicating if the account is active

**Constraints**:
- Email must be unique across all users
- Email must be valid email format
- Name and email are required fields
- Password must be securely hashed before storage

### Todos Table
- **id** (UUID/String): Primary key, unique identifier for each todo item
- **title** (String): The text content of the todo item
- **completed** (Boolean): Flag indicating if the todo is completed or pending
- **user_id** (UUID/String): Foreign key linking to the user who owns this todo
- **created_at** (DateTime): Timestamp when todo was created
- **updated_at** (DateTime): Timestamp when todo was last updated

**Constraints**:
- user_id must reference a valid user in the users table
- Title is a required field
- Each todo belongs to exactly one user
- Only the owning user can modify their todos

## Relationships

### User to Todos (One-to-Many)
- One user can have many todos
- Foreign key constraint: todos.user_id references users.id
- Cascade delete: If a user is deleted, their todos should also be deleted
- This ensures data isolation where users can only access their own todos

## Authentication Token Structure

### JWT Payload
- **sub** (Subject): User's unique identifier
- **email** (String): User's email address
- **name** (String): User's display name
- **iat** (Issued At): Token creation timestamp
- **exp** (Expiration): Token expiration timestamp

## API Request/Response Objects

### User Registration Request
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

### User Registration Response
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "created_at": "datetime"
}
```

### User Login Request
```json
{
  "email": "string",
  "password": "string"
}
```

### User Login Response
```json
{
  "access_token": "string",
  "token_type": "string",
  "user": {
    "id": "string",
    "name": "string",
    "email": "string"
  }
}
```

### Todo Creation Request
```json
{
  "title": "string",
  "completed": "boolean"
}
```

### Todo Response
```json
{
  "id": "string",
  "title": "string",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```