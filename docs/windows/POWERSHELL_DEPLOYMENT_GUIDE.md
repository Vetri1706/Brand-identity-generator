# 🚀 Google Cloud Deployment - PowerShell Guide

## ⚠️ Important: PowerShell vs Bash Syntax

If you're using **PowerShell** (Windows command line), you need to format the `gcloud` commands differently than bash scripts show.

---

## ✅ Correct PowerShell Syntax

### Single Line Command (Easiest)

Instead of multi-line bash format, use a single line in PowerShell:

```powershell
gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=your-key-here,COHERE_API_KEY=optional --memory 1Gi
```

### Step-by-Step Deployment

```powershell
# Step 1: Navigate to backend
cd backend

# Step 2: Deploy (single line)
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=your-key-here,COHERE_API_KEY=optional `
  --memory 1Gi
```

**Note**: In PowerShell, use backticks (`) at the end of lines to continue to the next line, NOT backslashes.

---

## 🔧 If Build Failed

### Check Build Logs

```powershell
# View recent build logs
gcloud builds log --region=us-central1 --limit=50
```

### Common Issues & Solutions

#### Issue 1: Missing PORT Environment Variable

**Error**: "Application failed to start"

**Solution**: Cloud Run needs the app to listen on the correct port.

Update `backend/main.py` to use port from environment:

```python
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
```

#### Issue 2: Python Dependencies Too Large

**Error**: "Build failed" or "timeout"

**Solution**: Cloud Run has build time limits. Simplify dependencies:

```bash
# Remove heavy packages if not used
# torch, transformers can be 2GB+
```

#### Issue 3: Dockerfile Issues

**Solution**: Use Cloud Run's Buildpacks instead:

```powershell
# Let Cloud Run auto-detect and build
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --runtime python311 `
  --entry-point "uvicorn main:app --host 0.0.0.0 --port 8000" `
  --memory 1Gi
```

---

## 📋 Prerequisites Check

Before deploying, verify:

```powershell
# Check 1: gcloud is installed and authenticated
gcloud auth list

# Check 2: APIs are enabled
gcloud services list --enabled | findstr "run.googleapis.com"

# Check 3: Requirements.txt has correct packages
cat backend/requirements.txt

# Check 4: main.py exists and has Flask/FastAPI app
cat backend/main.py | head -20
```

---

## 🎯 PowerShell-Specific Deployment Script

Create `deploy-gcp-powershell.ps1`:

```powershell
# Google Cloud Deployment Script for PowerShell

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Google Cloud Deployment" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: gcloud CLI not found" -ForegroundColor Red
    Write-Host "Download from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

Write-Host "OK - gcloud found" -ForegroundColor Green
Write-Host ""

# Get project ID
$projectId = Read-Host "Enter your Google Cloud Project ID"

if ([string]::IsNullOrEmpty($projectId)) {
    Write-Host "ERROR: Project ID is required" -ForegroundColor Red
    exit 1
}

Write-Host "Setting project to: $projectId" -ForegroundColor Yellow
gcloud config set project $projectId

# Get API keys
$togetherKey = Read-Host "Enter your Together AI API Key"
if ([string]::IsNullOrEmpty($togetherKey)) {
    Write-Host "ERROR: Together AI API Key is required" -ForegroundColor Red
    exit 1
}

$cohereKey = Read-Host "Enter your Cohere API Key (optional, press Enter to skip)"

# Enable APIs
Write-Host ""
Write-Host "Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable firebasehosting.googleapis.com

# Deploy backend
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Deploying Backend to Cloud Run" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

cd backend

Write-Host "Deploying brand-identity-api..." -ForegroundColor Yellow

if ([string]::IsNullOrEmpty($cohereKey)) {
    gcloud run deploy brand-identity-api `
      --source . `
      --platform managed `
      --region us-central1 `
      --allow-unauthenticated `
      --set-env-vars TOGETHER_API_KEY=$togetherKey,ENVIRONMENT=production,DEBUG=false `
      --memory 1Gi `
      --cpu 1 `
      --timeout 300 `
      --max-instances 100 `
      --min-instances 0
} else {
    gcloud run deploy brand-identity-api `
      --source . `
      --platform managed `
      --region us-central1 `
      --allow-unauthenticated `
      --set-env-vars TOGETHER_API_KEY=$togetherKey,COHERE_API_KEY=$cohereKey,ENVIRONMENT=production,DEBUG=false `
      --memory 1Gi `
      --cpu 1 `
      --timeout 300 `
      --max-instances 100 `
      --min-instances 0
}

# Get backend URL
$backendUrl = gcloud run services describe brand-identity-api `
  --platform managed `
  --region us-central1 `
  --format="value(status.url)"

Write-Host ""
Write-Host "OK - Backend deployed!" -ForegroundColor Green
Write-Host "Backend URL: $backendUrl" -ForegroundColor Cyan
Write-Host ""

# Update frontend config
cd ..\frontend

Write-Host "Updating frontend configuration..." -ForegroundColor Yellow
$envContent = "NEXT_PUBLIC_API_URL=$backendUrl"
Set-Content -Path ".env.production" -Value $envContent

