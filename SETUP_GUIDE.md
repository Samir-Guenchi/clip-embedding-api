# Keep Hugging Face Space Alive - Setup Guide

Your Space URL: **https://samirdze-alg.hf.space**

## Problem
Free Hugging Face Spaces go to sleep after 48 hours of inactivity.

## Solution
Use GitHub Actions to ping your Space every 30 minutes (100% FREE!).

## Setup Instructions

### 1️⃣ Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `hf-space-alg` (or any name)
3. Make it **Public** (required for free Actions)
4. Click "Create repository"

### 2️⃣ Push Code to GitHub
```bash
cd "c:\Users\Samir Guenchi\Desktop\basma\hf-space-alg"
git remote add github https://github.com/YOUR_USERNAME/hf-space-alg.git
git push github main
```

### 3️⃣ Activate GitHub Actions
1. Go to your GitHub repo
2. Click **Actions** tab
3. Click "I understand my workflows, go ahead and enable them"
4. Your Space will now be pinged every 30 minutes automatically! ✅

### 4️⃣ Test It (Optional)
1. Go to Actions tab
2. Click "Keep HF Space Alive" workflow
3. Click "Run workflow" button
4. Watch it ping your Space in real-time!

## How It Works
- GitHub Actions runs a cron job every 30 minutes
- Sends HTTP request to your Space URL
- Keeps your Space awake 24/7
- Completely free with GitHub's 2,000 free minutes/month

## Notes
- Make sure your GitHub repo is **PUBLIC** for free Actions
- First run might take a few minutes to start
- Check "Actions" tab to see ping history
