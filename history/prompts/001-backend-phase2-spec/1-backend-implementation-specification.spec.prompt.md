---
id: 1
title: backend-implementation-specification
stage: spec
date: 2026-01-28
surface: agent
model: gemini-2.5-flash
feature: backend-phase2-spec
branch: 001-backend-phase2-spec
user: Claude Code
command: /sp.specify
labels: ["spec", "backend", "todo-app", "api", "database", "auth"]
links:
  spec: ../specs/001-backend-phase2-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-backend-phase2-spec/spec.md
 - specs/001-backend-phase2-spec/api/spec.md
 - specs/001-backend-phase2-spec/database/spec.md
 - specs/001-backend-phase2-spec/feature/spec.md
 - specs/001-backend-phase2-spec/auth/spec.md
 - specs/001-backend-phase2-spec/checklists/requirements.md
tests:
 - null
---

## Prompt

"Backend Implementation Specification — Phase II Todo App" --parameters {
  "name": "backend-phase2-spec",
  "description": "Define complete backend specifications for Phase II Todo Full-Stack Web Application. Backend must fully integrate with an already implemented frontend and follow Spec-Kit Plus conventions strictly. This specification will act as the single source of truth for backend implementation.",
  "context": {
    "project_phase": "Phase II",
    "frontend_status": "Completed and finalized",
    "source_of_truth": [
      "Hackathon requirements document",
      "Existing frontend behavior and API expectations"
    ],
    "stack": {
      "backend": "FastAPI",
      "orm": "SQLModel",
      "database": "Neon Serverless PostgreSQL",
      "authentication": "Better Auth with JWT"
    },
    "environment_contract": {
      "NEXT_PUBLIC_API_URL": "http://localhost:8000",
      "BETTER_AUTH_URL": "http://localhost:3002",
      "BETTER_AUTH_SECRET": "Defined externally",
      "NEON_DB_URL": "Defined externally"
    }
  },
  "instructions": [
    "You are a Spec Writer Agent, not a developer.",
    "Do NOT write any code, SQL, schemas, migrations, or implementation details.",
    "Write specifications ONLY inside /specs/* directories.",
    "Backend specifications must align exactly with the existing frontend API usage and flows.",
    "Assume frontend behavior is correct and must not be changed.",
    "If any frontend-backend mismatch is detected, document it explicitly as an Open Question."
  ],
  "required_outputs": [
    {
      "path": "/specs/api/",
      "content_requirements": [
        "All REST API endpoints required by the frontend",
        "Request and response data contracts (conceptual, not code)",
        "Authentication and authorization rules per endpoint",
        "Error scenarios and failure responses",
        "Pagination, filtering, and sorting expectations where applicable"
      ]
    },
    {
      "path": "/specs/database/",
      "content_requirements": [
        "Data entities required to support frontend features",
        "Relationships between entities",
        "Data constraints and invariants",
        "Soft delete vs hard delete rules",
        "Audit and timestamp expectations"
      ]
    },
    {
      "path": "/specs/feature/",
      "content_requirements": [
        "Backend responsibilities per feature",
        "User stories from backend perspective",
        "Acceptance criteria mapping frontend actions to backend outcomes"
      ]
    },
    {
      "path": "/specs/auth/",
      "content_requirements": [
        "JWT lifecycle and validation rules",
        "Integration expectations with Better Auth",
        "Protected vs public routes",
        "Token expiration and refresh behavior (conceptual only)"
      ]
    }
  ],
  "global_rules": [
    "Every spec must include Purpose, Scope, User Stories, Acceptance Criteria, Constraints.",
    "Never assume implementation details such as libraries, middleware, or folder structure.",
    "Reference related specs using @spe
}

## Response snapshot

Successfully created comprehensive backend implementation specifications for the Phase II Todo App. The specification includes:

1. Main specification file with user scenarios, functional requirements, and success criteria
2. API specification detailing all endpoints, request/response contracts, and authentication rules
3. Database specification defining entities, relationships, and constraints
4. Feature specification outlining backend responsibilities and acceptance criteria
5. Authentication specification covering JWT lifecycle and Better Auth integration
6. Quality checklist to validate specification completeness

All specifications follow the required structure and focus on conceptual requirements rather than implementation details, ensuring alignment with the existing frontend while providing a complete backend specification.

## Outcome

- ✅ Impact: Complete backend specification created with all required components
- 🧪 Tests: Manual verification of all specification files
- 📁 Files: 6 specification files and 1 checklist created across multiple directories
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan phases
- 🧠 Reflection: Specification follows all requirements and maintains separation of concerns

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - all specifications meet requirements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A