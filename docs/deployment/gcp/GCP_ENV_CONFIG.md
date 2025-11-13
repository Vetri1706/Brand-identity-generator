# Google Cloud Deployment Configuration

## Environment Variables for Backend

Set these in Cloud Run Console or via gcloud CLI:

### Required

```bash
# LLM API Keys
TOGETHER_API_KEY=<your-key-from-together.ai>
COHERE_API_KEY=<your-key-from-cohere.com>  # Optional fallback

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Application Configuration

```bash
# LLM Settings
LLM_PROVIDER=together
LLM_MODEL=meta-llama/Llama-2-7b-hf
MAX_TOKENS=500
TEMPERATURE=0.7
```

### Optional (Future)

```bash
# Database (when ready)
DATABASE_URL=postgresql://user:pass@host/dbname

# Redis (when ready)
REDIS_URL=redis://host:port

# Monitoring
SENTRY_DSN=<your-sentry-dsn>
```

## Frontend Configuration

Set in `frontend/.env.production`:

```bash
NEXT_PUBLIC_API_URL=https://brand-identity-api-XXXXX.run.app
```

## Cloud Run Deployment Command

```bash
# From backend directory
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
```

## Firebase Deployment Command

```bash
# From frontend directory
npm run build
firebase deploy --only hosting
```
