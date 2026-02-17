# Feature Tasks: Authentication-first Todo App with Neon PostgreSQL

## Feature Overview

This document contains the implementation tasks for building an authentication-first Todo application with a protected frontend, REST backend, and Neon PostgreSQL database integration. The application follows Next.js 16+ with App Router for the frontend, FastAPI for the backend, and Neon PostgreSQL for the database layer.

## Implementation Strategy

The approach will follow a phased implementation starting with project setup and environment configuration, followed by database schema design, backend API development, frontend UI implementation, and finally integration and testing. Each phase builds upon the previous one to ensure a stable foundation before adding functionality.

## Dependencies

- User Story 1 (Registration) must be completed before User Story 2 (Authentication) can be fully tested
- User Story 2 (Authentication) must be completed before User Story 3 (Todo Management) can be implemented
- Backend APIs must be developed before frontend integration

## Parallel Execution Opportunities

- Frontend authentication pages can be developed in parallel with backend APIs [P]
- Database models and services can be developed in parallel [P]
- UI components can be developed in parallel once API contracts are established [P]

---

## Phase 1: Setup

- [X] T001 Initialize frontend project using Next.js 16+ App Router
- [X] T002 Configure Tailwind CSS and global styles
- [X] T003 Prepare backend project structure with FastAPI
- [X] T004 Set up environment variables (.env) for database and JWT secrets
- [X] T005 Establish Neon PostgreSQL connection and verify connectivity

## Phase 2: Foundational Tasks

- [X] T010 Design users table with id, name, email, hashed_password, timestamps
- [X] T011 Design todos table with id, title, completed status, user_id, timestamps
- [X] T012 Define foreign key relationship between users and todos
- [X] T013 Implement password hashing utility for secure storage
- [X] T014 Create JWT token generation and validation utilities

## Phase 3: [US1] First-Time User Registration

**Goal**: Enable first-time visitors to create an account and register securely.

**Independent Test**: Can be fully tested by navigating to the application and registering with valid credentials. The system should create a new user account and redirect to the login page.

- [X] T020 [P] [US1] Create User model in backend/src/models/user.py
- [X] T021 [P] [US1] Create UserService in backend/src/services/user_service.py
- [X] T022 [P] [US1] Implement user signup API endpoint in backend/src/api/auth.py
- [X] T023 [P] [US1] Build signup page UI in frontend/app/signup/page.tsx
- [X] T024 [US1] Implement signup form validation in frontend
- [X] T025 [US1] Test user registration flow with valid credentials
- [X] T026 [US1] Test user registration flow with invalid credentials

## Phase 4: [US2] Secure User Authentication

**Goal**: Allow registered users to securely log in to the Todo app and access their personal tasks.

**Independent Test**: Can be fully tested by attempting to log in with valid credentials and being redirected to the protected todo dashboard. Also test with invalid credentials to ensure proper error handling.

- [X] T030 [P] [US2] Implement login API endpoint with JWT token issuance
- [X] T031 [P] [US2] Implement JWT validation middleware for protected routes
- [X] T032 [P] [US2] Build login page UI in frontend/app/login/page.tsx
- [X] T033 [US2] Implement JWT token storage and retrieval in frontend
- [X] T034 [US2] Create protected route wrapper for authenticated access
- [X] T035 [US2] Test successful login and redirection to todo dashboard
- [X] T036 [US2] Test authentication failure with invalid credentials

## Phase 5: [US3] Protected Todo Management

**Goal**: Allow authenticated users to create, read, update, and delete their personal todo items.

**Independent Test**: Can be fully tested by logging in and performing all CRUD operations on todo items. All changes should persist in the Neon PostgreSQL database and be visible only to the authenticated user.

- [X] T040 [P] [US3] Create Todo model in backend/src/models/todo.py
- [X] T041 [P] [US3] Create TodoService in backend/src/services/todo_service.py
- [X] T042 [P] [US3] Implement GET /api/todos endpoint for user-specific todos
- [X] T043 [P] [US3] Implement POST /api/todos endpoint to add new todo
- [X] T044 [P] [US3] Implement PUT /api/todos/{id} endpoint to update todo
- [X] T045 [P] [US3] Implement PATCH /api/todos/{id}/toggle endpoint to toggle completion
- [X] T046 [P] [US3] Implement DELETE /api/todos/{id} endpoint to delete todo
- [X] T047 [P] [US3] Build Todo dashboard UI in frontend/app/todos/page.tsx
- [X] T048 [US3] Implement todo list display with proper user scoping
- [X] T049 [US3] Implement add todo functionality with backend sync
- [X] T050 [US3] Implement update todo functionality with backend sync
- [X] T051 [US3] Implement delete todo functionality with backend sync
- [X] T052 [US3] Implement toggle completion functionality with backend sync
- [X] T053 [US3] Ensure typed todo text color is black as required
- [X] T054 [US3] Test multi-user data isolation

## Phase 6: Frontend-Backend Integration

- [X] T060 Connect frontend API calls with backend endpoints
- [X] T061 Attach JWT token to protected requests
- [X] T062 Handle loading, success, and error states in UI
- [X] T063 Implement optimistic UI updates with backend confirmation
- [X] T064 Test end-to-end authentication and todo management flow

## Phase 7: UI Polish & UX Improvements

- [X] T070 Ensure consistent UI between login, signup, and dashboard
- [X] T071 Improve spacing, typography, and responsiveness
- [X] T072 Add empty states and error messages
- [X] T073 Verify accessibility basics
- [X] T074 Create initial auth entry page with Login/Signup CTA

## Phase 8: Testing & Validation

- [X] T080 Test signup, login, logout flows
- [X] T081 Verify protected routes behavior
- [X] T082 Test todo add/update/delete persistence in Neon
- [X] T083 Handle JWT token expiration scenarios
- [X] T084 Test database availability edge cases
- [X] T085 Validate email uniqueness and format constraints