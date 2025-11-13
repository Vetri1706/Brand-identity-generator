# ☁️ Google Cloud Deployment - Quick Summary

## Yes, You Can Deploy to Google Cloud! ✅

This project is **fully compatible** with Google Cloud Platform (GCP). Here's what you need to know:

---

## 🚀 Recommended: Cloud Run (MVP & Production)

**Why Cloud Run?**

- ✅ Auto-scales from 0 to 1000+ instances
- ✅ Pay only for compute time (free tier: 2M requests/month)
- ✅ No infrastructure management
- ✅ 20-30 minute setup
- ✅ Perfect for startups and MVPs

**Cost**: $0-50/month

**Architecture**:

```
Frontend: Firebase Hosting ($0-10/month)
Backend:  Cloud Run         ($0-40/month)
Total:    $0-50/month
```

---

## 📋 Step-by-Step (10 minutes)

### 1. Prerequisites (5 min)

```bash
# Install gcloud CLI
# Download: https://cloud.google.com/sdk/docs/install

# Create Google Cloud Project
# Go to: https://console.cloud.google.com
# Create new project (get $300 free credit)

# Login locally
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Deploy Backend to Cloud Run (5 min)

```bash
cd backend

gcloud run deploy brand-identity-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars \
    TOGETHER_API_KEY=your-key-here,\
    COHERE_API_KEY=optional \
  --memory 1Gi
```

### 3. Deploy Frontend to Firebase (5 min)

```bash
cd frontend

npm run build
firebase deploy --only hosting
```

### 4. Connect Them

Update `frontend/.env.production`:

```
NEXT_PUBLIC_API_URL=https://brand-identity-api-XXXXX.run.app
```

Done! ✅

---

## 📊 Comparison: GCP vs Others

| Platform        | Cloud Run | App Engine | Vercel  | Render  |
| --------------- | --------- | ---------- | ------- | ------- |
| **Frontend**    | Yes       | Firebase   | ⭐ Best | Free    |
| **Backend**     | ⭐ Best   | Yes        | No      | Free    |
| **Cost**        | $10-50    | $20-100    | $20-100 | $0-30   |
| **Setup**       | 20 min    | 25 min     | 15 min  | 15 min  |
| **Scalability** | Excellent | Good       | Good    | Limited |

---

## 📁 What We've Added

New files created for Google Cloud support:

```
backend/
  ├── Dockerfile              ← Docker image for Cloud Run
  ├── app.yaml               ← App Engine config (alternative)
  └── .dockerignore          ← Build optimization

frontend/
  ├── Dockerfile            ← Production Docker image
  ├── .dockerignore        ← Build optimization
  └── .env.production      ← Environment config

root/
  ├── GOOGLE_CLOUD_DEPLOYMENT.md    ← Full GCP guide (380+ lines)
  ├── GCP_ENV_CONFIG.md             ← Configuration reference
  ├── deploy-gcp.sh                 ← Automated deployment (Unix)
  ├── deploy-gcp.bat               ← Automated deployment (Windows)
  └── firebase.json                 ← Firebase config
