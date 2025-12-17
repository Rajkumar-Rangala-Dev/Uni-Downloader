# 🚀 Quick Railway Deployment

## Prerequisites
✅ Railway account (https://railway.app - free tier available)
✅ This repository pushed to GitHub

---

## Option 1: Using Railway Dashboard (Easiest)

### Step 1: Deploy Backend
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. **Important**: Set Root Directory to `backend`
5. Add environment variables:
   - `TEMP_DIR` = `/tmp`
   - `COOKIE_BROWSER` = (leave empty)
6. Click Deploy
7. **Copy the backend URL** (e.g., `https://abc123.up.railway.app`)

### Step 2: Deploy Frontend
1. In same Railway project, click "+ New"
2. Select "GitHub Repo" → Same repository
3. **Important**: Set Root Directory to `frontend`
4. Add environment variable:
   - `NEXT_PUBLIC_API_BASE` = `<your-backend-url-from-step-1>`
   - Example: `https://abc123.up.railway.app`
5. Click Deploy
6. Done! Your app is live 🎉

---

## Option 2: Using Railway CLI (Advanced)

### Install CLI
```bash
npm install -g @railway/cli
railway login
```

### Deploy Backend
```bash
cd backend
railway init
railway up
# Copy the URL shown
```

### Deploy Frontend
```bash
cd ../frontend
railway init
railway variables --set NEXT_PUBLIC_API_BASE=<backend-url>
railway up
```

---

## 🎯 What You'll Get

- ✅ **Backend**: `https://your-backend.railway.app`
  - API endpoints at `/analyze`, `/download`, `/file/{id}`
  - FFmpeg pre-installed
  - Auto-scaling
  - HTTPS enabled

- ✅ **Frontend**: `https://your-frontend.railway.app`
  - Modern UI
  - Connected to backend
  - HTTPS enabled

---

## 🔧 Important Notes

1. **Root Directory**: Must be set correctly
   - Backend: `backend`
   - Frontend: `frontend`

2. **Environment Variables**:
   - Backend needs `TEMP_DIR=/tmp`
   - Frontend needs `NEXT_PUBLIC_API_BASE=<backend-url>`

3. **Redeployment**:
   - If you change `NEXT_PUBLIC_API_BASE`, redeploy frontend
   - Push to GitHub triggers auto-deploy (if enabled)

4. **Costs**:
   - Railway free tier: $5 credit/month
   - This app uses ~$3-5/month

---

## ✅ Verify Deployment

### Test Backend
```bash
curl https://your-backend.railway.app/
# Should return: {"status":"ok","message":"Universal Media Downloader API"}
```

### Test Frontend
Open `https://your-frontend.railway.app` in browser

---

## 🆘 Troubleshooting

### Backend won't start
- Check logs in Railway dashboard
- Verify Dockerfile path is correct
- Ensure ffmpeg installed (check Dockerfile)

### Frontend shows CORS errors
- Verify `NEXT_PUBLIC_API_BASE` is set correctly
- Must redeploy frontend after changing env vars
- Backend URL should NOT have trailing slash

### Download fails
- Check backend logs for FFmpeg errors
- Instagram may need authentication
- YouTube works for public videos

---

## 📚 Full Guide

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for complete documentation.
