# Vercel Deployment Guide

## Step 1: Vercel CLI Install karein
```bash
npm install -g vercel
```

## Step 2: Vercel se login karein
```bash
vercel login
```

## Step 3: Project deploy karein
```bash
cd "E:\giaic hacathones\todo_fullstack_WebApp"
vercel
```

## Step 4: Environment Variables set karein
Vercel Dashboard mein jaakar ye variables add karein:

### Required Variables:
- `DATABASE_URL` - PostgreSQL connection string (Neon/Supabase use kar sakte hain)
- `BETTER_AUTH_URL` - Aapki Vercel app URL
- `BETTER_AUTH_SECRET` - 32+ characters ka secret key
- `NEXT_PUBLIC_API_URL` - Aapki Vercel app URL
- `ACCESS_TOKEN_EXPIRE_MINUTES` - 30 (default)

## Step 5: Production Deploy
```bash
vercel --prod
```

## Alternative: Vercel Dashboard se deploy
1. GitHub pe code push karein
2. Vercel.com pe jaakar "Add New Project" karein
3. GitHub repo select karein
4. Environment variables configure karein
5. Deploy button click karein

## Database Setup (Recommended: Neon)
1. https://neon.tech pe jaakar free account banayein
2. New project create karein
3. Connection string copy karein
4. Vercel mein `DATABASE_URL` variable mein paste karein

## Important Notes:
- Backend FastAPI ko Vercel serverless functions mein run hoga
- Database external hona chahiye (Neon, Supabase, Railway, etc.)
- JWT secret strong hona chahiye (32+ characters)
