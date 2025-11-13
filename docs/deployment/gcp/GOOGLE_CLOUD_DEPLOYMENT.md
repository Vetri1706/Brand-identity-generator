# 🚀 Google Cloud Platform Deployment Guide

## Overview

Three Google Cloud deployment options tailored to your needs and budget.

---

## Quick Comparison

| Option                      | Frontend              | Backend    | Cost/Month | Setup Time | Scalability |
| --------------------------- | --------------------- | ---------- | ---------- | ---------- | ----------- |
| **Cloud Run (Recommended)** | Cloud Run or Firebase | Cloud Run  | $10-50     | 20 min     | Excellent   |
| **App Engine**              | Firebase Hosting      | App Engine | $20-100    | 25 min     | Good        |
| **Kubernetes (GKE)**        | Cloud Armor + Compute | Cloud Run  | $70+       | 60+ min    | Advanced    |

---

## Option 1: Cloud Run (Recommended for MVP) ⭐

**Cost**: $10-50/month  
**Setup Time**: 20-30 minutes  
**Best For**: Startups, MVPs, variable traffic

### Why Cloud Run?

- ✅ Auto-scales from 0 to thousands
- ✅ Pay only for compute time used
- ✅ No infrastructure management
- ✅ Built-in monitoring and logging
- ✅ Free tier: 2M requests/month
- ✅ Simple deployment from GitHub or Docker

### Architecture

```
┌─────────────────────────────────────────────┐
│         Firebase Hosting (Frontend)         │
│ - Auto-deploys from GitHub                  │
│ - Global CDN                                │
│ - SSL certificates                          │
│ - Free tier: 1GB storage, 10GB bandwidth    │
└────────────────┬────────────────────────────┘
                 │ HTTPS/REST
┌────────────────▼────────────────────────────┐
│      Cloud Run (Backend - FastAPI)          │
│ - Containerized Python app                  │
│ - Auto-scaling (0-100+ instances)           │
│ - Pay per request                           │
│ - Built-in environment variables            │
│ - Cloud Logging integration                 │
└─────────────────────────────────────────────┘
```

### Prerequisites

1. **Google Cloud Account**

   ```bash
   # Go to console.cloud.google.com
   # Create a free account (get $300 credit)
   # Create a new project
   ```

2. **Install gcloud CLI**

   ```bash
   # Windows (PowerShell as Admin)
   # Download from: https://cloud.google.com/sdk/docs/install
   # Or use chocolatey:
   choco install google-cloud-sdk

   # macOS
   brew install --cask google-cloud-sdk

   # Linux
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

3. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project PROJECT_ID
   ```

### Step 1: Prepare Backend for Cloud Run

#### Create Dockerfile

Create `backend/Dockerfile`:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Update backend/.env for Cloud Run

Create `.env.production`:

```env
# Cloud Run Environment
ENVIRONMENT=production
DEBUG=false

# API Keys (set in Cloud Run secrets)
TOGETHER_API_KEY=${TOGETHER_API_KEY}
COHERE_API_KEY=${COHERE_API_KEY}

# CORS - allow Firebase Hosting domain
ALLOWED_ORIGINS=https://YOUR-PROJECT-ID.firebaseapp.com,https://your-custom-domain.com

# Database (optional, for future)
DATABASE_URL=${DATABASE_URL}

# LLM Configuration
LLM_PROVIDER=together
LLM_MODEL=meta-llama/Llama-2-7b-hf
MAX_TOKENS=500
TEMPERATURE=0.7
```

### Step 2: Deploy Backend to Cloud Run

#### Option A: Deploy from Git (Recommended)

```bash
# From project root
cd backend

# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Deploy
gcloud run deploy brand-identity-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TOGETHER_API_KEY=$TOGETHER_API_KEY,COHERE_API_KEY=$COHERE_API_KEY \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 100

# Get service URL
gcloud run services describe brand-identity-api --platform managed --region us-central1
```

#### Option B: Deploy from Docker Hub

```bash
# Build and push to Docker Hub
docker build -t yourusername/brand-identity-api:latest .
docker push yourusername/brand-identity-api:latest

# Deploy from Docker Hub
gcloud run deploy brand-identity-api \
  --image yourusername/brand-identity-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TOGETHER_API_KEY=$TOGETHER_API_KEY \
  --memory 1Gi \
  --timeout 300
```

#### Verify Backend Deployment

```bash
# Test health check
curl https://YOUR-BACKEND-URL/health

# View logs
gcloud run logs read brand-identity-api --platform managed --region us-central1
```

