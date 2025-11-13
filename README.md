# 🎨 Brand Identity Generator MVP

## Overview

A **production-ready, AI-powered brand identity generation platform** for tech and product companies. Generate unique logos, taglines, color palettes, and brand guidelines in seconds using LLMs.

### ✨ Key Features

- **AI-Powered Generation**: Works with a local free LLM via Ollama by default (no API key), and can also use Together AI or Cohere if configured
- **Multi-Modal Outputs**: Logos, taglines, color palettes, typography, guidelines
- **Multiple Variations**: 3+ creative variations for each asset
- **Company-Specific**: Tailored to different industry types (SaaS, FinTech, AI/ML, etc.)
- **Production Ready**: Built with industry best practices
- **Scalable Architecture**: Separate frontend & backend for easy scaling
- **Training Pipeline**: Optional fine-tuning for specialized branding

---

## 🏗️ Project Structure

```
brand_identity_generator_mvp/
├── frontend/                    # Next.js React Application
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   ├── components/        # React Components
│   │   ├── lib/              # Utilities & API Client
│   │   ├── hooks/            # Custom React Hooks
│   │   ├── stores/           # Zustand State Management
│   │   └── types/            # TypeScript Types
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.js
│
├── backend/                     # FastAPI Python Backend
│   ├── main.py               # FastAPI Application
│   ├── config.py             # Configuration Management
│   ├── schemas.py            # Pydantic Models
│   ├── llm_service.py        # LLM Integration
│   ├── requirements.txt
│   └── .env.example
│
├── training/                    # LLM Training Pipeline
│   ├── finetune.py          # Fine-tuning Scripts
│   └── data/
│       └── training/        # Training Data Directory
│
├── shared/                      # Shared Types & Schemas
│   └── types.ts             # TypeScript Definitions
│
├── docs/                     # All project documentation (organized)
│   ├── setup/               # Local dev, quick start, environment
│   ├── deployment/          # Deploy guides
│   │   └── gcp/             # Google Cloud specific docs
│   ├── architecture/        # System and design docs
│   ├── windows/             # PowerShell/Windows notes
│   ├── references/          # Indexes and references
│   └── reports/             # Delivery summaries
├── README.md                # Project Overview (this file)
```

---

## 🚀 Quick Start (5 minutes)

### 1. Clone or Extract Project

```bash
cd brand_identity_generator_mvp
```

### 2. Backend Setup (local & free by default)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Start with local free LLM (Ollama) or use built-in fallbacks
# If Ollama is not running, backend will still work with built-in generators

python -m uvicorn main:app --host 127.0.0.1 --port 8000
# Backend at http://localhost:8000 (see /docs)
```

### 3. Frontend Setup

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
# Frontend running at http://localhost:3000
```

### 4. Test the App

- Open http://localhost:3000
- Fill in company details
- Click "Generate Brand Identity"
- Wait 30-60 seconds for AI generation
- Review and download results

---

## 📦 Technology Stack

### Frontend

- **Framework**: Next.js 14 (React 18)
- **Styling**: Tailwind CSS + Custom CSS
- **Animations**: Framer Motion
- **State**: Zustand
- **HTTP**: Axios
- **UI Components**: Lucide React Icons
- **Type Safety**: TypeScript

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **LLM Provider**: Ollama (local, default) or Together AI/Cohere via env vars
- **Async**: AsyncIO + Uvicorn
- **Validation**: Pydantic
- **Logging**: Python Logging

### Optional Components

- **Database**: PostgreSQL (future)
- **Cache**: Redis (future)
- **Task Queue**: Celery (future)
- **Auth**: JWT via python-jose (future)

---

## 🔑 API Key Setup

### Optional: Configure Cloud LLMs

- Together AI: set TOGETHER_API_KEY in backend environment
- Cohere: set COHERE_API_KEY in backend environment

No keys are required for local development when using Ollama.

---

## 📊 API Endpoints

### Health Check

```
GET /health
Response: { status: "healthy", llm_model: "..." }
```

### Generate Branding

```
POST /api/v1/generate-branding
Request: {
  company_id: string,
  company_profile: CompanyProfile,
  num_variations: number (1-10),
  focus: "logo" | "tagline" | "palette" | "typography" | "all"
}
Response: BrandingResponse (logos, taglines, colors, typography, guidelines)
```

