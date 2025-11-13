@echo off
REM Google Cloud Platform Deployment Script
REM Deploys Brand Identity Generator to Google Cloud Run + Firebase Hosting

setlocal enabledelayedexpansion

echo ================================
echo Brand Identity Generator
echo Google Cloud Deployment
echo ================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where gcloud >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: gcloud CLI not found. Install from:
    echo https://cloud.google.com/sdk/docs/install
    exit /b 1
)

where firebase >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Firebase CLI not found. Install with:
    echo npm install -g firebase-tools
    exit /b 1
)

where docker >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Docker not found. Install from:
    echo https://www.docker.com/products/docker-desktop
    exit /b 1
)

echo OK - All tools found
echo.

REM Get project ID
set /p PROJECT_ID="Enter your Google Cloud Project ID: "

if "!PROJECT_ID!"=="" (
    echo ERROR: Project ID is required
    exit /b 1
)

echo.
echo Setting up project: !PROJECT_ID!

REM Set project
call gcloud config set project !PROJECT_ID!

REM Enable required APIs
echo.
echo Enabling required APIs...
call gcloud services enable run.googleapis.com
call gcloud services enable containerregistry.googleapis.com
call gcloud services enable firebasehosting.googleapis.com

REM Get API keys
echo.
set /p TOGETHER_API_KEY="Enter your Together AI API Key: "

if "!TOGETHER_API_KEY!"=="" (
    echo ERROR: Together AI API Key is required
    exit /b 1
)

echo.
set /p COHERE_API_KEY="Enter your Cohere API Key (optional, press Enter to skip): "

REM Deploy Backend
echo.
echo ================================
echo Deploying Backend to Cloud Run
echo ================================
echo.

cd backend

echo Deploying brand-identity-api...
call gcloud run deploy brand-identity-api ^
    --source . ^
    --platform managed ^
    --region us-central1 ^
    --allow-unauthenticated ^
    --set-env-vars TOGETHER_API_KEY=!TOGETHER_API_KEY!,COHERE_API_KEY=!COHERE_API_KEY!,ENVIRONMENT=production,DEBUG=false ^
    --memory 1Gi ^
    --cpu 1 ^
    --timeout 300 ^
    --max-instances 100 ^
    --min-instances 0

for /f "delims=" %%i in ('gcloud run services describe brand-identity-api --platform managed --region us-central1 --format="value(status.url)"') do set BACKEND_URL=%%i

echo.
echo OK - Backend deployed successfully!
echo URL: !BACKEND_URL!
echo.

REM Update frontend config
cd ..\frontend

echo Updating frontend configuration...

(
echo NEXT_PUBLIC_API_URL=!BACKEND_URL!
) > .env.production

echo OK - Frontend configuration updated
echo.

REM Build frontend
echo ================================
echo Building Frontend
echo ================================
echo.

echo Installing dependencies...
call npm ci

echo Building Next.js app...
call npm run build

REM Deploy Frontend
echo.
echo ================================
echo Deploying Frontend to Firebase
echo ================================
echo.

call firebase login

echo Deploying to Firebase Hosting...
call firebase deploy --only hosting

echo.
echo ================================
echo OK - Deployment Complete!
echo ================================
echo.
echo Backend URL: !BACKEND_URL!
echo Backend Health: !BACKEND_URL!/health
echo Backend Docs: !BACKEND_URL!/docs
echo.
echo Next steps:
echo 1. Wait 2-3 minutes for Firebase deployment to complete
echo 2. Check the Firebase console for your frontend URL
echo 3. Test the application
echo 4. Configure custom domain (optional)
echo.
echo Documentation:
echo - Setup: See GOOGLE_CLOUD_DEPLOYMENT.md
echo - Monitoring: gcloud run logs read brand-identity-api
echo - Update env vars: gcloud run update brand-identity-api --set-env-vars KEY=VALUE
echo.