```

---

## 🔧 Three GCP Options

### Option 1: Cloud Run (Recommended) ⭐

**Best for**: Startups, MVPs, variable traffic

```bash
# 20-30 minute setup
Backend:  Cloud Run (pay-per-request)
Frontend: Firebase Hosting (free)
Cost:     $0-50/month
```

**[Full Guide: See GOOGLE_CLOUD_DEPLOYMENT.md - Option 1](./GOOGLE_CLOUD_DEPLOYMENT.md)**

### Option 2: App Engine

**Best for**: Traditional apps, more control

```bash
# 25-40 minute setup
Backend:  App Engine Standard
Frontend: Firebase Hosting
Cost:     $20-100/month
```

**[Full Guide: See GOOGLE_CLOUD_DEPLOYMENT.md - Option 2](./GOOGLE_CLOUD_DEPLOYMENT.md)**

### Option 3: Kubernetes (GKE)

**Best for**: Enterprise, complex deployments

```bash
# 60+ minute setup
Backend:  Kubernetes cluster
Frontend: Cloud Armor
Cost:     $70+/month
```

**[Full Guide: See GOOGLE_CLOUD_DEPLOYMENT.md - Option 3](./GOOGLE_CLOUD_DEPLOYMENT.md)**

---

## 🎯 Quick Start for GCP

### Automated Deployment (Recommended)

**Windows:**

```bash
.\deploy-gcp.bat
# Enter project ID and API keys
# Everything else is automated
```

**macOS/Linux:**

```bash
bash deploy-gcp.sh
# Enter project ID and API keys
# Everything else is automated
```

### Manual Deployment

See **GOOGLE_CLOUD_DEPLOYMENT.md** for complete instructions.

---

## 💰 Pricing Estimate

### Free Tier (1,000 requests/month)

- Backend: $0 (within free tier)
- Frontend: $0 (within free tier)
- **Total: FREE**

### Small Scale (10,000 requests/month)

- Backend: $1-2
- Frontend: $0
- **Total: $1-2/month**

### Medium Scale (100,000 requests/month)

- Backend: $10-20
- Frontend: $1-5
- **Total: $11-25/month**

**See GOOGLE_CLOUD_DEPLOYMENT.md for detailed cost breakdown**

---

## 🔑 What You Need

### Required

- Google Cloud account (free, $300 credit)
- Together AI API key (free tier available)
- gcloud CLI (free)
- Docker (free, optional for manual setup)

### Optional

- Custom domain
- Cloud CDN
- PostgreSQL database
- Redis cache

---

## 📚 Resources

### Complete Guide

- **[GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)** - 380+ lines, complete step-by-step

### Configuration

- **[GCP_ENV_CONFIG.md](./GCP_ENV_CONFIG.md)** - Environment variables reference

### Automated Scripts

- **[deploy-gcp.bat](./deploy-gcp.bat)** - One-click Windows deployment
- **[deploy-gcp.sh](./deploy-gcp.sh)** - One-click Unix deployment

### Official Docs

- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Firebase Hosting](https://firebase.google.com/docs/hosting)
- [gcloud CLI](https://cloud.google.com/sdk/gcloud/reference)

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Backend responds to `/health` endpoint
- [ ] Frontend loads in browser
- [ ] Form submission works
- [ ] Results display correctly
- [ ] View logs: `gcloud run logs read brand-identity-api`
- [ ] Monitor metrics in Cloud Console

---

## 🆘 Troubleshooting

### Cloud Run won't start

```bash
# Check logs
gcloud run logs read brand-identity-api --limit 100

# Common fixes:
# 1. Environment variable TOGETHER_API_KEY missing
# 2. Docker image build failed
# 3. Port not exposed correctly
```

### CORS errors

Update `backend/main.py` to include frontend domain:

```python
ALLOWED_ORIGINS=[
    "https://YOUR-FRONTEND-URL.firebaseapp.com",
    "https://your-custom-domain.com"
]
```

### High latency

Set minimum instances:

```bash
gcloud run update brand-identity-api \
  --min-instances 1 \
  --region us-central1
```

**More: See GOOGLE_CLOUD_DEPLOYMENT.md Troubleshooting section**

---

## 🚀 Next Steps

1. **[Read GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)** (10 min)
2. **Create GCP account** (2 min) - https://console.cloud.google.com
3. **Get API keys** (5 min) - https://www.together.ai/
4. **Run automated script** (15 min) - `deploy-gcp.bat` or `deploy-gcp.sh`
5. **Test in production** (5 min)
6. **Configure domain** (optional, 10 min)

**Total Time: 30-45 minutes to production**

---

## 💡 Pro Tips

### Keep costs low

- Start with free tier (Cloud Run + Firebase)
- Monitor usage in Cloud Console
- Set up billing alerts
- Use auto-scaling (already configured)

### Improve performance

- Enable Cloud CDN for static assets
- Use regional databases near users
- Implement caching (Redis)
- Use Cloud Tasks for async jobs

### Monitor in production

```bash
# View logs
gcloud run logs read brand-identity-api --follow

# View metrics
# Dashboard: https://console.cloud.google.com/monitoring

# Set alerts
# Docs: GOOGLE_CLOUD_DEPLOYMENT.md - Monitoring section
```

---

## 🎓 Learning Resources

- **Deployment**: Complete guide with screenshots in GOOGLE_CLOUD_DEPLOYMENT.md
- **Architecture**: See ARCHITECTURE.md for system design
- **Code**: See relevant sections in backend/ and frontend/ directories
- **Official**: https://cloud.google.com/docs

---

## Support

For issues:

1. Check GOOGLE_CLOUD_DEPLOYMENT.md Troubleshooting section
2. View logs: `gcloud run logs read brand-identity-api`
3. Check Cloud Console: console.cloud.google.com
4. See official docs linked in GOOGLE_CLOUD_DEPLOYMENT.md

---

**Status**: ✅ Ready to deploy to Google Cloud

**Recommendation**: Use Cloud Run (Option 1) for best cost/performance ratio
