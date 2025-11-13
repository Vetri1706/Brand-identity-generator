# 🚀 Deployment Guide

Deploy your AI Logo Generator for free using modern platforms.

## Quick Deploy Buttons

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/NwjBNp)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Vetri1706/Brand-identity-generator)

## Manual Deployment

### Backend (Railway)

1. Sign up at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy automatically

### Frontend (Vercel)

1. Sign up at [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Deploy automatically

### Environment Variables

Add to Vercel:
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

Your logo generator will be live in minutes!