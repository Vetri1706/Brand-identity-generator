# 🚀 Complete Setup & Deployment Guide

## Project Overview

Brand Identity Generator MVP is a **production-ready fullstack application** with:

- ✅ **Next.js Frontend** - Premium React UI with Tailwind CSS
- ✅ **FastAPI Backend** - Python LLM service with Together AI
- ✅ **LLM Training Pipeline** - Fine-tune models for specific company types
- ✅ **Comprehensive Documentation** - This complete guide

**Time to Deploy: 30-45 minutes**

---

## 📋 Prerequisites

### System Requirements

- **OS**: Windows, macOS, or Linux
- **Node.js**: 18.17+ (for frontend)
- **Python**: 3.10+ (for backend)
- **Git**: Latest version

### Required Accounts

1. **Together AI** - For LLM inference (Free tier: $5 free credits)

   - Sign up: https://www.together.ai
   - Get API Key from dashboard

2. **GitHub** - For version control (optional but recommended)

3. **Vercel** - For frontend deployment (Free tier available)

   - Sign up: https://vercel.com

4. **Render** - For backend deployment (Free tier available)
   - Sign up: https://render.com

---

## 🔧 Local Development Setup

### 1. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
# TOGETHER_API_KEY=your_key_here
# COHERE_API_KEY=your_key_here (optional)
```

**Start Backend:**

```bash
python main.py
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 2. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
# or
yarn dev
# App runs at http://localhost:3000
```

**Verify Setup:**

- Frontend: Open http://localhost:3000
- Backend API: Open http://localhost:8000/docs
- Both should be accessible

---

## 🧠 LLM Training Pipeline

### Option 1: Run Locally (Quick Test)

```bash
cd training

# Install dependencies
pip install -r ../backend/requirements.txt

# Run training pipeline
python finetune.py
```

This creates sample datasets and training prompts.

### Option 2: Fine-tune via Together AI (Recommended)

```bash
# After running local pipeline, upload to Together AI:

# 1. Get your training data
cd training
ls -la data/training/training_prompts.jsonl

# 2. Fine-tune using Together AI CLI or API
# See the guide output from finetune.py for exact commands

# 3. Cost: ~$10-50 per fine-tuning job
# 4. Once trained, update backend with new model ID
```

---

## 🌐 Deployment

### Frontend Deployment (Vercel - 5 minutes)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy frontend
cd frontend
vercel deploy

# 3. When prompted:
# - Link to GitHub project: (or skip)
# - Deploy as new project: Yes
# - Framework: Next.js
# - Build command: npm run build

# 4. Add environment variable
# NEXT_PUBLIC_API_URL=<your-backend-url>

# 5. Get Vercel URL from output
```

**Vercel Configuration Example:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "env": {
    "NEXT_PUBLIC_API_URL": "@backend_url"
  }
}
```

### Backend Deployment (Render - 10 minutes)

```bash
# 1. Create Render account at https://render.com

# 2. Push code to GitHub (required for Render)
git add .
git commit -m "Ready for deployment"
git push origin main

# 3. In Render Dashboard:
# - New -> Web Service
# - Connect GitHub repository
# - Select branch: main
# - Environment: Python 3.10
# - Build Command: pip install -r requirements.txt
# - Start Command: python main.py
# - Instance Type: Free or Starter
# - Environment Variables:
#   TOGETHER_API_KEY=your_key
#   ENVIRONMENT=production
#   DEBUG=false

# 4. Deploy and wait 2-3 minutes
```

**Backend Environment Variables (Render):**

```
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
TOGETHER_API_KEY=your_together_ai_key
COHERE_API_KEY=your_cohere_key
CORS_ORIGINS=["https://your-vercel-app.vercel.app","https://yourdomain.com"]
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              Brand Identity Generator                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐         ┌──────────────────────┐  │
│  │  Frontend (Next) │◄───────►│  Backend (FastAPI)   │  │
│  │  - React UI      │  HTTP   │  - LLM Service       │  │
│  │  - Tailwind CSS  │         │  - Orchestration     │  │
│  │  - Animations    │         │  - Error Handling    │  │
│  └──────────────────┘         └──────────────────────┘  │
│         ▲                              ▲                 │
│         │ (Vercel)              (Render/Railway)        │
│         │ Hosted                 Hosted                 │
│  ┌──────┴─────────┐         ┌────────┴────────────┐    │
│  │ CDN / Cache    │         │  LLM API Integration│    │
│  │ Auto-scaling   │         │  • Together AI       │    │
│  └────────────────┘         │  • Cohere (optional) │    │
│                             └─────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Training Pipeline (Optional, Run Locally)         │ │
│  │  • Data Preparation                               │ │
│  │  • Fine-tuning Scripts                            │ │
│  │  • Evaluation Metrics                             │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing the Application

