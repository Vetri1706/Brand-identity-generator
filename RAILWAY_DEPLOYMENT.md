# 🚂 Railway Backend Deployment

## Instant Deploy (30 seconds)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FVetri1706%2FBrand-identity-generator&plugins=postgresql&envs=PORT&PORTDesc=Port+for+the+server&PORTDefault=8000)

## Manual Deploy (2 minutes)

1. **Go to Railway**: https://railway.app
2. **Sign up** with your GitHub account
3. **Click "Deploy from GitHub"**
4. **Select**: `Vetri1706/Brand-identity-generator`
5. **Railway auto-detects Python** → Deploys automatically!

## Your Backend URL

After deployment, you'll get a URL like:

```
https://brand-identity-generator-production.up.railway.app
```

## Test Your Backend

```bash
curl https://your-backend-url.railway.app/health
```

Should return: `{"status": "healthy"}`

## Environment Variables (if needed)

In Railway dashboard:

- `PORT`: 8000 (auto-set)
- Add any custom configs later

✅ **Backend will be LIVE in 2 minutes!**
