# 🚀 QUICK START - Local Development with Ollama

## ⚡ 5-Minute Setup (NO API Keys Needed!)

### Prerequisites ✅

- Windows/Mac/Linux
- 8GB+ RAM
- Ollama installed (https://ollama.ai)

### Step 1: Download & Start Ollama

```bash
# Go to https://ollama.ai and download
# After installation, start it:
ollama serve
```

**Keep this terminal running!**

### Step 2: Get a Model (30 seconds)

Open a **NEW terminal**:

```bash
ollama pull mistral
```

Wait for download (~4GB). Once done, the model is cached locally - subsequent uses are instant!

### Step 3: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Start Backend (NEW terminal)

```bash
cd backend
python -m uvicorn main:app --reload
```

You'll see:

```
Uvicorn running on http://127.0.0.1:8000
```

**Keep this running!**

### Step 5: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 6: Start Frontend (NEW terminal)

```bash
cd frontend
npm run dev
```

You'll see:

```
> Local:        http://localhost:3000
```

### Step 7: Open Browser

Go to: **http://localhost:3000** 🎉

---

## 📋 Check Everything Works

### Verify Ollama

```bash
curl http://localhost:11434/api/tags
```

Should return list of available models

### Verify Backend

```bash
curl http://localhost:8000/health
```

Should return:

```json
{"status": "healthy", "llm_model": "mistral", ...}
```

### Try Generation

Open http://localhost:3000:

1. Fill in company details
2. Click "Generate Brand"
3. Watch the magic happen! ✨

---

## 🎯 Terminal Layout

```
┌─────────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│   Terminal 1        │  │   Terminal 2     │  │   Terminal 3    │
│                     │  │                  │  │                 │
│ ollama serve        │  │ python -m        │  │ npm run dev     │
│                     │  │ uvicorn main:app │  │                 │
│ Port: 11434         │  │ Port: 8000       │  │ Port: 3000      │
│ (KEEP RUNNING)      │  │ (KEEP RUNNING)   │  │ (KEEP RUNNING)  │
└─────────────────────┘  └──────────────────┘  └─────────────────┘
         │                       │                      │
         └───────────────────────┴──────────────────────┘
                        http://localhost:3000
                          (Open in browser)
```

---

## 🛠️ Configuration

### Change Model

Edit `backend/.env`:

```env
LLM_MODEL=neural-chat  # or dolphin-mixtral, phi, etc.
```

### Adjust Creativity

```env
LLM_TEMPERATURE=0.7  # Higher = more creative
```

---

## 🚨 Troubleshooting

### "Connection refused" at localhost:11434

```
Ollama not running!
Solution: Run "ollama serve" in a separate terminal
```

### "Model not found"

```
Solution: Run "ollama pull mistral"
```

### Frontend can't reach backend

```
Check: http://localhost:8000/health works?
If not, backend not running or wrong port
```

### Out of memory errors

```
Try smaller model: ollama pull neural-chat
Or close other applications
```

---

## 📊 Available Models

| Model           | Size  | Speed  | Quality  | Recommended          |
| --------------- | ----- | ------ | -------- | -------------------- |
| neural-chat     | 3.5GB | ⚡⚡⚡ | ⭐⭐     | ✅ Fastest           |
| **mistral**     | 4.1GB | ⚡⚡   | ⭐⭐⭐   | ✅ **Balanced**      |
| dolphin-mixtral | 25GB  | ⚡     | ⭐⭐⭐⭐ | 🚀 Best (needs 48GB) |
| phi             | 2.7GB | ⚡⚡⚡ | ⭐⭐     | 💾 Minimal           |

---

## 🎓 How It Works

1. **Frontend (Next.js)** - Beautiful UI at http://localhost:3000
2. **Backend (FastAPI)** - API at http://localhost:8000
3. **Ollama (Local LLM)** - AI brain at http://localhost:11434

No cloud services. Everything runs locally. 100% free after initial setup!

---

## 📝 Next Steps

1. ✅ **Generate some brands** - Try different industries
2. 📖 **Read the code** - Check `backend/llm_service.py` for how generation works
3. 🎨 **Customize prompts** - Edit prompts in `llm_service.py` to change output style
4. 🚀 **Deploy** - See DEPLOYMENT.md for cloud options

---

## 💡 Pro Tips

- **First generation** takes longer (model warming up)
- **Subsequent requests** are much faster (~10-30 seconds)
- **Run multiple models** - Ollama manages them efficiently
- **Low on disk?** Delete unused models: `ollama rm <model-name>`
- **Want faster?** Use `neural-chat` (3x faster, slightly lower quality)

---

## 🤝 Need Help?

Check these files:

- `LOCAL_SETUP_OLLAMA.md` - Detailed setup guide
- `backend/.env` - Configuration options
- `http://localhost:8000/docs` - Interactive API documentation

---

**Enjoy building! 🚀🎨**
