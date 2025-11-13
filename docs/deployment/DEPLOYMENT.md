# 🚀 Deployment Strategies

## Overview

Three deployment options tailored to different needs and budgets.

---

## Option 1: Free Tier (Recommended for MVP)

**Cost**: $0/month

### Frontend: Vercel (Free)

- Auto-deploys from GitHub
- Built-in CDN
- 100GB bandwidth/month
- Automatic SSL

### Backend: Render (Free)

- Auto-deploys from GitHub
- Sleeps after 15 min inactivity (cold starts)
- 0.5GB RAM
- Enough for MVP testing

**Total Setup Time**: 30 minutes

```bash
# 1. Push to GitHub
git push origin main

# 2. Vercel: Connect GitHub repo
# - Go to vercel.com
# - Click "New Project"
# - Select your repo
# - Add env: NEXT_PUBLIC_API_URL

# 3. Render: Connect GitHub repo
# - Go to render.com
# - Click "New Web Service"
# - Select your repo
# - Runtime: Python 3.10
# - Build: pip install -r requirements.txt
# - Start: python main.py
# - Add env: TOGETHER_API_KEY
```

---

## Option 2: Paid Hobby (For Development)

**Cost**: ~$15-30/month

### Frontend: Vercel Pro

- Better performance
- Priority support
- $20/month for premium features

### Backend: Render Starter

- Always running
- 2GB RAM
- $12/month

**Total**: ~$32/month

---

## Option 3: Production Grade

**Cost**: $100-500+/month

### Architecture

```
Frontend:
  - Vercel Pro (or self-hosted)
  - CloudFlare CDN
  - Custom domain SSL

Backend:
  - AWS / Google Cloud / Azure
  - Auto-scaling
  - Dedicated GPU for LLM
  - PostgreSQL database
  - Redis cache
  - CloudWatch monitoring
```

---

## Step-by-Step: Vercel Deployment

### Prerequisites

- GitHub account with code pushed
- Vercel account (free)

### Steps

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Navigate to frontend
cd frontend

# 3. Deploy
vercel deploy

# 4. Choose options:
#    - Link to existing project? (n if first time)
#    - Set project name? (yes)
#    - Production? (yes)

# 5. Add environment variable
vercel env add NEXT_PUBLIC_API_URL
# Input: your-backend-url.onrender.com

# 6. Redeploy with env vars
vercel deploy --prod
```

Your frontend is now live! 🎉

---

## Step-by-Step: Render Deployment

### Prerequisites

- GitHub account (must have code pushed)
- Render account (free)

### Steps

1. **Go to render.com dashboard**

2. **Click "New +" → "Web Service"**

3. **Connect GitHub**

   - Authorize Render with GitHub
   - Select your repository
   - Select branch: main

4. **Configure**

   - Name: brand-identity-generator-backend
   - Environment: Python 3
   - Region: Choose closest to you
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

5. **Add Environment Variables**

   - TOGETHER_API_KEY: your_key
   - ENVIRONMENT: production
   - DEBUG: false
   - CORS_ORIGINS: ["https://your-frontend.vercel.app"]

6. **Deploy**

   - Click "Create Web Service"
   - Wait 2-3 minutes for first deploy
   - Get your backend URL

7. **Update Frontend**
   ```bash
   cd frontend
   vercel env add NEXT_PUBLIC_API_URL
   # Input: https://your-backend.onrender.com
   vercel deploy --prod
   ```

Your app is now live! 🚀

---

## Self-Hosted Option

### Docker Setup

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      TOGETHER_API_KEY: ${TOGETHER_API_KEY}
      ENVIRONMENT: production
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000
    restart: always
```

```bash
# Run with Docker Compose
docker-compose up -d
```

---

## Monitoring & Logging

### Vercel Analytics

- Built-in performance monitoring
- Real User Monitoring (RUM)
- Error tracking

### Render Logs

- View in dashboard
- Real-time streaming
- Historical logs

### DIY Monitoring (Production)

```python
# Add to backend
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

---

## Cost Comparison

| Option     | Frontend          | Backend         | Monthly   | Cold Start | Downtime |
| ---------- | ----------------- | --------------- | --------- | ---------- | -------- |
| Free       | Vercel Free       | Render Free     | $0        | Yes        | None     |
| Hobby      | Vercel Pro        | Render Starter  | $32       | No         | None     |
| Standard   | Vercel Pro        | Render Standard | $60       | No         | None     |
| Production | Vercel Enterprise | AWS/GCP/Azure   | $200-500+ | No         | 0        |

---

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] API keys are valid and not in code
- [ ] .gitignore properly configured
- [ ] README and docs up to date
- [ ] Error handling implemented
- [ ] CORS configured correctly
- [ ] Frontend build successful (`npm run build`)
- [ ] Backend starts without errors (`python main.py`)
- [ ] Health check endpoint works
- [ ] API endpoints tested
- [ ] Rate limiting considered
- [ ] Monitoring set up

---

## Post-Deployment

### Smoke Tests

```bash
# 1. Health check
curl https://your-backend.onrender.com/health

# 2. Generate branding
curl -X POST https://your-backend.onrender.com/api/v1/generate-branding \
  -H "Content-Type: application/json" \
  -d '{...}'

# 3. Test frontend
Open https://your-app.vercel.app
```

### Monitoring

- Check Vercel Analytics
- Check Render Logs
- Monitor API response times
- Set up error alerts

### Optimization

- Enable caching headers
- Optimize images
- Minify CSS/JS
- Consider CDN

---

## Troubleshooting Deployments

### Frontend won't deploy

```bash
# Check build locally
npm run build

# Check for environment variables
echo $NEXT_PUBLIC_API_URL

# Check for unused variables in code
npm run lint
```

### Backend won't start

```bash
# Check dependencies
cat requirements.txt

# Check for syntax errors
python -m py_compile main.py

# Test locally first
python main.py
```

### CORS errors

```
Update CORS_ORIGINS in backend/.env
Include your frontend URL exactly as it appears in browser
```

### Cold start too slow

- Upgrade Render plan
- Use Vercel Pro with automatic scaling
- Pre-warm functions (optional)

---

## Next Steps

1. Deploy frontend to Vercel
2. Deploy backend to Render
3. Test full integration
4. Monitor for errors
5. Optimize performance
6. Plan scaling strategy

**Congratulations! Your app is live!** 🎉

---

_For detailed instructions, see SETUP_GUIDE.md_
