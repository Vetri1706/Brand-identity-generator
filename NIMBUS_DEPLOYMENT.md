# Nimbus Platform Deployment Guide (ByteXL)

## 🚀 Brand Identity Generator - Deployment Instructions

This guide will help you deploy the **Premium Brand Identity Generator** to the **Nimbus Platform** at ByteXL.

---

## 📋 Project Overview

**Project Name:** Brand Identity Generator  
**Technology Stack:** Python 3.13+ | Streamlit | AI APIs (Freepik, Stability AI, Google Gemini)  
**Purpose:** AI-powered brand identity generation with logos, taglines, color palettes, and fonts  
**Deployment Target:** Nimbus Platform (ByteXL)

---

## 📦 Pre-Deployment Checklist

### ✅ Files Included:
- [x] `app.py` - Main application (2100+ lines)
- [x] `requirements.txt` - Python dependencies
- [x] `config.py` - Configuration utilities
- [x] `utils.py` - Helper functions
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `.env.example` - Environment variable template
- [x] `README.md` - Project documentation
- [x] Documentation files (15+ guides)

### ✅ Features:
- [x] 8 Global Standard Design Themes
- [x] AI Logo Generation (Freepik, Stability AI)
- [x] AI Tagline Generation (Google Gemini)
- [x] Built-in Logo Generator (Fallback)
- [x] Color Palette Generation
- [x] Font Recommendations
- [x] Social Media Mockups
- [x] ZIP Download of All Assets
- [x] Premium UI/UX Design

---

## 🔧 Deployment Steps for Nimbus Platform

### Step 1: Prepare Project Directory

```bash
# Navigate to project directory
cd d:\Miniproj\brand_identity_generator

# Verify all files are present
dir
```

### Step 2: Environment Configuration

Create `.env` file from template:

```bash
# Copy template
copy .env.example .env

# Edit .env with your API keys
notepad .env
```

**.env Contents:**
```env
# AI API Keys
FREEPIK_API_KEY=FPSX4348e07e94407257da038c3276b06411
STABILITY_API_KEY=sk-Jk7BVf7yLSsdXVxN0ljY54YocUCr7CBjsur13hrrLEkAcj9l
GENAI_API_KEY=AIzaSyB_tyhoIu-zCZIBZw2o2qpiFQsHACEwbno
OPENAI_API_KEY=

# Application Settings
USE_AI_BY_DEFAULT=False
DEFAULT_AI_PROVIDER=Freepik
```

### Step 3: Verify Dependencies

**requirements.txt:**
```
streamlit>=1.28.0
Pillow>=10.0.0
google-generativeai>=0.3.0
requests>=2.31.0
```

Install and test locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Step 4: Create Nimbus Deployment Package

Create a deployment-ready structure:

```
brand_identity_generator/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── config.py                 # Configuration
├── utils.py                  # Utilities
├── .streamlit/
│   └── config.toml          # Streamlit config
├── .env                      # Environment variables (SECURE!)
├── README.md                 # Documentation
└── docs/                     # Additional documentation
    ├── NIMBUS_DEPLOYMENT.md
    ├── QUICKSTART.md
    ├── API_SETUP_GUIDE.md
    └── THEME_UI_UPGRADE.md
```

---

## 🌐 Nimbus Platform Configuration

### Platform Settings:

**1. Application Type:**
- Framework: `Streamlit`
- Python Version: `3.13` or `3.11+`
- Entry Point: `app.py`

**2. Build Command:**
```bash
pip install -r requirements.txt
```

**3. Start Command:**
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**4. Environment Variables (Set in Nimbus Dashboard):**
```
FREEPIK_API_KEY=FPSX4348e07e94407257da038c3276b06411
STABILITY_API_KEY=sk-Jk7BVf7yLSsdXVxN0ljY54YocUCr7CBjsur13hrrLEkAcj9l
GENAI_API_KEY=AIzaSyB_tyhoIu-zCZIBZw2o2qpiFQsHACEwbno
USE_AI_BY_DEFAULT=False
DEFAULT_AI_PROVIDER=Freepik
```

**5. Port Configuration:**
- Default Port: `8501` (or use Nimbus-assigned port)
- Protocol: `HTTP/HTTPS`

**6. Health Check:**
- Endpoint: `/healthz` (Streamlit default)
- Timeout: `30 seconds`

---

## 🔒 Security Considerations

### API Keys Management:

**❌ DO NOT:**
- Commit API keys to Git repository
- Hardcode keys in `app.py`
- Share `.env` file publicly

