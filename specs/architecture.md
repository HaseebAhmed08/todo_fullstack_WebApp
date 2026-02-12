# System Architecture

## Monorepo Structure
The project is organized as a monorepo to allow Claude Code to edit both frontend and backend in a single context.

### Folder Structure
- `/frontend` - Next.js 16+ (App Router), TypeScript, Tailwind CSS.
- `/backend` - Python FastAPI, SQLModel, SQLServer/Postgres (Neon).
- `/specs` - Organized specifications for the project.

## Tech Stack
- **Frontend**: Next.js, React, Tailwind CSS, Lucide React.
- **Backend**: FastAPI, SQLModel, Pydantic.
- **Database**: Neon (PostgreSQL).
- **Authentication**: Better Auth (Frontend) + JWT Verification (Backend).

## Authentication Flow
Uses JWT tokens issued by Better Auth on the frontend.
The backend verifies these tokens using a shared `BETTER_AUTH_SECRET`.
All API requests must include the JWT in the Authorization header.
