# ☁️ Google Cloud Deployment - PowerShell Quick Fix

## ⚠️ Build Failed: "No main.py found"

The error was:
```
failed to build: Python, provide a main.py or app.py file or set an entrypoint
```

**Reason**: You deployed from the project root, but `main.py` is in the `backend/` folder.

---

## ✅ Fix: Deploy from backend folder

### Correct Steps:

```powershell
# Navigate to backend folder FIRST
cd backend

# Then deploy
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=your-key-here `
  --memory 1Gi
```

**Key**: The `--source .` means "current directory", so you must be IN the backend folder.

---

## 🚀 Try Again (Complete Steps)

```powershell
# Step 1: Navigate to backend
cd C:\brand_identity_generator_mvp\backend

# Step 2: Deploy
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=your-actual-key-here `
  --memory 1Gi `
  --timeout 300
```

**Wait**: The build will take 2-5 minutes.

---

## 🔑 Important: Replace `your-actual-key-here`

Get your Together AI API key:

1. Go to: https://www.together.ai/
2. Sign up or login
3. Click "API" in settings
4. Copy your API key (looks like: `sk_xxxxx...`)
5. Replace in command above

---

## ✅ Verify Deployment

Once deployment succeeds, you'll see:

```
✓ Service [brand-identity-api] revision [brand-identity-api-xxxxxxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://brand-identity-api-xxxxx.run.app
```

### Test it works:

```powershell
# Copy your Service URL from above, then:
Invoke-WebRequest "https://brand-identity-api-xxxxx.run.app/health"

# Should return: {"status": "ok"}
```

---

## 📝 Full OneLiners

If you prefer everything in one command:

**PowerShell - Single Command**:
```powershell
cd backend; gcloud run deploy brand-identity-api --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars TOGETHER_API_KEY=your-key --memory 1Gi --timeout 300
```

**PowerShell - Multi-line with backticks**:
```powershell
cd backend
gcloud run deploy brand-identity-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TOGETHER_API_KEY=your-key `
  --memory 1Gi `
  --timeout 300
```

---

## 🆘 If It Still Fails

Check:

1. **Are you in the backend folder?**
   ```powershell
   pwd  # Should show: ...brand_identity_generator_mvp\backend
   ls   # Should show: main.py, Dockerfile, requirements.txt
   ```

2. **Is main.py there?**
   ```powershell
   Get-Item main.py
   ```

3. **View latest build logs**:
   ```powershell
   gcloud builds log --region us-central1 --limit 1
   ```

---

## 📖 Next Steps After Success

Once the backend deploys successfully:

1. **Get the URL**: Shown after deployment (e.g., `https://brand-identity-api-xxxxx.run.app`)

2. **Deploy Frontend**:
   ```powershell
   cd ../frontend
   npm run build
   firebase deploy --only hosting
   ```

3. **Connect them**: Update frontend `.env.production`:
   ```
   NEXT_PUBLIC_API_URL=https://brand-identity-api-xxxxx.run.app
   ```

4. **Test**: Open Firebase-provided URL

---

## 💡 Key Takeaway

**Always navigate to the correct folder before deploying**:

- Deploy backend from `backend/` folder
- Deploy frontend from `frontend/` folder
- Use `cd` to navigate first
- Then use `--source .`

---

**Status**: Ready to retry deployment  
**Next**: Navigate to backend folder and run deploy command above