**✅ DO:**
- Use Nimbus environment variables
- Keep `.env` file in `.gitignore`
- Rotate keys regularly
- Use separate keys for dev/prod

### Update app.py to Use Environment Variables:

The app already supports loading from environment:
```python
# Lines 20-33 in app.py
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyB_tyhoIu-zCZIBZw2o2qpiFQsHACEwbno")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "sk-Jk7BVf7yLSsdXVxN0ljY54YocUCr7CBjsur13hrrLEkAcj9l")
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY", "FPSX4348e07e94407257da038c3276b06411")
```

---

## 📊 Resource Requirements

### Minimum Requirements:
- **CPU**: 1 vCPU
- **RAM**: 512 MB
- **Storage**: 100 MB
- **Bandwidth**: Standard

### Recommended for Production:
- **CPU**: 2 vCPUs
- **RAM**: 1-2 GB (for AI processing)
- **Storage**: 250 MB
- **Bandwidth**: High (for image generation)

---

## 🧪 Testing Deployment

### Pre-Deployment Tests:

1. **Local Test:**
```bash
streamlit run app.py
# Navigate to http://localhost:8501
# Test all features
```

2. **Feature Checklist:**
- [ ] Sidebar visible with themes
- [ ] All 8 design themes selectable
- [ ] Company info form functional
- [ ] Generate button works
- [ ] Built-in logos generate (no AI)
- [ ] AI generation works (with keys)
- [ ] Taglines generate
- [ ] Colors display correctly
- [ ] Fonts suggested
- [ ] Mockup renders
- [ ] ZIP download works

3. **API Tests:**
```python
# Test each API (optional)
python test_setup.py
```

---

## 🚀 Deployment Process

### Method 1: Git Repository (Recommended)

1. **Push to Git:**
```bash
git init
git add .
git commit -m "Initial deployment to Nimbus"
git remote add origin <your-bytexl-repo-url>
git push -u origin main
```

2. **Connect to Nimbus:**
- Login to ByteXL Nimbus Platform
- Create New Application
- Select "Import from Git"
- Connect repository
- Configure build settings
- Add environment variables
- Deploy

### Method 2: Direct Upload

1. **Create ZIP package:**
```bash
# Compress project folder
Compress-Archive -Path d:\Miniproj\brand_identity_generator\* -DestinationPath brand_identity_generator.zip
```

2. **Upload to Nimbus:**
- Login to ByteXL Nimbus Platform
- Create New Application
- Select "Upload ZIP"
- Upload `brand_identity_generator.zip`
- Configure settings
- Add environment variables
- Deploy

### Method 3: CLI Deployment (If Available)

```bash
# Nimbus CLI commands (if ByteXL provides CLI)
nimbus login
nimbus create-app brand-identity-generator
nimbus deploy --path ./brand_identity_generator
nimbus env set FREEPIK_API_KEY=FPSX4348e07e94407257da038c3276b06411
nimbus env set STABILITY_API_KEY=sk-Jk7BVf7yLSsdXVxN0ljY54YocUCr7CBjsur13hrrLEkAcj9l
nimbus env set GENAI_API_KEY=AIzaSyB_tyhoIu-zCZIBZw2o2qpiFQsHACEwbno
nimbus start
```

---

## 🔧 Post-Deployment Configuration

### 1. Verify Deployment:
- Check Nimbus dashboard for build status
- View deployment logs
- Confirm app is running

### 2. Test Live Application:
```
https://your-app-name.nimbus.bytexl.com
or
https://nimbus.bytexl.com/apps/brand-identity-generator
```

### 3. Monitor Performance:
- Check response times
- Monitor memory usage
- Review error logs
- Test AI integrations

### 4. Configure Custom Domain (Optional):
- Add custom domain in Nimbus
- Update DNS records
- Enable HTTPS/SSL

---

## 📝 Nimbus Platform Specifics

### Streamlit Configuration (.streamlit/config.toml):

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#667eea"
backgroundColor = "#f5f7fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#2d3748"
font = "sans serif"
```

### Nimbus Health Checks:

If Nimbus requires a custom health endpoint:

**Add to app.py (before main()):**
```python
# Health check endpoint
@st.cache_data(ttl=60)
def health_check():
    return {"status": "healthy", "version": "2.0"}

if st.query_params.get("health") == "check":
    st.json(health_check())
    st.stop()
```

---

## 🐛 Troubleshooting

### Issue: App Won't Start

**Solution:**
```bash
# Check logs
nimbus logs brand-identity-generator

