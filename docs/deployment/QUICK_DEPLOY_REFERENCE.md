# 📍 Deployment Quick Reference - PowerShell

## Problem Identified ✅

**Error**: Build failed - "No main.py found"  
**Cause**: Deployed from project root instead of backend folder  
**Solution**: Navigate to backend folder before deploying

---

## Solution: 3 Simple Steps

### ✅ Step 1: Navigate to Backend

```powershell
cd C:\brand_identity_generator_mvp\backend
```

Verify:
```powershell
pwd     # Check location
ls      # Verify main.py exists
```

### ✅ Step 2: Get API Key

1. Go to: https://www.together.ai/
2. Create free account
3. Get API Key (starts with `sk_`)
4. Copy it

### ✅ Step 3: Deploy

**Single line** (copy-paste):
```powershell
gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=sk_your_actual_key --memory 1Gi --timeout 300
```

**Multi-line** (easier to read):
```powershell
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=sk_your_actual_key `
  --memory 1Gi `
  --timeout 300
```

**Important**: Replace `sk_your_actual_key` with your real key!

---

## What to Expect

```
Building Container...          (2-3 minutes)
Creating Revision...            (1 minute)
Routing traffic...              (1 minute)

✓ Deployment successful!
Service URL: https://brand-identity-api-xxxxx.run.app
```

**Total time**: 5-8 minutes

---

## After Deployment ✅

### 1. Save Your Backend URL
```
https://brand-identity-api-xxxxx.run.app
```

### 2. Test It
```powershell
Invoke-WebRequest https://brand-identity-api-xxxxx.run.app/health
```

Should return:
```json
{"status": "ok"}
```

### 3. Deploy Frontend
```powershell
cd ../frontend
npm run build
firebase deploy --only hosting
```

### 4. Connect Them
Update `frontend/.env.production`:
```
NEXT_PUBLIC_API_URL=https://brand-identity-api-xxxxx.run.app
```

---

## Troubleshooting

### If build fails again

```powershell
# View logs
gcloud run logs read brand-identity-api --limit 50

# View build logs
gcloud builds list --region us-central1 --limit 1
gcloud builds log BUILD_ID --region us-central1
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "No main.py" | Navigate to backend folder first |
| API key error | Use actual key, starts with `sk_` |
| Build timeout | Wait 5-8 min, check logs |
| CORS errors | Update frontend `.env.production` |

---

## Key Commands

```powershell
# Check location
pwd

# List files (verify main.py exists)
ls

# Navigate to backend
cd backend

# Deploy
gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=sk_your_key --memory 1Gi

# View logs
gcloud run logs read brand-identity-api --follow

# Get service URL
gcloud run services describe brand-identity-api --platform managed --region us-central1 --format="value(status.url)"

# Test endpoint
Invoke-WebRequest https://your-service-url/health
```

---

## 📝 Full Documentation

For more details, see:
- `DEPLOYMENT_TROUBLESHOOTING.md` - Complete troubleshooting
- `POWERSHELL_DEPLOYMENT_GUIDE.md` - PowerShell specific guide
- `GOOGLE_CLOUD_DEPLOYMENT.md` - Full GCP guide

---

## ✅ You're Ready!

**Next**: Run the deploy command from backend folder!

```powershell
cd C:\brand_identity_generator_mvp\backend
gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=sk_your_key --memory 1Gi --timeout 300
```
