# API Contracts: Authentication Endpoints

## Overview
This document defines the API contracts for authentication endpoints that the frontend authentication components interact with. These contracts ensure proper integration between the frontend forms and backend services.

## Authentication Endpoints

### POST /api/auth/register
**Purpose**: Register a new user account

**Request**:
- Method: POST
- Endpoint: `/api/auth/register`
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "email": "string (required)",
    "password": "string (required, min 8 characters)",
    "name": "string (required)"
  }
  ```

**Response**:
- Success (200):
  ```json
  {
    "id": "string (user ID)",
    "email": "string (user email)",
    "name": "string (user name)",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)",
    "last_login_at": "string (ISO date, nullable)",
    "is_active": "boolean"
  }
  ```
- Error (400, 409, 500):
  ```json
  {
    "error": {
      "code": "string",
      "message": "string"
    }
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
    "email": "string (required)",
    "password": "string (required)"
  }
  ```

**Response**:
- Success (200):
  ```json
  {
    "token": "string (JWT token)",
    "user": {
      "id": "string (user ID)",
      "email": "string (user email)",
      "name": "string (user name)"
    }
  }
  ```
- Error (401, 500):
  ```json
  {
    "error": {
      "code": "string",
      "message": "string"
    }
  }
  ```

### POST /api/auth/logout
**Purpose**: End user session

**Request**:
- Method: POST
- Endpoint: `/api/auth/logout`
- Headers: `Authorization: Bearer <token>`
- Body: Empty

**Response**:
- Success (200):
  ```json
  {
    "success": true
  }
  ```
- Error (401, 500):
  ```json
  {
    "error": {
      "code": "string",
      "message": "string"
    }
  }
  ```

## Frontend Integration Requirements

### SignupFormComponent
- Must send properly formatted registration data to `/api/auth/register`
- Must handle success response by storing JWT token appropriately
- Must handle various error responses with appropriate user feedback
- Should validate form data before submission

### SigninFormComponent
- Must send properly formatted login credentials to `/api/auth/login`
- Must handle success response by storing JWT token and user data
- Must handle various error responses with appropriate user feedback
- Should validate form data before submission

### Error Handling
- Both components should handle network errors gracefully
- Should provide user-friendly error messages
- Should maintain form state during submission
- Should properly clear sensitive data after logout

## Security Considerations
- JWT tokens must be stored securely (preferably in httpOnly cookies or secure local storage)
- Passwords must not be stored or logged
- Authentication credentials must be sent over HTTPS
- Session management must follow security best practices