# 🎨 AI Logo Generator

> Revolutionary logo generation system with industry intelligence

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/NwjBNp)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Vetri1706/Brand-identity-generator&project-name=ai-logo-generator&repository-name=ai-logo-generator)

## 🚀 Features

- **6 Logo Categories**: Wordmark, Lettermark, Pictorial, Abstract, Combination, Emblem
- **Industry Intelligence**: Specialized designs for Tech, Healthcare, Finance, and more
- **Professional Quality**: High-resolution 1000x1000px logos
- **Instant Generation**: Real-time logo creation with AI

## 🏗️ Architecture

```
├── backend/          # FastAPI Python server
│   ├── main.py      # API endpoints
│   └── professional_logo_generator.py
├── frontend/         # Next.js React app
│   ├── src/app/     # App router pages
│   └── src/components/
└── README.md
```

## 🚀 Quick Start

### Local Development

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

### Free Deployment

1. **Backend**: Deploy on [Railway](https://railway.app)
2. **Frontend**: Deploy on [Vercel](https://vercel.com)

## 📋 API Endpoints

- `POST /api/professional-logos` - Generate diverse professional logos
- `GET /health` - Health check

## 🎯 Tech Stack

- **Backend**: Python, FastAPI, Pillow
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Deployment**: Railway (Backend), Vercel (Frontend)

## 📄 License

MIT License - feel free to use for personal and commercial projects.

---

**Generate professional logos with AI-powered industry intelligence.**
