# 🚀 LOCAL DEVELOPMENT SETUP - Ollama (Free, No API Keys Required)

## Quick Start (5 minutes)

### Step 1: Install Ollama
Ollama runs AI models locally on your machine for FREE - no API keys needed!

**Windows/Mac/Linux:**
Download from: https://ollama.ai

### Step 2: Pull a Model
```powershell
ollama pull mistral
```
This downloads the Mistral model (lightweight, ~4GB). Other options:
- `ollama pull neural-chat` (faster)
- `ollama pull dolphin-mixtral` (better quality)

### Step 3: Start Ollama
```powershell
ollama serve
```
Leave this running in a terminal. Ollama will be available at `http://localhost:11434`

### Step 4: Install Backend Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

### Step 5: Start Backend (New Terminal)
```powershell
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

### Step 6: Install Frontend Dependencies
```powershell
cd frontend
npm install
```

### Step 7: Start Frontend (Another Terminal)
```powershell
cd frontend
npm run dev
```

Frontend: http://localhost:3000

---

## ✅ Verification Checklist

- [ ] Ollama running (`ollama serve` terminal visible)
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can see API docs at http://localhost:8000/docs
- [ ] Form loads at http://localhost:3000

---

## 🧪 Test the API

In a new terminal:

```powershell
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test Backend Health
curl http://localhost:8000/health

# Test Brand Generation
curl -X POST http://localhost:8000/api/generate-brand `
  -H "Content-Type: application/json" `
  -d @'{
    "name": "TechStartup",
    "company_type": "SaaS",
    "industry": "AI/ML",
    "description": "AI-powered analytics platform",
    "target_audience": "Enterprise customers",
    "brand_values": ["Innovation", "Simplicity"],
    "tone": "professional"
  }'
```

---

## 📊 Models Performance

| Model | Size | Speed | Quality | RAM |
|-------|------|-------|---------|-----|
| neural-chat | 3.5GB | ⚡⚡⚡ | 🌟🌟 | 6GB |
| mistral | 4.1GB | ⚡⚡ | 🌟🌟🌟 | 8GB |
| dolphin-mixtral | 25GB | ⚡ | 🌟🌟🌟🌟 | 48GB |

**Recommendation:** Start with `mistral` for good balance.

---

## 🔧 Troubleshooting

### "Failed to initialize LLM"
- Ollama not running? Start it: `ollama serve`
- Model not pulled? Run: `ollama pull mistral`
- Wrong port? Check `http://localhost:11434` is accessible

### "Connection refused"
```powershell
# Check if Ollama is listening
netstat -ano | findstr :11434
```

### Slow generation?
- Using a faster model: `ollama pull neural-chat`
- Check system resources (CPU/RAM usage)

### Frontend can't reach backend?
- Backend running on http://localhost:8000?
- CORS enabled? (should be in main.py)
- Check browser console for errors

---

## 📚 Ollama Commands

```powershell
# List available models
ollama list

# Pull a model
ollama pull [model-name]

# Remove a model
ollama rm mistral

# Show model info
ollama show mistral

# Run interactive chat
ollama run mistral
```

---

## 🎯 Next Steps

1. **Test the application** - Fill form on http://localhost:3000
2. **Check results** - Should generate logos, taglines, colors, typography
3. **Debug if needed** - Check terminal outputs and http://localhost:8000/docs
4. **Customize** - Edit prompts in `backend/llm_service.py`

---

## 📝 Configuration

Edit `backend/.env` to customize:
```env
LLM_MODEL=mistral           # Change model
LLM_TEMPERATURE=0.7         # Higher = more creative, 0.3 = more focused
LLM_MAX_TOKENS=1024         # Max response length
OLLAMA_BASE_URL=http://localhost:11434  # Custom Ollama URL
```

---

## 💡 Tips

- **First generation** will be slow (model warming up)
- **Subsequent requests** are much faster
- **Out of memory?** Close other apps or use smaller model
- **Want to fine-tune?** Check `training/finetune.py`

Enjoy! 🎨
