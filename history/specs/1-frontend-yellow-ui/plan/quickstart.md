# Frontend Quickstart Guide

## Prerequisites
- Node.js 18+ installed
- Access to backend API endpoints
- Environment configured for development

## Setup Instructions

### 1. Clone and Navigate
```bash
cd /frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend root with the following:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-secret-here
```

### 4. Run Development Server
```bash
npm run dev
```

## Key Technologies
- Next.js 16+ with App Router
- Tailwind CSS for styling
- Better Auth for authentication
- TypeScript for type safety

## Project Structure
```
/frontend
├── /app          # Next.js App Router pages
│   ├── /signup
│   ├── /signin
│   ├── /dashboard
│   ├── /tasks
│   └── /profile
├── /components   # Reusable UI components
├── /lib          # Utilities and API client
└── /styles       # Global styles
```

## Running Tests
```bash
npm run test
```

## Building for Production
```bash
npm run build
npm start
```