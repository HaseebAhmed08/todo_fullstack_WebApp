# Data Model: Authentication and Persistence Fixes

## Overview
Data model for the authentication and persistence fixes in the Todo Full-Stack Web Application. Defines the entity structures, relationships, and validation rules required to implement secure user authentication and persistent task storage.

## Entities

### User
Represents a registered user account in the system.

**Attributes:**
- `id` (UUID/string): Unique identifier from Better Auth JWT
- `email` (string): User's email address (authentication credential)
- `name` (string): User's display name
- `created_at` (datetime): Timestamp of first backend access
- `updated_at` (datetime): Timestamp of last update

**Validation Rules:**
- Email must be valid email format
- Email must be unique across all users
- Name must be non-empty string
- ID must match the format used by Better Auth

**Relationships:**
- One-to-many with Task (user has many tasks)

### Task
Represents a user-owned task in the system.

**Attributes:**
- `id` (UUID): Unique identifier for the task
- `title` (string): Task name/title
- `description` (string, optional): Detailed information about the task
- `completed` (boolean): Status flag indicating if task is completed
- `created_at` (datetime): Timestamp when task was created
- `updated_at` (datetime): Timestamp of last update
- `user_id` (UUID/string): Foreign key linking to the owning user

**Validation Rules:**
- Title must be non-empty string
- User_id must reference an existing user
- Completed flag defaults to false
- Description length limited to 1000 characters

**Relationships:**
- Many-to-one with User (task belongs to one user)

## State Transitions

### Task State Transitions
- **Active** → **Completed**: When user marks task as complete
- **Completed** → **Active**: When user unmarks task as complete

## Database Schema

### Users Table
```
users (
  id: UUID/STRING PRIMARY KEY,
  email: VARCHAR(255) UNIQUE NOT NULL,
  name: VARCHAR(255) NOT NULL,
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tasks Table
```
tasks (
  id: UUID PRIMARY KEY,
  title: VARCHAR(255) NOT NULL,
  description: TEXT,
  completed: BOOLEAN DEFAULT FALSE,
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id: UUID/STRING REFERENCES users(id) ON DELETE CASCADE
)
```

## Indexes
- Index on `users.email` for efficient login lookups
- Index on `tasks.user_id` for efficient user task filtering
- Index on `tasks.completed` for filtering completed tasks

## Security Considerations
- All task queries must be filtered by user_id to prevent cross-user data access
- User_id should be extracted from JWT token, never from request body
- Foreign key constraint ensures data integrity (tasks deleted when user is deleted)