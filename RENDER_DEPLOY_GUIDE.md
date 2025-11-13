# 🎨 FREE RENDER DEPLOYMENT GUIDE

## ⚡ Deploy on Render.com (Alternative to Railway)

### Why Render?
- ✅ FREE tier with 750 hours/month
- ✅ Auto-deploys from GitHub  
- ✅ Built-in SSL certificates
- ✅ Great for Python backends

### Step 1: Setup
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"

### Step 2: Configuration
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python main.py`
- **Environment**: `Python 3`
- **Branch**: `main`

### Step 3: Environment Variables
Add in Render dashboard:
```
PORT=10000
PYTHON_VERSION=3.11
```

### Free Tier Limits:
- 750 hours/month (enough for demos)
- 512MB RAM
- Spins down after 15min inactivity (cold starts)
- Custom domains on free tier ✅

### Live URL:
Your app will be at: `https://yourapp.onrender.com`