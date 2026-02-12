# Phase II Frontend Specification

## Project Context
- Framework: Next.js 16+ (App Router)
- Styling: Tailwind CSS with yellow-ish color palette
- Auth: Better Auth with JWT tokens
- Backend: FastAPI + SQLModel
- Features: Task CRUD, User Authentication, Task Filtering/Sorting
- Monorepo: /frontend folder

## Pages to Implement
1. /signup/page.tsx - Signup form with validation and animations
2. /signin/page.tsx - Signin form with JWT token storage
3. /dashboard/page.tsx - List of tasks, filtering, sorting, task creation
4. /tasks/[id]/page.tsx - Task detail and update page
5. /profile/page.tsx - User profile management

## Components
- Header.tsx - Navigation bar, logout button, yellow accents
- TaskCard.tsx - Display individual task with animation on hover
- TaskList.tsx - Grid/list view of tasks with smooth transitions
- LoadingSpinner.tsx - Animated spinner using Tailwind CSS
- ErrorAlert.tsx - Animated error messages

## Theme & Styling
- Primary color: Yellow-ish (#FACC15, Tailwind yellow-400)
- Accent colors: Complementary grays and whites
- Professional animations: fade-in, slide-up for task cards, button hover effects, loading spinners
- Responsive design: mobile-first, breakpoints for tablet and desktop

## API Integration
- /lib/api.ts to handle all CRUD operations
- Attach JWT token to Authorization header for all requests
- Handle errors gracefully and update UI accordingly

## State Management
- Use React state or context to manage tasks and session
- Update UI immediately after create/update/delete operations
- Loading and error states must be clearly shown

## Auth & Route Protection
- Use Better Auth hooks (useSession, signIn, signOut)
- Protect /dashboard and /tasks/* pages via middleware/hooks
- Redirect unauthenticated users to /signin

## Animations
- TaskCard hover: scale-up + shadow + smooth transition
- Page load: fade-in + slide-up effect for main content
- Buttons: hover color change with subtle motion
- Loading spinner: rotate animation

## Acceptance Criteria
1. All pages are fully responsive and visually consistent
2. Yellow-ish theme applied across all UI components
3. Smooth animations make UI professional
4. API integration works for task CRUD with JWT auth
5. Protected routes prevent unauthorized access
6. Errors and loading states are visually clear
7. State updates immediately reflect user actions

## References
- Spec references: @specs/features/task-crud.md, @specs/features/authentication.md
- Tailwind CSS classes for colors, spacing, typography, and animations
- Follow frontend/CLAUDE.md guidance for component and page patterns

## Output Expectations
- Fully functional frontend with all specified pages and components
- Professional, polished UI with yellow-themed design
- Proper authentication and authorization flow
- Smooth animations and responsive design