# Authentication Specifications for Phase II Todo App Backend

## Purpose
Define JWT lifecycle and validation rules, integration expectations with Better Auth, and protected route management for the todo application backend.

## Scope
This specification outlines the authentication and authorization mechanisms that protect backend resources, ensure user identity verification, and manage secure session lifecycles using Better Auth with JWT tokens.

## JWT Lifecycle and Validation Rules

### JWT Token Structure
The backend expects JWT tokens following the standard format with the following claims:

**Required Claims:**
- `sub` (Subject): User's unique identifier (UUID)
- `iat` (Issued At): Unix timestamp when token was issued
- `exp` (Expiration): Unix timestamp when token expires
- `jti` (JWT ID): Unique identifier for the token (for potential revocation)

**Additional Claims:**
- `email`: User's email address
- `name`: User's display name
- `role`: User role (currently always "user")

### JWT Generation
- Tokens are generated upon successful authentication (login/register)
- Expiration time: 24 hours from issuance (configurable)
- Algorithm: HS256 with secure secret from BETTER_AUTH_SECRET
- Token includes user identity claims for authorization decisions

### JWT Validation Rules
- **Signature Verification**: All tokens must have valid signature using BETTER_AUTH_SECRET
- **Expiration Check**: Expired tokens (exp < current time) are rejected with 401
- **Subject Validation**: Token subject must correspond to a valid user in the database
- **Malformed Token**: Malformed or invalid JWTs return 401 status
- **Revocation Check**: (Future enhancement) Check token against blacklist if applicable

### Token Refresh Behavior (Conceptual)
- When a token expires, frontend should redirect to login or use refresh mechanism
- Long-lived sessions may implement refresh token pattern
- Refresh tokens have extended lifetime but limited reuse window

## Integration Expectations with Better Auth

### Configuration Requirements
- **BETTER_AUTH_URL**: Points to authentication service (http://localhost:3002)
- **BETTER_AUTH_SECRET**: Secret key for JWT signing/validation
- **API Compatibility**: Backend endpoints must accept Better Auth generated JWTs
- **User Sync**: User information should be consistent between Better Auth and backend

### Authentication Flow Integration
1. **Frontend Login**: User submits credentials to Better Auth
2. **Token Generation**: Better Auth generates JWT and returns to frontend
3. **Backend Validation**: Backend receives JWT and validates using Better Auth secret
4. **User Context**: Backend extracts user identity from token claims

### User Data Synchronization
- User ID from Better Auth should match user ID in backend database
- Profile updates in Better Auth may need synchronization with backend user records
- Email consistency maintained between Better Auth and backend systems

## Protected vs Public Routes

### Public Routes (No Authentication Required)
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration
- `GET /api/health` - Health check endpoint
- `GET /api/status` - System status information

### Protected Routes (JWT Required)
- All `GET /api/todos/*` endpoints - Todo retrieval operations
- All `POST /api/todos/*` endpoints - Todo creation operations
- All `PUT /api/todos/*` endpoints - Todo update operations
- All `PATCH /api/todos/*` endpoints - Todo modification operations
- All `DELETE /api/todos/*` endpoints - Todo deletion operations
- `POST /api/auth/logout` - Session termination

### Authentication Middleware Behavior
- Extracts `Authorization: Bearer <token>` header from requests
- Validates JWT signature and expiration
- Attaches user context to request for downstream handlers
- Returns 401 for invalid/missing tokens
- Logs authentication failures for security monitoring

## Authorization Implementation

### Resource-Level Authorization
- Users can only access their own todo items
- Backend verifies `userId` in todo record matches authenticated user's ID
- Unauthorized access attempts return 403 Forbidden status
- Admin functionality (future) would require role-based checks

### Permission Checks
- **Owner Check**: Verify requesting user ID matches resource owner ID
- **Method Permissions**: Different permissions for read vs write operations
- **Bulk Operation Validation**: Verify user owns all resources in bulk requests

### Role-Based Access (Future Enhancement)
- Current implementation assumes single "user" role
- Future admin roles would require additional authorization checks
- Role information stored in JWT claims for efficient validation

## Security Considerations

### Token Security
- JWTs transmitted over HTTPS only (enforced by frontend)
- Short expiration times to limit exposure window
- Secure storage recommendations for frontend (HttpOnly cookies or secure localStorage)
- Protection against CSRF and XSS attacks

### Rate Limiting
- Authentication endpoints should implement rate limiting
- Limit failed login attempts to prevent brute force
- Consider account lockout after multiple failed attempts

### Audit Trail
- Log authentication events (successful and failed)
- Track token generation and validation activities
- Monitor for suspicious authentication patterns
- Maintain logs for compliance and security analysis

## Error Handling for Authentication

### Authentication-Specific Error Responses
- **401 Unauthorized**: Invalid, expired, or missing JWT
- **403 Forbidden**: Valid JWT but insufficient permissions for resource
- **429 Too Many Requests**: Rate limit exceeded on auth endpoints
- **500 Internal Error**: Authentication system failure

### Error Response Format
```
{
  "error": {
    "code": "AUTHENTICATION_FAILED" | "TOKEN_EXPIRED" | "INSUFFICIENT_PERMISSIONS",
    "message": "Descriptive error message",
    "timestamp": "ISO date string"
  }
}
```

## Token Lifecycle Management

### Token Issuance
- Upon successful login/registration
- Contains necessary user identity information
- Expires after configured duration
- Should be treated as sensitive information

### Token Renewal
- Frontend responsible for managing token lifecycle
- Automatic renewal before expiration (if refresh mechanism available)
- Graceful handling of token expiration events

### Token Revocation (Conceptual)
- Logout should invalidate current session
- Potential for token blacklisting (advanced feature)
- Session termination should be immediate and complete