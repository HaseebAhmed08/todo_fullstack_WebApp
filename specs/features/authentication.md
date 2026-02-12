# Feature: Authentication
 
## Objective
Implement user signup and signin using Better Auth with JWT tokens for API security.

## The Challenge
Better Auth is a JavaScript/TypeScript authentication library that runs on your Next.js frontend. However, your FastAPI backend is a separate Python service that needs to verify which user is making API requests.

## The Solution: JWT Tokens
Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.

## How It Works
1. **User logs in on Frontend** → Better Auth creates a session and issues a JWT token.
2. **Frontend makes API call** → Includes the JWT token in the `Authorization: Bearer <token>` header.
3. **Backend receives request** → Extracts token from header, verifies signature using shared secret.
4. **Backend identifies user** → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL.
5. **Backend filters data** → Returns only tasks belonging to that user.

## Component Changes Required
- **Better Auth Config**: Enable JWT plugin to issue tokens.
- **Frontend API Client**: Attach JWT token to every API request header.
- **FastAPI Backend**: Add middleware to verify JWT and extract user.
- **API Routes**: Filter all queries by the authenticated user's ID.

## Security Benefits
- **User Isolation**: Each user only sees their own tasks.
- **Stateless Auth**: Backend doesn't need to call frontend to verify users.
- **Token Expiry**: JWTs expire automatically.
- **No Shared DB Session**: Frontend and backend can verify auth independently.
