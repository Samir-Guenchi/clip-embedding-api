# Hugging Face Space Keep-Alive Guide

Your Space goes to sleep after **48 hours of inactivity** on the free tier. Here are 3 solutions:

## 🥇 Option 1: Upgrade to Persistent Storage ($5/month)
**BEST SOLUTION** - Your Space will never sleep
- Go to your Space settings on HF
- Enable "Persistent Storage"
- $5/month, always active

## 🥈 Option 2: Deploy External Pinger (Free)

### A. Deploy on Railway (Recommended, Free tier available)
1. Create account at [railway.app](https://railway.app)
2. Create new project → "Deploy from GitHub repo"
3. Connect this repo (`hf-space-alg` folder)
4. Add environment variable:
   - Key: `HF_SPACE_URL`
   - Value: `https://huggingface.co/spaces/YOUR_USERNAME/alg`
5. Railway will auto-deploy using `Procfile` → runs `external_pinger.py`
6. Pings your Space every 25 minutes

### B. Deploy on Render.com (Alternative)
1. Create account at [render.com](https://render.com)
2. New → Background Worker
3. Connect GitHub repo
4. Build Command: `pip install -r requirements_pinger.txt`
5. Start Command: `python external_pinger.py`
6. Add environment variable `HF_SPACE_URL`

### C. Run on Your Server/Local Machine
```bash
# Install dependencies
pip install -r requirements_pinger.txt

# Set your Space URL
export HF_SPACE_URL="https://huggingface.co/spaces/YOUR_USERNAME/alg"

# Run the pinger (runs forever)
python external_pinger.py
```

## 🥉 Option 3: Use GitHub Actions (Free)

Create `.github/workflows/ping.yml` in your repo:

```yaml
name: Keep HF Space Alive
on:
  schedule:
    - cron: '*/25 * * * *'  # Every 25 minutes
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping HF Space
        run: |
          curl -s -o /dev/null -w "%{http_code}" ${{ secrets.HF_SPACE_URL }}
```

Add `HF_SPACE_URL` to GitHub repo secrets.

## 📊 Comparison

| Method | Cost | Reliability | Setup |
|--------|------|-------------|-------|
| Persistent Storage | $5/mo | ⭐⭐⭐⭐⭐ | 1 min |
| Railway/Render | Free | ⭐⭐⭐⭐ | 5 min |
| GitHub Actions | Free | ⭐⭐⭐ | 3 min |
| Local Server | Free | ⭐⭐ | 2 min |

## 🔍 Current Setup

Your `app.py` now includes:
- `keep_alive.py` - Internal keep-alive (pings itself)
- `external_pinger.py` - External service (deploy separately)

**For best results**: Use **External Pinger on Railway** + set `SPACE_URL` in HF Space secrets (so internal ping also works).

## ⚡ Quick Start

1. **Push updated code to HF Space**:
```bash
cd hf-space-alg
git add .
git commit -m "Add keep-alive service"
git push
```

2. **Deploy external pinger on Railway**:
   - Connect repo → Auto-deploys
   - Set `HF_SPACE_URL` env var
   - Done! ✅

Your Space will now stay awake 24/7!
