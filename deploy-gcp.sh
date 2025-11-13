#!/bin/bash
# Google Cloud Platform Deployment Script
# Deploys Brand Identity Generator to Google Cloud Run + Firebase Hosting

set -e

echo "================================"
echo "Brand Identity Generator"
echo "Google Cloud Deployment"
echo "================================"
echo ""

# Check prerequisites
echo "✓ Checking prerequisites..."

if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install from:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Install with:"
    echo "   npm install -g firebase-tools"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install from:"
    echo "   https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ All tools found"
echo ""

# Get project ID
echo "Enter your Google Cloud Project ID:"
read PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID is required"
    exit 1
fi

echo ""
echo "Setting up project: $PROJECT_ID"

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo ""
echo "✓ Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable firebasehosting.googleapis.com

# Get API keys
echo ""
echo "Enter your Together AI API Key (get from https://www.together.ai/):"
read TOGETHER_API_KEY

if [ -z "$TOGETHER_API_KEY" ]; then
    echo "❌ Together AI API Key is required"
    exit 1
fi

echo ""
echo "Enter your Cohere API Key (optional, press Enter to skip):"
read COHERE_API_KEY

# Deploy Backend
echo ""
echo "================================"
echo "Deploying Backend to Cloud Run"
echo "================================"
echo ""

cd backend

echo "✓ Deploying brand-identity-api..."
gcloud run deploy brand-identity-api \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars \
      TOGETHER_API_KEY=$TOGETHER_API_KEY,\
      COHERE_API_KEY=$COHERE_API_KEY,\
      ENVIRONMENT=production,\
      DEBUG=false \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 100 \
    --min-instances 0

BACKEND_URL=$(gcloud run services describe brand-identity-api --platform managed --region us-central1 --format='value(status.url)')
echo ""
echo "✓ Backend deployed successfully!"
echo "  URL: $BACKEND_URL"
echo ""

# Update frontend config
cd ../frontend

echo "Updating frontend configuration..."
cat > .env.production << EOF
NEXT_PUBLIC_API_URL=$BACKEND_URL
EOF

echo "✓ Frontend configuration updated"
echo ""

# Build frontend
echo "================================"
echo "Building Frontend"
echo "================================"
echo ""

echo "✓ Installing dependencies..."
npm ci

echo "✓ Building Next.js app..."
npm run build

# Deploy Frontend
echo ""
echo "================================"
echo "Deploying Frontend to Firebase"
echo "================================"
echo ""

firebase login || true

echo "✓ Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo ""
echo "================================"
echo "✓ Deployment Complete!"
echo "================================"
echo ""
echo "Backend URL: $BACKEND_URL"
echo "Backend Health: $BACKEND_URL/health"
echo "Backend Docs: $BACKEND_URL/docs"
echo ""
echo "Next steps:"
echo "1. Wait 2-3 minutes for Firebase deployment to complete"
echo "2. Check the Firebase console for your frontend URL"
echo "3. Test the application"
echo "4. Configure custom domain (optional)"
echo ""
echo "Documentation:"
echo "- Setup: See GOOGLE_CLOUD_DEPLOYMENT.md"
echo "- Monitoring: gcloud run logs read brand-identity-api"
echo "- Update env vars: gcloud run update brand-identity-api --set-env-vars KEY=VALUE"
echo ""