# Common fixes:
1. Verify Python version (3.11+)
2. Check requirements.txt syntax
3. Ensure all dependencies installed
4. Verify port configuration
```

### Issue: API Keys Not Working

**Solution:**
```bash
# Verify environment variables
nimbus env list

# Re-set variables
nimbus env set FREEPIK_API_KEY=your-key-here
nimbus env set STABILITY_API_KEY=your-key-here
nimbus env set GENAI_API_KEY=your-key-here

# Restart app
nimbus restart brand-identity-generator
```

### Issue: Out of Memory

**Solution:**
- Upgrade to higher tier plan
- Increase RAM allocation
- Optimize image processing
- Enable caching in Streamlit

### Issue: Slow Response Times

**Solution:**
- Enable Streamlit caching
- Optimize AI API calls
- Use CDN for static assets
- Upgrade CPU allocation

---

## 📊 Monitoring & Logs

### View Logs:
```bash
# Real-time logs
nimbus logs brand-identity-generator --follow

# Recent errors
nimbus logs brand-identity-generator --level error

# Specific time range
nimbus logs brand-identity-generator --since 1h
```

### Key Metrics to Monitor:
- Response time (should be < 2s)
- Memory usage (should be < 1GB)
- API success rate (should be > 95%)
- Error rate (should be < 5%)
- User session duration

---

## 🔄 Updates & Maintenance

### Deploy Updates:

**Git Method:**
```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push origin main

# Nimbus auto-deploys on push (if configured)
```

**Manual Method:**
```bash
# Upload new version
nimbus deploy --path ./brand_identity_generator --force
```

### Rollback (If Needed):
```bash
# Rollback to previous version
nimbus rollback brand-identity-generator --version previous
```

---

## 🎯 Production Best Practices

### 1. Use Environment Variables:
```python
# In app.py - already implemented
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY", "")
```

### 2. Enable Caching:
```python
# Already implemented in app.py
@st.cache_data(ttl=3600)
def generate_logo(...):
    ...
```

### 3. Error Handling:
```python
# Already implemented
try:
    logo = generate_logo_freepik(...)
except Exception as e:
    st.error(f"AI generation failed: {e}")
    logo = create_placeholder_logo(...)
```

### 4. Rate Limiting:
```python
# Add to app.py if needed
import time
from functools import wraps

def rate_limit(calls_per_minute):
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 60.0 / calls_per_minute - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator
```

### 5. Analytics (Optional):
```python
# Add Google Analytics or Nimbus analytics
# Already has usage tracking in Streamlit
```

---

## 📞 Support & Resources

### ByteXL Nimbus Support:
- **Documentation**: https://nimbus.bytexl.com/docs
- **Support Portal**: support@bytexl.com
- **Community Forum**: https://community.bytexl.com
- **Status Page**: https://status.bytexl.com

### Project Resources:
- **GitHub**: (Your repository URL)
- **Documentation**: `/docs` folder
- **Issues**: (Issue tracker URL)
- **API Keys**: Store securely in password manager

---

## ✅ Deployment Checklist

Before going live:

- [ ] All code tested locally
- [ ] Environment variables configured
- [ ] API keys validated
- [ ] `.gitignore` includes `.env`
- [ ] Dependencies up to date
- [ ] Documentation complete
- [ ] Error handling in place
- [ ] Caching enabled
- [ ] Health checks working
- [ ] Logs configured
- [ ] Monitoring enabled
- [ ] Backup plan ready
- [ ] Team notified
- [ ] DNS configured (if custom domain)
- [ ] SSL/HTTPS enabled

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ App loads at Nimbus URL  
✅ All 8 themes display correctly  
✅ Logo generation works (built-in)  
✅ AI generation works (with keys)  
✅ Forms accept input  
✅ Download works  
✅ No console errors  
✅ Mobile responsive  
✅ Response time < 3s  
✅ Uptime > 99%

---

## 📧 Contact

**Project Maintainer:** (Your Name)  
**Email:** (Your Email)  
**Organization:** ByteXL  
**Platform:** Nimbus

---

## 🔖 Version History

- **v2.0** - Premium UI/UX with global design themes
- **v1.5** - Freepik AI integration
- **v1.0** - Initial release with OpenAI/Stability AI

---

**Ready to deploy!** 🚀

Follow the steps above to get your Brand Identity Generator live on ByteXL's Nimbus Platform.

For questions or issues, contact ByteXL Nimbus support or refer to the project documentation.
