# Data Model: Task CRUD Issues Fix

## Entities

### Task
- **Fields**:
  - id: Unique identifier (UUID/Integer)
  - title: String (required, max 255 characters)
  - description: Text (optional, unlimited length)
  - completed: Boolean (default: false)
  - user_id: Foreign key to User entity
  - created_at: DateTime (auto-generated)
  - updated_at: DateTime (auto-generated)

- **Validation rules**:
  - Title must not be empty
  - Task must be associated with a valid user
  - User can only access their own tasks

- **State transitions**:
  - Active (default) ↔ Completed (toggle operation)

### User
- **Fields**:
  - id: Unique identifier (UUID/Integer)
  - email: String (unique, required)
  - password_hash: String (encrypted)
  - created_at: DateTime (auto-generated)
  - updated_at: DateTime (auto-generated)

- **Validation rules**:
  - Email must be valid format
  - Password must meet security requirements
  - Email must be unique

### Authentication Session
- **Fields**:
  - user_id: Foreign key to User entity
  - jwt_token: String (encrypted/session data)
  - expires_at: DateTime
  - created_at: DateTime (auto-generated)

- **Validation rules**:
  - Token must be valid JWT format
  - Session must not be expired
  - User must exist and be active

## Relationships
- User (1) : Task (Many) - A user can have many tasks
- User (1) : Authentication Session (1) - A user has one active session

## Constraints
- Referential integrity: Tasks must have valid user associations
- Data consistency: All timestamp fields are UTC
- Access control: Users can only modify their own data