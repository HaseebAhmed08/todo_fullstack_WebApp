# Phase II Frontend Implementation Plan

## Objective
Implement the frontend for the Phase II Todo Full-Stack Web App, adhering to the specified UI theme, animations, and secure JWT authentication.

## Technical Context
- **Framework**: Next.js 16+ with App Router
- **Styling**: Tailwind CSS with yellow-ish color palette (#FACC15)
- **Authentication**: Better Auth with JWT tokens
- **Backend API**: FastAPI + SQLModel endpoints
- **Features**: Task CRUD, User Authentication, Task Filtering/Sorting
- **Environment**: Monorepo structure with /frontend folder
- **Constraints**: Responsive design, professional animations, secure auth flow

## Constitution Check
- **Full-Stack Development Approach**: Ensure API integration follows well-defined contracts with backend
- **Specification-Driven Development**: All implementation follows the spec in @specs/1-frontend-yellow-ui/spec.md
- **Test-First Implementation**: All components and pages will have associated tests
- **Security-First Architecture**: JWT tokens properly handled and API requests secured
- **Responsive Design Priority**: Mobile-first responsive design implemented
- **Monorepo Organization**: Adhere to /frontend folder structure

## Gates
- [x] Specification exists and is complete
- [x] Technology stack defined in constitution
- [x] Architecture constraints understood
- [x] Security requirements clear
- [x] Performance standards defined

## Phase 0: Outline & Research

### Research Tasks

#### 1. Next.js 16+ App Router Implementation
- **Decision**: Use App Router for page routing and layout management
- **Rationale**: App Router is the recommended approach for Next.js 13+, offering better performance and developer experience
- **Alternatives considered**: Pages Router (legacy approach)

#### 2. Better Auth JWT Integration
- **Decision**: Implement Better Auth with JWT for authentication
- **Rationale**: Better Auth provides robust authentication with JWT support and integrates well with Next.js
- **Alternatives considered**: Auth.js, Clerk, custom JWT implementation

#### 3. Tailwind CSS Configuration
- **Decision**: Configure Tailwind with custom yellow color palette
- **Rationale**: Tailwind offers utility-first CSS approach that pairs well with Next.js
- **Alternatives considered**: Styled-components, Emotion, vanilla CSS modules

#### 4. API Integration Pattern
- **Decision**: Create centralized API client in /lib/api.ts with JWT handling
- **Rationale**: Centralized API client ensures consistent request handling and authentication
- **Alternatives considered**: Direct fetch calls, SWR, React Query

## Phase 1: Design & Contracts

### Data Model (data-model.md)
Based on the spec requirements, the frontend will work with these key entities:

1. **User Entity**
   - id: string
   - email: string
   - name: string
   - createdAt: Date
   - updatedAt: Date

2. **Task Entity**
   - id: string
   - title: string
   - description: string
   - completed: boolean
   - userId: string
   - createdAt: Date
   - updatedAt: Date

### API Contracts
The frontend will interact with these backend endpoints (to be implemented in the backend):

- POST /api/auth/signup - User registration
- POST /api/auth/signin - User authentication
- GET /api/tasks - Get user tasks
- POST /api/tasks - Create new task
- PUT /api/tasks/:id - Update task
- DELETE /api/tasks/:id - Delete task
- GET /api/profile - Get user profile
- PUT /api/profile - Update user profile

### Quickstart Guide
1. Navigate to the /frontend directory
2. Install dependencies: `npm install`
3. Configure environment variables for API URLs and auth
4. Start development server: `npm run dev`

### Subtasks Breakdown

#### 1. Project Setup
- **Verify Project Structure**: Confirm the `/frontend` folder structure is correct.
- **Install Tailwind CSS**: Configure Tailwind with the yellow-ish color palette (#FACC15) and ensure it's applied globally.
- **Configure Better Auth**: Set up the JWT plugin, and ensure environment variables (NEXT_PUBLIC_API_URL, BETTER_AUTH_URL, BETTER_AUTH_SECRET) are properly defined.

#### 2. Component Development (Priority 1)
- **Header Component (Header.tsx)**: Create a navigation bar with yellow accents and a logout button. Ensure it is responsive and user-friendly.
- **TaskCard Component (TaskCard.tsx)**: Design the task card component with hover animations and smooth transitions.
- **TaskList Component (TaskList.tsx)**: Develop a grid/list view for tasks with professional animations and responsive design.
- **LoadingSpinner Component (LoadingSpinner.tsx)**: Implement a Tailwind CSS animated spinner for loading states.
- **ErrorAlert Component (ErrorAlert.tsx)**: Create animated error messages that are visually clear and consistent.

#### 3. API Integration (Priority 2)
- **API Client (/lib/api.ts)**: Implement functions to handle all CRUD operations, ensuring JWT tokens are attached to headers and errors are managed gracefully.

#### 4. Page Development (Priority 3)
- **Signup Page (/signup/page.tsx)**: Implement the signup form with validation, animations, and responsive design. Integrate Better Auth for user registration.
- **Signin Page (/signin/page.tsx)**: Build the signin form, handle JWT token storage, and provide proper error handling and animations.
- **Dashboard Page (/dashboard/page.tsx)**: Create the task list with filtering, sorting, and task creation features. Integrate API calls and ensure smooth animations.
- **Task Detail Page (/tasks/[id]/page.tsx)**: Develop the task detail and update page, ensuring data fetching and updates are seamless and animated.
- **Profile Page (/profile/page.tsx)**: Implement user profile management with the ability to edit user information and view tasks.

#### 5. State Management (Integrated)
- **React State/Context**: Use React state or context to manage tasks and user session. Ensure UI updates immediately after any CRUD operation and handle loading and error states effectively.

#### 6. Authentication & Route Protection (Integrated)
- **Better Auth Integration**: Utilize Better Auth hooks (`useSession`, `signIn`, `signOut`) to manage user sessions.
- **Protected Routes**: Implement middleware/hooks to protect `/dashboard` and `/tasks/*` pages, redirecting unauthenticated users to `/signin`.

#### 7. Animations & Styling (Ongoing)
- **Theme Implementation**: Apply the yellow-ish theme consistently across all UI components using Tailwind CSS.
- **Animations**: Implement professional animations such as fade-in, slide-up for task cards, button hover effects, and a rotating loading spinner.

## Phase 2: Implementation Steps

### Week 1: Setup and Components
1. Set up Next.js project with Tailwind CSS
2. Configure Better Auth
3. Create all reusable components
4. Implement basic styling with yellow theme

### Week 2: API Integration and Authentication
1. Create API client with JWT handling
2. Implement authentication flow
3. Set up protected routes
4. Add error handling

### Week 3: Page Development
1. Build signup and signin pages
2. Create dashboard page with task listing
3. Implement task detail and update functionality
4. Add profile management page

### Week 4: Polish and Testing
1. Add animations and transitions
2. Conduct integration testing
3. Fix bugs and optimize performance
4. Prepare for deployment

## Acceptance Criteria
- [ ] All pages are fully responsive and visually consistent
- [ ] Yellow-ish theme applied across all UI components
- [ ] Smooth animations make UI professional
- [ ] API integration works for task CRUD with JWT auth
- [ ] Protected routes prevent unauthorized access
- [ ] Errors and loading states are visually clear
- [ ] State updates immediately reflect user actions
- [ ] All components have associated tests

## Risk Assessment
1. **Authentication Complexity**: Better Auth JWT integration might require additional configuration
2. **API Integration**: Backend endpoints might not be ready on schedule
3. **Performance**: Animations might impact performance on lower-end devices
4. **Responsive Design**: Ensuring consistency across all device sizes

## Success Metrics
- All acceptance criteria met
- Page load times under 2 seconds
- Zero critical security vulnerabilities
- Cross-browser compatibility achieved
- Mobile-responsive design validated