### Get Company Types

```
GET /api/v1/company-types
Response: { company_types: [{ id, name, description }, ...] }
```

### API Documentation

```
Interactive Docs: http://localhost:8000/docs
Alternative Docs: http://localhost:8000/redoc
```

---

## 🧠 How It Works

### Generation Flow

```
1. User Input
   ↓
2. Company Profile Sent to Backend
   ↓
3. LLM Processes with Custom Prompts
   ↓
4. Generate Logos → Taglines → Colors → Typography
   ↓
5. Compile Brand Guidelines
   ↓
6. Return Complete Brand Package
   ↓
7. Display & Download in Frontend
```

### LLM Integration

- Default: local Ollama model (mistral) for free, private inference
- Optional: Together AI or Cohere if API keys are provided
- Robust fallbacks and JSON parsing/validation ensure stable results

---

## 🧪 Testing

### Unit Tests (Backend)

```bash
cd backend
pytest tests/  # Create tests/ directory first
```

### Integration Tests (Full Stack)

```bash
# Start both services in separate terminals
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend + Tests
cd frontend
npm run dev
npm test
```

### Manual Testing

```bash
# Test API directly
curl -X POST http://localhost:8000/api/v1/generate-branding \
  -H "Content-Type: application/json" \
  -d @test_payload.json

# Or use Postman/Insomnia for easier testing
```

---

## 🚢 Deployment

### Frontend (Vercel)

```bash
cd frontend
npm install -g vercel
vercel deploy
# Add environment: NEXT_PUBLIC_API_URL=your-backend-url
```

### Backend (Render)

```bash
# Push to GitHub first
git push origin main

# In Render dashboard:
# 1. New Web Service
# 2. Connect GitHub repo
# 3. Runtime: Python 3.10
# 4. Build: pip install -r requirements.txt
# 5. Start: python main.py
# 6. Add TOGETHER_API_KEY env var
```

See `docs/` for detailed setup and deployment instructions. Start with `docs/README.md`.

---

## 🎓 Training Pipeline

### Fine-tune on Your Data

```bash
cd training
python finetune.py

# This creates:
# - Sample training dataset
# - Training prompts in JSONL format
# - Evaluation set
# - Fine-tuning guide
```

### Upload to Together AI

```bash
# Follow guide output to fine-tune
# Cost: ~$10-50 per job
# Improvement: 15-30% better accuracy
```

---

## 🔒 Security Best Practices

- ✅ Environment variables for all secrets
- ✅ No API keys in source code
- ✅ CORS properly configured
- ✅ Input validation via Pydantic
- ✅ Rate limiting ready
- ✅ Error handling without exposing internals
- ✅ Logging for debugging
- ✅ .gitignore configured

---

## 📈 Performance

### Generation Time

- **Average**: 30-60 seconds
- **First call**: May be slower (model loading)
- **Subsequent calls**: Consistent 40-50s

### Optimization Tips

- Use Together AI's faster models (Mistral 7B)
- Cache common company type profiles
- Implement request queuing for high traffic
- Use CDN for frontend assets

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Make your changes
4. Write tests
5. Submit pull request

---

## 📝 License

MIT License - Feel free to use commercially

---

## 🆘 Troubleshooting

### Backend won't connect to LLM

```bash
# Check API key
echo $TOGETHER_API_KEY

# Check internet connection
curl https://api.together.xyz/v1/models

# Check logs
DEBUG=true python main.py
```

### Frontend can't reach backend

```bash
# Check backend running
curl http://localhost:8000/health

# Check .env.local
cat frontend/.env.local

# Check CORS in backend
# CORS_ORIGINS should include frontend URL
```

### Generation is slow or timing out

- Check Together AI status: https://status.together.ai
- Reduce `num_variations` parameter
- Try with `focus: "logo"` instead of `"all"`

---

## � Documentation

- Central docs hub: `docs/README.md`
- Local setup and quick start: `docs/setup/`
- Deployment (GCP and more): `docs/deployment/`
- Architecture: `docs/architecture/`

API Docs: http://localhost:8000/docs

---

**Made with ❤️ for creators and startups**

_Last Updated: November 2024_
