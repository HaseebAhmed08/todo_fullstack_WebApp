---
description: "Task list for fixing authentication, user persistence, and task persistence issues"
---

# Tasks: Fix Authentication, User Persistence, and Task Persistence

**Input**: Design documents from `/specs/001-auth-data-persistence/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow the project structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Set up environment variables with Neon connection string in backend/.env
- [x] T002 [P] Install backend dependencies: FastAPI, SQLModel, psycopg2-binary, python-jose[cryptography], passlib[bcrypt], better-auth
- [x] T003 [P] Install frontend dependencies: Next.js, React, Tailwind CSS, better-auth

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Set up database connection with SQLModel in backend/src/database/database.py
- [x] T005 [P] Create User model in backend/src/models/user.py
- [x] T006 [P] Create Task model in backend/src/models/task.py
- [x] T007 [P] Set up JWT authentication middleware in backend/src/services/auth.py
- [x] T008 Implement JWT verification using Better Auth public keys in backend/src/services/auth.py
- [x] T009 Create user service for automatic user creation in backend/src/services/user_service.py
- [x] T010 Set up database initialization and migration framework

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Reliable User Authentication (Priority: P1) 🎯 MVP

**Goal**: Implement reliable signup and login functionality that works consistently every time

**Independent Test**: Complete signup and login operations across different sessions and verify consistent success

### Implementation for User Story 1

- [x] T011 [P] [US1] Implement signup endpoint with JWT token verification in backend/src/api/auth.py
- [x] T012 [US1] Implement login endpoint with JWT token verification in backend/src/api/auth.py
- [x] T013 [US1] Update frontend signup page to handle authentication responses in frontend/src/pages/auth/signup.tsx
- [x] T014 [US1] Update frontend login page to handle authentication responses in frontend/app/signin/page.tsx
- [ ] T015 [US1] Test signup and login functionality to verify consistent success

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Backend User Persistence (Priority: P1)

**Goal**: Ensure authenticated users are automatically persisted in the backend database if they don't already exist

**Independent Test**: Create new user account and verify that user data is automatically created and persisted in the backend database

### Implementation for User Story 2

- [x] T016 [P] [US2] Implement automatic user creation service in backend/src/services/user_service.py
- [x] T017 [US2] Add user existence check before creating records in backend/src/services/user_service.py
- [x] T018 [US2] Update auth middleware to trigger user creation if needed in backend/src/services/auth.py
- [x] T019 [US2] Create database error handling for user creation in backend/src/services/user_service.py
- [ ] T020 [US2] Test user synchronization between Better Auth and backend database

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Consistent JWT Token Verification (Priority: P1)

**Goal**: Ensure every API request to the FastAPI backend properly verifies JWT tokens issued by Better Auth

**Independent Test**: Make various API requests with and without valid JWT tokens and verify that access is properly granted or denied

### Implementation for User Story 3

- [x] T021 [P] [US3] Implement JWT validation middleware in backend/src/services/auth.py
- [x] T022 [US3] Create helper function to extract user ID from JWT in backend/src/services/auth.py
- [x] T023 [US3] Add 401 Unauthorized responses for invalid tokens in backend/src/services/auth.py
- [x] T024 [US3] Update all protected endpoints to use JWT verification in backend/src/api/
- [ ] T025 [US3] Test JWT token verification with valid and invalid tokens

**Checkpoint**: All authentication should now be secure and consistent

---

## Phase 6: User Story 4 - Persistent Task Storage with User Isolation (Priority: P1)

**Goal**: Enable users to create, update, delete, and complete tasks that persist in Neon PostgreSQL and are properly associated with their authenticated user identity

**Independent Test**: Perform all task operations while authenticated and verify that changes persist in the database and are accessible only to the owning user

### Implementation for User Story 4

- [x] T026 [P] [US4] Create task CRUD endpoints in backend/src/api/tasks.py
- [x] T027 [US4] Implement task service with user association in backend/src/services/task_service.py
- [x] T028 [US4] Add JWT verification to task endpoints to ensure user isolation in backend/src/api/tasks.py
- [x] T029 [US4] Ensure task operations link to correct user_id via JWT token in backend/src/services/task_service.py
- [x] T030 [US4] Add database error logging for task operations in backend/src/services/task_service.py
- [x] T031 [US4] Test task creation to verify association with authenticated user
- [x] T032 [US4] Test user isolation to ensure users cannot access other users' tasks
- [x] T033 [US4] Update frontend task page to handle authenticated task operations in frontend/app/tasks/page.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T034 [P] Update database initialization to create tables for User and Task models
- [x] T035 Add comprehensive error logging for all database operations
- [x] T036 [P] Update environment configuration to use provided Neon connection string
- [x] T037 [P] Add validation to ensure user isolation for task access
- [x] T038 Run quickstart validation to verify all functionality works as expected
- [x] T039 Update documentation with new authentication flow and database setup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 with database persistence
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on authentication for token verification
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Builds on authentication and user persistence for task operations

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Implement signup endpoint with JWT token verification in backend/src/api/auth.py"
Task: "Update frontend signup page to handle authentication responses in frontend/src/pages/auth/signup.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence