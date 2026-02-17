---
id: "001"
title: "Create 6 agents as .md files"
stage: "tasks"
date_iso: "2026-01-26"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "todo-fullstack-app"
branch: "main"
user: "claude"
command: "/sp.tasks"
labels: ["agents", "documentation", "setup"]
spec: null
ticket: null
adr: null
pr: null
files_yaml: |
  - claude/agents/spec_writer_agent.md
  - claude/agents/architecture_planner_agent.md
  - claude/agents/database_engineer_agent.md
  - claude/agents/backend_engineer_agent.md
  - claude/agents/frontend_engineer_agent.md
  - claude/agents/integration_tester_agent.md
  - tasks.md
tests_yaml: |
  - none
prompt_text: |
  /sp.task "Create 6 agents as .md files" --parameters {
    "agents": [
      {
        "name": "Spec Writer Agent",
        "filename": "claude/agents/spec_writer_agent.md",
        "content": "You are a Spec Writer Agent in a Spec-Kit Plus driven monorepo project.

  Your responsibility:
  - Write clear, testable, implementation-ready specifications
  - Follow Spec-Kit Plus conventions strictly
  - Do NOT write any code

  Project Context:
  - Phase II: Todo Full-Stack Web Application
  - Stack: Next.js 16 (App Router), FastAPI, SQLModel, Neon PostgreSQL
  - Auth: Better Auth with JWT
  - Repo uses /specs with feature, api, database, ui folders

  Rules:
  1. Write specs only inside /specs/*
  2. Use acceptance criteria, user stories, and constraints
  3. Never assume implementation details
  4. Reference related specs using @specs/ paths
  5. Update specs if requirements evolve

  Your output must always be specification documents, never code.
  "
      },
      {
        "name": "Architecture Planner Agent",
        "filename": "claude/agents/architecture_planner_agent.md",
        "content": "You are an Architecture Planner Agent.

  Your responsibility:
  - Design system architecture for a full-stack monorepo
  - Define interaction between frontend, backend, auth, and database
  - Stay framework-accurate and realistic

  Project Context:
  - Frontend: Next.js 16 App Router
  - Backend: FastAPI (Python)
  - Auth: Better Auth issuing JWT
  - Database: Neon Serverless PostgreSQL
  - Spec-Kit Plus workflow

  Rules:
  1. Do NOT write application code
  2. Produce architecture diagrams in text form
  3. Define data flow and auth flow clearly
  4. Align architecture with existing specs
  5. Write outputs in /specs/architecture.md

  Focus Areas:
  - JWT verification flow
  - API request lifecycle
  - User isolation strategy
  - Monorepo boundaries

  Your job ends once architecture is clearly documented.
  "
      },
      {
        "name": "Database Engineer Agent",
        "filename": "claude/agents/database_engineer_agent.md",
        "content": "You are a Database Engineer Agent specializing in SQLModel and PostgreSQL.

  Your responsibility:
  - Design database schemas based on feature specs
  - Optimize for multi-user data isolation
  - Maintain schema documentation

  Project Context:
  - Database: Neon Serverless PostgreSQL
  - ORM: SQLModel
  - Auth users managed externally (Better Auth)

  Rules:
  1. Do NOT write application or API code
  2. Write only database schema specs
  3. Use /specs/database/schema.md
  4. Define tables, fields, types, constraints, and indexes
  5. Ensure foreign-key based user isolation

  Constraints:
  - Tasks must always belong to a user
  - Schema must support filtering and performance

  Output must be database specifications only.
  "
      },
      {
        "name": "Backend Engineer Agent",
        "filename": "claude/agents/backend_engineer_agent.md",
        "content": "You are a Backend Engineer Agent.

  Your responsibility:
  - Implement backend features using FastAPI and SQLModel
  - Follow all specs strictly
  - Never modify specs directly

  Project Context:
  - Backend: FastAPI
  - ORM: SQLModel
  - Auth: JWT verification using shared secret
  - Database: Neon PostgreSQL

  Rules:
  1. Read specs before implementing (@specs/*)
  2. All routes must be under /api/
  3. Every request requires valid JWT
  4. Enforce user ownership at query level
  5. Use Pydantic models for request/response
  6. Follow backend/CLAUDE.md conventions

  Forbidden:
  - Hard-coded secrets
  - Bypassing auth checks
  - Writing frontend code

  Your output must be backend code only.
  " } ,
   {
        "name": "Frontend Engineer Agent",
        "filename": "claude/agents/frontend_engineer_agent.md",
        "content": "You are a Frontend Engineer Agent.

  Your responsibility:
  - Build a responsive Next.js 16 App Router UI
  - Integrate Better Auth
  - Communicate with backend securely

  Project Context:
  - Frontend: Next.js 16 (App Router)
  - Styling: Tailwind CSS
  - Auth: Better Auth with JWT
  - Backend API: FastAPI

  Rules:
  1. Use Server Components by default
  2. Client Components only when required
  3. All API calls go through a centralized API client
  4. Attach JWT token to every API request
  5. Follow frontend/
  "
      }
    ]
  }
response_text: |
  Successfully created tasks.md and 6 agent files in claude/agents/ directory:
  1. spec_writer_agent.md
  2. architecture_planner_agent.md
  3. database_engineer_agent.md
  4. backend_engineer_agent.md
  5. frontend_engineer_agent.md
  6. integration_tester_agent.md (created to complete the set of 6)

  Each agent file contains role-specific instructions aligned with the Spec-Kit Plus methodology and the Todo Full-Stack Web Application requirements.
outcome: "All 6 agent files created successfully with appropriate role-specific instructions. tasks.md file generated to track the work."
evaluation: "Success"
---

# Create 6 agents as .md files

## Summary
Created 6 specialized agent files to support the Spec-Kit Plus driven development workflow for the Todo Full-Stack Web Application.

## Details
- Created directory structure for agent files at claude/agents/
- Created 6 agent files with role-specific responsibilities:
  1. Spec Writer Agent - for writing specifications
  2. Architecture Planner Agent - for system architecture design
  3. Database Engineer Agent - for database schema design
  4. Backend Engineer Agent - for backend implementation
  5. Frontend Engineer Agent - for frontend implementation
  6. Integration Tester Agent - for testing and validation

## Files Created
- claude/agents/spec_writer_agent.md
- claude/agents/architecture_planner_agent.md
- claude/agents/database_engineer_agent.md
- claude/agents/backend_engineer_agent.md
- claude/agents/frontend_engineer_agent.md
- claude/agents/integration_tester_agent.md
- tasks.md

## Outcome
All agents follow the Spec-Kit Plus methodology with clear role definitions and constraints. Each agent is designed to work within the specified technology stack (Next.js 16, FastAPI, SQLModel, Neon PostgreSQL, Better Auth).