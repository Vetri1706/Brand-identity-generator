# 🎯 How to Run with Ollama (Llama)

## Quick Summary

This project uses **Ollama** to run AI models locally (like Llama, Mistral, etc.) - completely FREE and private!

---

## Option 1: Automated (Easiest!) ⭐

Just double-click:

```
start-with-ollama.bat
```

This will:

1. Check if Ollama is installed
2. Download the Mistral model if needed
3. Start all services automatically
4. Open your browser to http://localhost:3000

---

## Option 2: Manual Setup

### Prerequisites

1. **Install Ollama**: https://ollama.ai/download/windows
2. **Install Python** (you have this)
3. **Install Node.js** (you have this)

### Quick Start

Open **3 separate PowerShell terminals**:

**Terminal 1 - Ollama:**

```powershell
ollama serve
```

**Terminal 2 - Backend:**

```powershell
cd C:\Users\vetri\Miniproj\brand_identity_generator_mvp\backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

**Terminal 3 - Frontend:**

```powershell
cd C:\Users\vetri\Miniproj\brand_identity_generator_mvp\frontend
npm run dev
```

**Open browser:** http://localhost:3000

---

## Available Models

You can use different Ollama models. Edit `backend/.env` and change `LLM_MODEL`:

```env
LLM_MODEL=mistral      # Default, balanced (4GB)
LLM_MODEL=llama2       # Original Llama2 (4GB)
LLM_MODEL=neural-chat  # Faster (3.5GB)
LLM_MODEL=phi          # Smallest (2.7GB)
```

Download a new model:

```powershell
ollama pull llama2
```

List installed models:

```powershell
ollama list
```

---

## Troubleshooting

### "Connection refused" on backend startup

**Problem:** Ollama isn't running

**Fix:** Start Ollama first:

```powershell
ollama serve
```

### Backend works but results are generic

**Problem:** Ollama model not downloaded

**Fix:** Pull the model:

```powershell
ollama pull mistral
```

### Want better quality?

Try a larger model:

```powershell
ollama pull llama2:13b
```

Then update `backend/.env`:

```env
LLM_MODEL=llama2:13b
```

---

## What is Ollama?

- **Free & Open Source**: No API costs
- **Private**: Runs 100% on your computer
- **Offline**: Works without internet (after initial download)
- **Fast**: Uses your GPU automatically
- **Easy**: Simple commands, no configuration

---

## Cost Comparison

| Option      | Cost          | Setup Time | Privacy         |
| ----------- | ------------- | ---------- | --------------- |
| **Ollama**  | $0/month      | 10 min     | 100% Private ✅ |
| Together AI | $5-50/month   | 5 min      | Sent to API ❌  |
| OpenAI      | $20-100/month | 5 min      | Sent to API ❌  |

---

## URLs When Running

- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **Ollama**: http://localhost:11434

---

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull mistral model
3. ✅ Start all services
4. 🎨 **Generate your first brand!**
5. 📖 Read `docs/` for advanced features
6. 🚀 Deploy when ready (see `docs/deployment/`)

---

**Need Help?**

- Ollama docs: https://ollama.ai/
- Project docs: `docs/README.md`
- Setup guide: `docs/setup/LOCAL_SETUP_OLLAMA.md`

---

**Status**: ✅ Ready to run with free local AI!
