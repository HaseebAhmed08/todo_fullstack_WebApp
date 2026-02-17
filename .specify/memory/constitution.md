<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: Core Principles for Todo Full-Stack Web App
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution - Phase II

## Core Principles

### I. Full-Stack Development Approach
All development follows a coordinated full-stack methodology where frontend and backend components are designed and implemented in parallel. Frontend (Next.js) and backend (FastAPI) teams maintain tight integration through well-defined API contracts.

### II. Specification-Driven Development
Every feature begins with a complete specification in the /specs directory before any implementation work starts. Specifications must include user stories, acceptance criteria, and technical requirements before development proceeds.

### III. Test-First Implementation (NON-NEGOTIABLE)
All code must be developed following TDD practices: Tests written → Requirements validated → Tests fail → Then implement. Both unit and integration tests are mandatory for all new functionality.

### IV. Security-First Architecture
Authentication and authorization are built into every feature from the ground up. JWT tokens issued by Better Auth must secure all API endpoints, with proper validation on both frontend and backend.

### V. Responsive Design Priority
All UI components must be responsive and accessible across devices. Frontend implementation must follow modern UX best practices with mobile-first design principles.

### VI. Monorepo Organization
Code organization follows the defined monorepo structure with clear separation between frontend (/frontend), backend (/backend), and specifications (/specs). Dependencies between components are managed through proper import paths.

## Additional Constraints

### Technology Stack Requirements
- Frontend: Next.js 16+ with App Router
- Backend: FastAPI with SQLModel and Neon PostgreSQL
- Authentication: Better Auth with JWT
- File Structure: Strict adherence to monorepo organization with /frontend, /backend, and /specs directories

### Performance Standards
- API response times under 500ms for standard operations
- Page load times under 2 seconds for initial render
- Proper caching strategies implemented for optimized performance

## Development Workflow

### Agent Responsibilities
1. Spec Writer Agent - Write and maintain all specifications in /specs
2. Architecture Planner Agent - Document system architecture and data flow
3. Database Engineer Agent - Design and maintain database schema
4. Backend Engineer Agent - Implement FastAPI endpoints, enforce JWT auth
5. Frontend Engineer Agent - Build pages, components, API integration
6. Integration Tester Agent - Validate end-to-end functionality and compliance with specs

### Implementation Process
1. Read relevant spec (@specs/features/xxx.md)
2. Implement backend/frontend via respective CLAUDE.md guidance
3. Test integration (Integration Tester Agent)
4. Iterate and update spec if needed
5. All changes must pass QA checks defined in CLAUDE.md

## Governance

All development activities must comply with this constitution. Changes to core principles require explicit approval and documentation of the impact on existing implementations. The constitution serves as the authoritative guide for all technical decisions and development practices.

**Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26