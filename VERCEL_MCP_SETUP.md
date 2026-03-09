# Vercel MCP Setup Guide

## Vercel MCP Server ko connect karne ke liye:

### Step 1: Vercel MCP install karein
Apne global Claude config file mein ye add karein:

**File:** `C:\Users\WELCOME DEKVER WORLD\.claude\settings.json`

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": ["-y", "@vercel/mcp"],
      "env": {
        "VERCEL_TOKEN": "your-vercel-token"
      }
    }
  }
}
```

### Step 2: Vercel Token generate karein
1. https://vercel.com/account/settings pe jaayein
2. "Access Tokens" section mein
3. "Create" click karein
4. Token ko copy karein aur upar `VERCEL_TOKEN` mein paste karein

### Step 3: Claude restart karein
Claude ko restart karein taake MCP server load ho jaye

## Alternative: Direct Vercel CLI use karein

Agar MCP setup nahi karna chahte, toh Vercel CLI directly use kar sakte hain:

```bash
# Install
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

## Current Project Status:
- ✅ Frontend Vercel pe deploy ho raha hai
- ⏳ Backend Railway/Render pe deploy karna hai
- ⏳ Environment variables configure karne hain
