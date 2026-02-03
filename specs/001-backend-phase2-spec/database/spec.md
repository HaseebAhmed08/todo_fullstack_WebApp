# Database Specifications for Phase II Todo App Backend

## Purpose
Define data entities required to support frontend features, relationships between entities, data constraints, and audit expectations for the Neon Serverless PostgreSQL database.

## Scope
This specification outlines the data model for the backend, including entities, relationships, constraints, and data management rules that support the todo application functionality.

## Data Entities

### User Entity
Represents an authenticated user account in the system.

**Attributes:**
- `id`: String (Primary Key, UUID) - Unique identifier for the user
- `email`: String (Unique, Indexed) - User's email address for authentication
- `passwordHash`: String - Securely hashed password (using bcrypt/scrypt)
- `name`: String - User's display name
- `createdAt`: DateTime - Timestamp when user account was created
- `updatedAt`: DateTime - Timestamp when user record was last updated
- `lastLoginAt`: DateTime (Optional) - Timestamp of last successful login
- `isActive`: Boolean (Default: true) - Whether the account is active

**Constraints:**
- Email must be unique across all users
- Email must follow standard email format validation
- Password must meet security requirements (length, complexity)
- Name must be between 1-100 characters

### Todo Entity
Represents a task item owned by a specific user.

**Attributes:**
- `id`: String (Primary Key, UUID) - Unique identifier for the todo
- `userId`: String (Foreign Key) - Reference to the owning user
- `title`: String - Title of the todo item (required)
- `description`: Text (Optional) - Detailed description of the task
- `completed`: Boolean (Default: false) - Completion status
- `createdAt`: DateTime - Timestamp when todo was created
- `updatedAt`: DateTime - Timestamp when todo was last modified
- `dueDate`: DateTime (Optional) - Deadline for the task
- `priority`: String (Enum: 'low', 'medium', 'high', Default: 'medium') - Priority level
- `tags`: JSON (Optional) - Array of tags for categorization

**Constraints:**
- Title must not be empty (1-200 characters)
- Description length limit: 2000 characters
- Each todo must belong to exactly one user
- Completed status can only be true/false
- Due date must be a valid future date (if provided)

## Relationships Between Entities

### User-Todo Relationship (One-to-Many)
- One User can own many Todos
- Foreign Key: Todo.userId references User.id
- Cascade delete: When a User is deleted, all their Todos are also deleted
- Index: Todo.userId is indexed for efficient lookup

### Referential Integrity
- All foreign key relationships enforce referential integrity
- Attempts to create a Todo with non-existent userId will fail
- Database-level constraints prevent orphaned records

## Data Constraints and Invariants

### Data Integrity Rules
- **Ownership Enforcement**: A Todo can only be accessed/modified by its owner (User)
- **Email Uniqueness**: No two users can have the same email address
- **Required Fields**: Critical fields (email, title) cannot be null
- **Data Validation**: All string fields have appropriate length limits
- **Timestamp Consistency**: updatedAt must always be >= createdAt

### Business Rules
- **Soft Deletes**: User accounts cannot be hard deleted; they can only be deactivated
- **Todo Ownership**: Users cannot modify or access todos belonging to other users
- **Data Privacy**: Personal information is stored securely and only accessible to the owner
- **Audit Trail**: Creation and modification timestamps are automatically managed

## Soft Delete vs Hard Delete Rules

### Soft Delete Policy
- **User Accounts**: Never hard deleted; instead, set `isActive: false`
- **Reason**: Maintain data integrity for historical records and potential account recovery
- **Retention**: Deactivated accounts remain in the database indefinitely but are excluded from active queries

### Hard Delete Policy
- **Todos**: May be hard deleted upon user request
- **Reason**: Individual task items can be permanently removed at user discretion
- **Cascading**: When a user is soft-deleted, their todos may be hard deleted depending on retention policy

## Audit and Timestamp Expectations

### Automatic Timestamp Management
- **createdAt**: Automatically set on record creation, never modified thereafter
- **updatedAt**: Automatically updated whenever any field in the record changes
- **Consistency**: Both timestamps use UTC timezone for uniformity across all services

### Audit Trail Requirements
- **Change Tracking**: All modifications to Todo items are logged with timestamps
- **Access Logging**: Authentication events (login, logout) are recorded for security
- **Data Modification**: Changes to user profiles are tracked for compliance purposes
- **Retention Period**: Audit logs maintained for minimum 90 days, maximum 2 years

### Query Performance Considerations
- **Indexing Strategy**: Frequently queried fields (userId, completed status) are indexed
- **Partitioning**: Large tables may be partitioned by date ranges for performance
- **Archiving**: Historical data beyond certain thresholds may be archived to separate tables

## Data Migration Considerations
- **Schema Evolution**: Database schema changes follow backward-compatible patterns
- **Rollback Capability**: All schema migrations include corresponding rollback procedures
- **Data Validation**: Migration scripts validate data integrity before and after changes
- **Zero Downtime**: Schema changes designed to minimize service disruption