### Step 3: Deploy Frontend to Firebase Hosting

#### Option A: Firebase Hosting (Easiest)

```bash
# Install Firebase CLI
npm install -g firebase-tools

# From frontend directory
cd frontend

# Login
firebase login

# Initialize Firebase
firebase init hosting

# Build frontend
npm run build

# Create firebase.json if not exists
cat > firebase.json << EOF
{
  "hosting": {
    "public": ".next",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
EOF

# Deploy
firebase deploy
```

#### Option B: Cloud Run for Frontend (More control)

Create `frontend/Dockerfile.prod`:

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["npm", "start"]
```

Deploy frontend:

```bash
cd frontend

gcloud run deploy brand-identity-web \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60
```

### Step 4: Connect Frontend to Backend

Update `frontend/.env.production`:

```env
NEXT_PUBLIC_API_URL=https://brand-identity-api-XXXXX.run.app
```

Update `frontend/src/lib/api.ts`:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});
```

### Step 5: Set Up Custom Domain (Optional)

```bash
# 1. Point your domain to Cloud Run
gcloud run domain-mappings create \
  --service=brand-identity-api \
  --domain=api.yourdomain.com \
  --region=us-central1

# 2. Update DNS records
# - Type: A
# - Name: api
# - Value: Get from `gcloud compute addresses describe`

# 3. Similarly for frontend with Firebase
firebase hosting:channel:deploy live
```

### Pricing Estimate

**Backend (Cloud Run)**:

- Requests: $0.40 per 1M requests (free: 2M/month)
- Computing: $0.00002400 per CPU-second (free: 180,000 CPU-seconds/month)
- Memory: $0.00000050 per GB-second

**Example (1,000 requests/month, 40 seconds each)**:

- ~40,000 CPU-seconds = Well within free tier ✅
- Cost: $0/month

**Frontend (Firebase Hosting)**:

- Storage: $0.18 per GB/month (free: 1GB)
- Bandwidth: $0.12 per GB (free: 10GB/month)

**Total Estimated**: $0-15/month

---

## Option 2: App Engine (Traditional Approach)

**Cost**: $20-100/month  
**Setup Time**: 25-40 minutes  
**Best For**: More control, traditional applications

### Backend Deployment

```bash
# Create app.yaml in backend directory
cat > backend/app.yaml << EOF
runtime: python311
env: standard
entrypoint: uvicorn main:app --host 0.0.0.0 --port 8080

env_variables:
  TOGETHER_API_KEY: "${TOGETHER_API_KEY}"
  COHERE_API_KEY: "${COHERE_API_KEY}"

automatic_scaling:
  min_instances: 1
  max_instances: 10

handlers:
- url: /.*
  secure: always
  redirect_http_response_code: 301
  script: auto
EOF

# Deploy
gcloud app deploy
```

### Frontend Deployment

```bash
# Build
cd frontend
npm run build

# Deploy to Firebase Hosting (same as Option 1)
firebase deploy
```

---

## Option 3: Kubernetes (GKE)

**Cost**: $70+ per month  
**Setup Time**: 60+ minutes  
**Best For**: Advanced, high-traffic, complex deployments

### Quick Setup

```bash
# Create GKE cluster
gcloud container clusters create brand-identity-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-1

# Deploy backend
kubectl create deployment brand-api --image=yourusername/brand-identity-api
kubectl expose deployment brand-api --type=LoadBalancer --port=80 --target-port=8000

# Deploy frontend
kubectl create deployment brand-web --image=yourusername/brand-identity-web
kubectl expose deployment brand-web --type=LoadBalancer --port=80 --target-port=3000

# View services
kubectl get services
```

---

## Monitoring & Logging

### Cloud Logging

```bash
# View all logs
gcloud run logs read brand-identity-api --limit 50

# Real-time logs
gcloud run logs read brand-identity-api --follow

# Filter by level
gcloud run logs read brand-identity-api --filter="severity=ERROR"
```

### Cloud Monitoring Dashboard

```bash
# Create a dashboard
gcloud monitoring dashboards create --config-from-file=dashboard.json
```

Example `dashboard.json`:

```json
{
  "displayName": "Brand Identity Generator",
  "dashboardFilters": [],
  "gridLayout": {
    "widgets": [
      {
        "title": "Request Count",
        "xyChart": {
          "dataSets": [
            {
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" metric.type=\"run.googleapis.com/request_count\""
                }
              }
            }
          ]
        }
      },
      {
        "title": "Error Rate",
        "xyChart": {
          "dataSets": [
            {
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" metric.type=\"run.googleapis.com/request_count\" metric.response_code_class=\"5xx\""
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Set Up Alerts

```bash
# Alert on high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Brand API High Error Rate" \
  --condition-display-name="Errors > 10% in 5 min" \
  --condition-threshold-value=0.1 \
  --condition-threshold-duration=300s
