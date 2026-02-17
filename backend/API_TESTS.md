# Task API Testing Guide

This document provides examples for testing the Task CRUD APIs using both Postman and cURL.

## Prerequisites

Before testing the APIs, you need to:
1. Have a valid JWT token from the authentication system
2. Know your user ID (extracted from the JWT token)

## API Endpoints

### 1. Create Task
- **Endpoint**: `POST /api/{user_id}/tasks/`
- **Description**: Creates a new task for the authenticated user
- **Headers**: 
  - `Authorization: Bearer <your-jwt-token>`
  - `Content-Type: application/json`

#### Postman Example:
- Method: `POST`
- URL: `http://localhost:8000/api/<your-user-id>/tasks/`
- Headers:
  - Key: `Authorization`, Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
  - Key: `Content-Type`, Value: `application/json`
- Body (raw JSON):
```json
{
  "title": "Sample Task",
  "description": "This is a sample task description",
  "completed": false
}
```

#### cURL Example:
```bash
curl -X POST "http://localhost:8000/api/<your-user-id>/tasks/" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Task",
    "description": "This is a sample task description",
    "completed": false
  }'
```

### 2. Get All Tasks
- **Endpoint**: `GET /api/{user_id}/tasks/`
- **Description**: Retrieves all tasks for the authenticated user
- **Headers**: 
  - `Authorization: Bearer <your-jwt-token>`

#### Postman Example:
- Method: `GET`
- URL: `http://localhost:8000/api/<your-user-id>/tasks/`
- Headers:
  - Key: `Authorization`, Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### cURL Example:
```bash
curl -X GET "http://localhost:8000/api/<your-user-id>/tasks/" \
  -H "Authorization: Bearer <your-jwt-token>"
```

### 3. Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{task_id}`
- **Description**: Retrieves a specific task by ID
- **Headers**: 
  - `Authorization: Bearer <your-jwt-token>`

#### Postman Example:
- Method: `GET`
- URL: `http://localhost:8000/api/<your-user-id>/tasks/<task-id>`
- Headers:
  - Key: `Authorization`, Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### cURL Example:
```bash
curl -X GET "http://localhost:8000/api/<your-user-id>/tasks/<task-id>" \
  -H "Authorization: Bearer <your-jwt-token>"
```

### 4. Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`
- **Description**: Updates a specific task by ID
- **Headers**: 
  - `Authorization: Bearer <your-jwt-token>`
  - `Content-Type: application/json`

#### Postman Example:
- Method: `PUT`
- URL: `http://localhost:8000/api/<your-user-id>/tasks/<task-id>`
- Headers:
  - Key: `Authorization`, Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
  - Key: `Content-Type`, Value: `application/json`
- Body (raw JSON):
```json
{
  "title": "Updated Task Title",
  "description": "Updated task description",
  "completed": true
}
```

#### cURL Example:
```bash
curl -X PUT "http://localhost:8000/api/<your-user-id>/tasks/<task-id>" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task Title",
    "description": "Updated task description",
    "completed": true
  }'
```

### 5. Update Task Completion Status
- **Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`
- **Description**: Updates the completion status of a specific task
- **Headers**: 
  - `Authorization: Bearer <your-jwt-token>`
  - `Content-Type: application/json`

#### Postman Example:
- Method: `PATCH`
- URL: `http://localhost:8000/api/<your-user-id>/tasks/<task-id>/complete`
- Headers:
  - Key: `Authorization`, Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
  - Key: `Content-Type`, Value: `application/json`
- Body (raw JSON):
```json
{
  "completed": true
}
```

#### cURL Example:
```bash
curl -X PATCH "http://localhost:8000/api/<your-user-id>/tasks/<task-id>/complete" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### 6. Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`
- **Description**: Deletes a specific task by ID
- **Headers**: 
  - `Authorization: Bearer <your-jwt-token>`

#### Postman Example:
- Method: `DELETE`
- URL: `http://localhost:8000/api/<your-user-id>/tasks/<task-id>`
- Headers:
  - Key: `Authorization`, Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### cURL Example:
```bash
curl -X DELETE "http://localhost:8000/api/<your-user-id>/tasks/<task-id>" \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Common Response Codes

- `200 OK`: Request successful
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Notes

- The `{user_id}` in the URL must match the authenticated user's ID from the JWT token
- Users can only access their own tasks (enforced by the backend)
- All endpoints require a valid JWT token in the Authorization header