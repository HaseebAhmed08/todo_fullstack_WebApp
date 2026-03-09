# GitHub Pages Deployment Guide for HaseebAhmed08/todo_fullstack_WebApp

---

## Introduction
This guide will walk you through the deployment of your full-stack todo application. The frontend will be hosted on GitHub Pages, while the backend will be hosted on a free hosting service. 

## Prerequisites
- A GitHub account
- Access to the repository **HaseebAhmed08/todo_fullstack_WebApp**
- Basic knowledge of Git and the command line
- A text editor (e.g., Visual Studio Code)

## Step 1: Prepare Your Frontend for Deployment
1. **Build the Frontend:**
   - Navigate to the frontend directory of your project in the terminal.
   - Run the build command to create a production-ready version of your application.
     ```bash
     npm run build
     ```
   - This will create a `build` folder containing all the optimized files for deployment.

2. **Add a GitHub Pages branch:**
   - In your project, create a new branch called `gh-pages`.
     ```bash
     git checkout -b gh-pages
     ```
   - Copy the contents of the `build` folder into the root of your `gh-pages` branch.

3. **Push the `gh-pages` branch to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy frontend to GitHub Pages"
   git push origin gh-pages
   ```

## Step 2: Configure GitHub Pages
1. **Go to Your Repository Settings:**
   - Navigate to your repository on GitHub.
   - Click on the `Settings` tab.

2. **Enable GitHub Pages:**
   - Scroll down to the `Pages` section.
   - Under `Source`, select the `gh-pages` branch and click `Save`.

3. **Access Your Deployed App:**
   - After a few minutes, your site will be published at `https://HaseebAhmed08.github.io/todo_fullstack_WebApp/`.

## Step 3: Prepare Your Backend for Deployment
1. **Choose a Free Hosting Service:**
   - Popular choices include Heroku, Vercel, or Render. For this guide, we will use Render.

2. **Set Up an Account on Render:**
   - Go to the Render website and create an account.

3. **Deploy Your Backend:**
   - Create a new web service on Render:
     - Connect your GitHub account.
     - Select your repository (**HaseebAhmed08/todo_fullstack_WebApp**).
     - Choose the branch that contains your backend code.
     - Set the build command (e.g., `npm install`).
     - Set the start command (e.g., `node server.js`).

4. **Configure Environment Variables:**
   - If your application uses environment variables (like API keys), make sure to set those in the Render dashboard.

5. **Deploy:**
   - Click on the `Create Web Service` button to deploy your backend.
   - After a successful deployment, Render will provide a public URL for your backend.

## Step 4: Connect Frontend to Backend
1. Update the API endpoints in your frontend code to point to the public URL of your backend service.
   - For example:
   ```javascript
   const API_URL = "https://your-backend-url.onrender.com/api";
   ```

2. Push the changes to the `main` branch of your repository.

## Conclusion
You have successfully deployed your full-stack todo application with the frontend hosted on GitHub Pages and the backend on Render. If you encounter any issues, review the logs in Render or the GitHub repository settings for GitHub Pages.

## Additional Resources
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Render Documentation](https://render.com/docs)