### Test Frontend

```bash
# Start frontend
npm run dev

# Visit http://localhost:3000
# 1. Fill in company form
# 2. Submit and wait for generation
# 3. Review generated branding assets
# 4. Download results as JSON
```

### Test Backend API

```bash
# Backend running at localhost:8000

# 1. Health Check
curl http://localhost:8000/health

# 2. Get Company Types
curl http://localhost:8000/api/v1/company-types

# 3. Generate Branding (takes 30-60 seconds)
curl -X POST http://localhost:8000/api/v1/generate-branding \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "test_123",
    "company_profile": {
      "name": "TestCorp AI",
      "company_type": "ai_ml",
      "industry": "Artificial Intelligence",
      "description": "Testing brand generation",
      "target_audience": "Enterprise",
      "brand_values": ["Innovation", "Trust"]
    },
    "num_variations": 3,
    "focus": "all"
  }'
```

---

## 🔐 Environment Variables Explained

### Backend (.env)

| Variable           | Purpose                    | Example                                       |
| ------------------ | -------------------------- | --------------------------------------------- |
| `TOGETHER_API_KEY` | LLM API authentication     | `0a1b2c3d...`                                 |
| `COHERE_API_KEY`   | Fallback LLM provider      | `0a1b2c3d...`                                 |
| `ENVIRONMENT`      | Production/Development     | `production`                                  |
| `DEBUG`            | Debug mode (false in prod) | `false`                                       |
| `LLM_MODEL`        | Model to use               | `NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO` |
| `CORS_ORIGINS`     | Allowed frontends          | `["https://myapp.vercel.app"]`                |
| `LOG_LEVEL`        | Logging verbosity          | `INFO`                                        |

### Frontend (.env.local)

| Variable              | Purpose         | Example                   |
| --------------------- | --------------- | ------------------------- |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://api.mybrand.com` |

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Check API key
echo $TOGETHER_API_KEY  # Should show key

# Enable debug mode
DEBUG=true python main.py
```

### Frontend Can't Connect to Backend

```bash
# 1. Verify backend is running
curl http://localhost:8000/health

# 2. Check CORS configuration
# Backend CORS_ORIGINS should include frontend URL

# 3. Check .env.local
cat .env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. Restart frontend
npm run dev
```

### Slow Generation (>2 minutes)

- First call may be slower (model loading)
- Check Together AI quota: https://together.ai/
- Consider upgrading API tier
- Reduce `num_variations` parameter

---

## 📈 Performance Optimization

### Frontend

```javascript
// Use Next.js Image optimization
import Image from "next/image";

// Implement code splitting
const BrandingResults = dynamic(() => import("@/components/BrandingResults"));

// Cache API responses
const cacheTime = 3600; // 1 hour
```

### Backend

```python
# Add caching decorator
from functools import lru_cache

@lru_cache(maxsize=128)
def get_company_types():
    return [...]

# Use async operations
async def generate_branding(request):
    # Non-blocking operations
    ...
```

---

## 🚀 Production Checklist

- [ ] Environment variables set on all platforms
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] SSL/HTTPS enabled
- [ ] Database backups (if using)
- [ ] Monitoring and logging configured
- [ ] Error tracking setup (Sentry, etc.)
- [ ] Performance monitoring (Datadog, etc.)
- [ ] API documentation updated
- [ ] User authentication (optional)

---

## 📚 Additional Resources

- [Together AI Docs](https://docs.together.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Render Deployment Guide](https://render.com/docs)
- [Vercel Deployment Guide](https://vercel.com/docs)

---

## 💬 Support & Community

- Issues & Bugs: Create GitHub issues
- Questions: Check documentation first
- Feature Requests: Open GitHub discussions
- Community Forum: Discord / Slack (if available)

---

## 📝 License & Credits

- Built with ❤️ using Next.js, FastAPI, and LLM technology
- Open source and ready for contribution
- For commercial use, see LICENSE.md

---

**Last Updated:** November 2024
**Version:** 1.0.0-MVP
