# LinkedIn Scraper - Streamlit Deployment Guide

This guide will walk you through deploying your LinkedIn Scraper application to Streamlit Cloud for permanent hosting.

## Prerequisites

1. A GitHub account
2. Your LinkedIn Scraper code (app.py and any other files)

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account
2. Click on the "+" icon in the top-right corner and select "New repository"
3. Name your repository (e.g., "linkedin-scraper")
4. Choose "Public" visibility (required for free Streamlit Cloud deployment)
5. Click "Create repository"

## Step 2: Upload Your Code to GitHub

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/yourusername/linkedin-scraper.git
   cd linkedin-scraper
   ```

2. Copy your LinkedIn Scraper files into this directory:
   - app.py
   - requirements.txt (create this file with the following content):
     ```
     streamlit
     pandas
     selenium
     beautifulsoup4
     ```

3. Commit and push your code:
   ```
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

## Step 3: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and the main file path (app.py)
5. Click "Deploy"

Your app will be deployed to a URL like: `https://yourusername-linkedin-scraper-app.streamlit.app`

## Step 4: Configure Your App (Optional)

1. In the Streamlit Cloud dashboard, find your app and click on the three dots menu
2. Select "Settings"
3. Here you can configure:
   - App name
   - Theme
   - Python version
   - Package dependencies
   - Environment variables (if needed)

## Step 5: Share Your App

Your app now has a permanent URL that you can share with others. Anyone with the link can access your LinkedIn Scraper application.

## Updating Your App

Whenever you want to update your app:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Streamlit Cloud will automatically detect the changes and redeploy your app

## Troubleshooting

If you encounter issues with your deployment:

1. Check the logs in the Streamlit Cloud dashboard
2. Ensure all required packages are listed in requirements.txt
3. Verify that your app works locally before deploying
4. Check that you're not exceeding Streamlit Cloud's free tier limits

## Streamlit Cloud Free Tier Limitations

- 1 app per account
- Public repositories only
- Limited compute resources
- No authentication built-in (we've implemented our own)

For more advanced needs, consider upgrading to Streamlit Cloud Teams or Enterprise.