```

---

## Comparison: Google Cloud vs. Other Platforms

| Feature            | Google Cloud | AWS        | Azure       | Vercel/Render |
| ------------------ | ------------ | ---------- | ----------- | ------------- |
| **Learning Curve** | Medium       | Hard       | Medium      | Easy          |
| **Cost Control**   | Excellent    | Good       | Good        | Limited       |
| **Auto-scaling**   | Built-in     | Yes        | Yes         | Yes           |
| **Free Tier**      | $300 credit  | Limited    | $200 credit | Limited       |
| **Setup Time**     | 20-30 min    | 30-45 min  | 30-45 min   | 10-15 min     |
| **Best For**       | Startups, ML | Enterprise | Enterprise  | Simple apps   |

---

## Step-by-Step Quick Start

### For Cloud Run (Recommended):

1. **Create Google Cloud Project**

   ```bash
   gcloud projects create brand-identity-mvp
   gcloud config set project brand-identity-mvp
   ```

2. **Enable APIs**

   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable firebasehosting.googleapis.com
   ```

3. **Deploy Backend**

   ```bash
   cd backend
   gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated
   ```

4. **Deploy Frontend**

   ```bash
   cd frontend
   npm run build
   firebase deploy
   ```

5. **Update Configuration**

   - Add backend URL to frontend `.env.production`
   - Test at Firebase-provided URL

6. **Monitor**
   - View logs: `gcloud run logs read brand-identity-api`
   - Visit Cloud Console: `console.cloud.google.com`

---

## Cost Calculator

```
Monthly Estimate (1,000 requests/month, 40s each):

Backend (Cloud Run):
- CPU: 40,000 CPU-seconds / 180,000 free = $0
- Memory: 40GB-seconds / 360,000 free = $0
- Requests: 1,000 / 2M free = $0
Subtotal: $0

Frontend (Firebase):
- Storage: 0.5GB / 1GB free = $0
- Bandwidth: 2GB / 10GB free = $0
Subtotal: $0

Total: FREE (within free tier limits)

With 10,000 requests/month (10x):
Backend: ~$1-2
Frontend: $0
Total: ~$1-2/month
```

---

## Troubleshooting

### Cloud Run Won't Start

```bash
# Check logs
gcloud run logs read brand-identity-api --limit 100

# Common issues:
# 1. Port not 8000/8080
# 2. API key missing in env vars
# 3. Dockerfile issues

# Solution: Add to Dockerfile
ENV PORT=8000
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000
```

### High Latency/Cold Starts

```bash
# Set minimum instances
gcloud run update brand-identity-api \
  --min-instances 1 \
  --region us-central1

# Estimated cost increase: +$10-20/month
```

### CORS Issues

Update backend `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://YOUR-FRONTEND-URL.firebaseapp.com",
        "https://your-custom-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication/Secrets

```bash
# Store API keys in Secret Manager
gcloud secrets create TOGETHER_API_KEY --data-file=- << EOF
your-api-key-here
EOF

# Reference in Cloud Run
gcloud run deploy brand-identity-api \
  --set-env-vars TOGETHER_API_KEY=projects/PROJECT_ID/secrets/TOGETHER_API_KEY/versions/latest
```

---

## Next Steps

1. ✅ Create Google Cloud account (get $300 free credit)
2. ✅ Install gcloud CLI
3. ✅ Deploy backend to Cloud Run (Option 1 recommended)
4. ✅ Deploy frontend to Firebase Hosting
5. ✅ Test end-to-end functionality
6. ✅ Set up monitoring and alerts
7. ✅ Configure custom domain (optional)

---

## Resources

- **Google Cloud Documentation**: https://cloud.google.com/docs
- **Cloud Run**: https://cloud.google.com/run/docs
- **Firebase Hosting**: https://firebase.google.com/docs/hosting
- **gcloud CLI**: https://cloud.google.com/sdk/gcloud/reference
- **Pricing Calculator**: https://cloud.google.com/products/calculator
- **Free Tier Details**: https://cloud.google.com/free

---

## Support

For issues or questions:

- Cloud Run: https://cloud.google.com/run/docs/troubleshooting
- Firebase: https://firebase.google.com/support
- Stack Overflow: tag `google-cloud`