Write-Host "OK - Frontend updated" -ForegroundColor Green
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "1. Build frontend: npm run build" -ForegroundColor Yellow
Write-Host "2. Deploy frontend: firebase deploy --only hosting" -ForegroundColor Yellow
Write-Host "3. View backend logs: gcloud run logs read brand-identity-api" -ForegroundColor Yellow
Write-Host "4. Test at frontend URL" -ForegroundColor Yellow
```

---

## 🚀 Quick Start - Choose One

### Option A: One-Line Deployment (Fastest)

```powershell
gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=your-key-here --memory 1Gi
```

### Option B: Step-by-Step PowerShell

```powershell
# 1. Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Enable APIs
gcloud services enable run.googleapis.com firebasehosting.googleapis.com

# 3. Deploy backend (navigate to backend folder first)
cd backend
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=your-key `
  --memory 1Gi

# 4. Get the URL
$backendUrl = gcloud run services describe brand-identity-api --platform managed --region us-central1 --format="value(status.url)"
Write-Host "Backend URL: $backendUrl"

# 5. Deploy frontend
cd ../frontend
npm run build
firebase deploy --only hosting
```

### Option C: PowerShell Script

```powershell
# Save as deploy.ps1, then run:
.\deploy.ps1
```

(See full script above)

---

## 🆘 Troubleshooting in PowerShell

### Check if gcloud is working

```powershell
gcloud --version
gcloud auth list
gcloud config get project
```

### View deployment logs

```powershell
# Real-time logs
gcloud run logs read brand-identity-api --follow

# Last 50 lines
gcloud run logs read brand-identity-api --limit 50

# Errors only
gcloud run logs read brand-identity-api --limit 50 | findstr "ERROR"
```

### View build logs

```powershell
# Find your build
gcloud builds list --region us-central1

# View specific build
gcloud builds log BUILD_ID --region us-central1
```

### Test your deployment

```powershell
# Get service URL
$url = gcloud run services describe brand-identity-api --platform managed --region us-central1 --format="value(status.url)"

# Test health endpoint
curl "$url/health"

# Test with parameter
Invoke-WebRequest "$url/health"
```

---

## 📊 Environment Variables

Make sure to replace placeholders:

```powershell
# Before:
--set-env-vars TOGETHER_API_KEY=your-key-here

# After:
--set-env-vars TOGETHER_API_KEY=sk_xxxxxxxxxxxxx
```

Get your Together AI key from: https://www.together.ai/

---

## 🎯 Common PowerShell Issues

### Issue: Command continues to next line unexpectedly

**Cause**: Backslash `\` instead of backtick `` ` ``

**Solution**: Use PowerShell backtick for line continuation
```powershell
# Wrong:
gcloud run deploy brand-identity-api \
  --source .

# Correct:
gcloud run deploy brand-identity-api `
  --source .
```

### Issue: "Unexpected token" errors

**Cause**: Copying bash commands directly into PowerShell

**Solution**: Use single-line format or proper backtick syntax

### Issue: Special characters in API keys

**Cause**: PowerShell interprets special characters

**Solution**: Use single quotes for API keys
```powershell
--set-env-vars TOGETHER_API_KEY='your-key-with-$pecial-chars'
```

---

## ✅ Verification

After deployment:

```powershell
# 1. Check service exists
gcloud run services describe brand-identity-api --platform managed --region us-central1

# 2. Check environment variables
gcloud run services describe brand-identity-api --platform managed --region us-central1 --format=json | ConvertFrom-Json | Select-Object -ExpandProperty spec

# 3. Test endpoint
$url = gcloud run services describe brand-identity-api --platform managed --region us-central1 --format="value(status.url)"
Invoke-WebRequest "$url/health"

# 4. View recent logs
gcloud run logs read brand-identity-api --limit 20
```

---

## 📞 Next Steps

1. **Set your API key**: Replace `your-key-here` with actual key
2. **Run deployment**: Copy one-liner or use PowerShell script
3. **Wait 2-5 minutes**: Build and deployment
4. **Check logs**: Use `gcloud run logs read`
5. **Deploy frontend**: After backend is ready

---

## 💡 Pro Tips for PowerShell Users

### Save commands as variables

```powershell
$projectId = "my-project"
$apiKey = "sk_xxx"
$backendUrl = gcloud run services describe brand-identity-api --platform managed --region us-central1 --format="value(status.url)"
```

### Create reusable functions

```powershell
function Deploy-ToCloudRun {
    param(
        [string]$ServiceName,
        [string]$ProjectId,
        [string]$ApiKey
    )
    
    gcloud config set project $ProjectId
    
    gcloud run deploy $ServiceName `
      --source . `
      --platform managed `
      --region us-central1 `
      --allow-unauthenticated `
      --set-env-vars TOGETHER_API_KEY=$ApiKey
}

# Usage:
Deploy-ToCloudRun -ServiceName "brand-identity-api" -ProjectId "my-project" -ApiKey "sk_xxx"
```

### Monitor in real-time

```powershell
# Watch logs in real-time
gcloud run logs read brand-identity-api --follow
```

---

**Status**: ✅ Ready to deploy using PowerShell

**Key Difference**: Use backticks (`) not backslashes (\) for line continuation in PowerShell
