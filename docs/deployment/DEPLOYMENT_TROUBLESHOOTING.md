# 🔧 PowerShell Deployment - What Went Wrong & How to Fix

## Summary of Issue

You successfully ran the `gcloud run deploy` command, but it **failed because**:

```
Python - Missing Entrypoint Error:
"failed to build: for Python, provide a main.py or app.py file"
```

**Reason**: The deployment was from the project **root** directory, not the **backend** directory where `main.py` is located.

---

## ✅ The Fix

### Step 1: Navigate to backend folder

```powershell
cd C:\brand_identity_generator_mvp\backend
```

Verify you're in the right place:

```powershell
pwd  # Should show: ...brand_identity_generator_mvp\backend
ls   # Should show: main.py, Dockerfile, requirements.txt, etc.
```

### Step 2: Get Your Together AI API Key

1. Go to: https://www.together.ai/
2. Sign in (or create account - free tier available)
3. Navigate to API section
4. Copy your API key (format: `sk_xxxxxxxxxxxxx`)

### Step 3: Deploy from backend folder

```powershell
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=sk_your_actual_key_here `
  --memory 1Gi `
  --timeout 300 `
  --max-instances 100
```

**Replace**: `sk_your_actual_key_here` with your actual key from Together.ai

---

## 🎯 Single Command (Fastest)

If you want to copy-paste one line:

```powershell
cd C:\brand_identity_generator_mvp\backend; gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=sk_your_key_here --memory 1Gi --timeout 300
```

Replace `sk_your_key_here` with your actual Together AI API key.

---

## ⏱️ What to Expect

After running the command:

1. **Build starts** (~30 seconds)
   ```
   Building using Buildpacks and deploying container to Cloud Run...
   Building Container.
   ```

2. **Creating repository** (~1 minute)
   ```
   OK Creating Container Repository...
   ```

3. **Build container** (~2-3 minutes)
   ```
   Building Container... 
   Logs are available at: https://console.cloud.google.com/...
   ```

4. **Deploy service** (~1 minute)
   ```
   Creating Revision...
   Routing traffic...
   Setting IAM Policy...
   ```

5. **Success!** You'll see:
   ```
   Service [brand-identity-api] revision [brand-identity-api-xxxxx] has been deployed
   Service URL: https://brand-identity-api-xxxxx.run.app
   ```

**Total time**: 5-8 minutes

---

## ✅ After Successful Deployment

### 1. Save Your Backend URL

You'll see something like:
```
Service URL: https://brand-identity-api-xxxxx.run.app
```

**Copy this URL** - you'll need it for the frontend.

### 2. Test the Backend

```powershell
# Replace with your actual URL
curl https://brand-identity-api-xxxxx.run.app/health

# Or use PowerShell:
Invoke-WebRequest https://brand-identity-api-xxxxx.run.app/health
```

Should return:
```json
{"status": "ok"}
```

### 3. View Logs

```powershell
# View recent logs
gcloud run logs read brand-identity-api --limit 20

# Watch live logs
gcloud run logs read brand-identity-api --follow
```

### 4. Deploy Frontend

```powershell
# Navigate to frontend folder
cd C:\brand_identity_generator_mvp\frontend

# Update environment
"NEXT_PUBLIC_API_URL=https://brand-identity-api-xxxxx.run.app" | Set-Content .env.production

# Build
npm run build

# Deploy to Firebase
firebase deploy --only hosting
```

---

## 🆘 If It Still Fails

### Check 1: Verify folder contents

```powershell
cd C:\brand_identity_generator_mvp\backend
ls -Name  # Should list: main.py, Dockerfile, requirements.txt, schemas.py, etc.
```

### Check 2: Verify main.py syntax

```powershell
python main.py --help  # Should work without errors
```

### Check 3: Check build logs

```powershell
gcloud builds list --region us-central1 --limit 1
# Find the build ID, then:
gcloud builds log BUILD_ID --region us-central1 | Select-Object -Last 50
```

### Check 4: Verify API key format

Together AI keys should start with `sk_`
```
✓ Correct: sk_12345abcde...
✗ Wrong: (empty, "your-key", etc.)
```

---

## 📝 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No main.py" error | Deploying from wrong folder | `cd backend` first |
| Build timeout | Dependencies too large | Reduce to essential packages |
| Authentication fails | Not logged in | `gcloud auth login` |
| API key error | Wrong key format | Use key starting with `sk_` |
| CORS errors | Frontend trying to reach backend | Update `.env.production` with correct URL |

---

## 🎯 Complete Deployment Flow

```powershell
# 1. Navigate to backend
cd C:\brand_identity_generator_mvp\backend

# 2. Deploy backend
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=sk_your_key `
  --memory 1Gi `
  --timeout 300

# 3. Wait for deployment to complete (5-8 min)
# You'll see: Service URL: https://brand-identity-api-xxxxx.run.app

# 4. Save the URL, then navigate to frontend
cd ../frontend

# 5. Update environment
"NEXT_PUBLIC_API_URL=https://brand-identity-api-xxxxx.run.app" | Set-Content .env.production

# 6. Build frontend
npm run build

# 7. Deploy frontend
firebase deploy --only hosting

# 8. Done! Frontend URL will be displayed
```

---

## 💡 Key Learnings

### PowerShell Syntax

- ✅ Use backticks (`) for line continuation
- ❌ Don't use backslashes (\) like in bash
- ✅ Use `Set-Content` for writing files
- ❌ Don't use `echo` or `>` redirects

### Folder Structure

- **Deploy from `backend/`** when using `--source .`
- **Deploy from `frontend/`** for Firebase
- Always check your location: `pwd`

### Google Cloud

- Build takes 5-8 minutes first time
- Redeployments are faster (2-3 min)
- You can deploy multiple versions
- Watch logs: `gcloud run logs read SERVICE_NAME --follow`

---

## 📊 Deployment Timeline

```
Now:           Read this guide (5 min)
+5 min:        Get API key from Together.ai
+13 min:       Run deploy command (waiting for build)
+18 min:       Backend ready, copy URL
+25 min:       Deploy frontend
+35 min:       Both live in production! 🎉
```

**Total time**: ~35 minutes (most is waiting for build)

---

## 🚀 Ready?

1. **Have you created a Together.ai account?** https://www.together.ai/
2. **Do you have your API key?** (looks like: `sk_...`)
3. **Ready to deploy?** Run:

```powershell
cd C:\brand_identity_generator_mvp\backend

gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=sk_your_key_here `
  --memory 1Gi `
  --timeout 300
```

**Replace `sk_your_key_here` with your actual key**, then press Enter!

---

## 📞 Additional Resources

- **PowerShell Guide**: See `POWERSHELL_DEPLOYMENT_GUIDE.md`
- **Full GCP Guide**: See `GOOGLE_CLOUD_DEPLOYMENT.md`
- **Together.ai Docs**: https://www.together.ai/docs
- **Google Cloud Docs**: https://cloud.google.com/docs

---

**Status**: ✅ Ready to deploy  
**Next Step**: Get Together AI key, then run deploy command  
**Expected Result**: Service URL for your backend API
