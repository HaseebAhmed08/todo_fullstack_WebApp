# Data Model for Frontend Implementation

## User Entity
- **id**: string (unique identifier)
- **email**: string (user's email address, unique)
- **name**: string (user's display name)
- **createdAt**: Date (timestamp when user was created)
- **updatedAt**: Date (timestamp when user was last updated)

## Task Entity
- **id**: string (unique identifier)
- **title**: string (task title, required)
- **description**: string (optional task description)
- **completed**: boolean (whether the task is completed)
- **userId**: string (foreign key linking to user who owns the task)
- **createdAt**: Date (timestamp when task was created)
- **updatedAt**: Date (timestamp when task was last updated)

## Validation Rules
From the functional requirements:
- User email must be valid email format
- Task title must not be empty
- User must be authenticated to create/view tasks
- Only task owner can modify/delete their tasks

## State Transitions
- Task entity: pending → completed (via toggle)
- User session: unauthenticated → authenticated (via login)
- User session: authenticated → unauthenticated (via logout)