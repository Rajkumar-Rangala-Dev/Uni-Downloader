# Railway Deployment Guide

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub account
- Push this repository to GitHub

## Step 1: Deploy Backend to Railway

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Click "New Project"

2. **Deploy from GitHub**
   - Select "Deploy from GitHub repo"
   - Choose your `Uni-Downloader` repository
   - Railway will detect the Dockerfile automatically

3. **Configure Backend Service**
   - **Root Directory**: Set to `backend`
   - **Dockerfile Path**: `Dockerfile`
   
4. **Set Environment Variables**
   - Go to "Variables" tab
   - Add these variables:
     ```
     TEMP_DIR=/tmp
     COOKIE_BROWSER=
     MAX_FILE_SIZE_MB=200
     DOWNLOAD_TIMEOUT=600
     ```

5. **Deploy**
   - Railway will automatically build and deploy
   - Wait for deployment to complete
   - Copy the **public URL** (e.g., `https://your-backend.up.railway.app`)

## Step 2: Deploy Frontend to Railway

1. **Create New Service**
   - In the same Railway project, click "New"
   - Select "GitHub Repo" again
   - Choose the same `Uni-Downloader` repository

2. **Configure Frontend Service**
   - **Root Directory**: Set to `frontend`
   - **Dockerfile Path**: `Dockerfile`

3. **Set Environment Variables**
   - Go to "Variables" tab
   - Add this variable with your backend URL:
     ```
     NEXT_PUBLIC_API_BASE=https://your-backend.up.railway.app
     ```
   - Replace `your-backend.up.railway.app` with the actual backend URL from Step 1

4. **Deploy**
   - Railway will automatically build and deploy
   - Wait for deployment to complete
   - Your frontend will be available at the provided URL

## Alternative: Using Railway CLI

### Install Railway CLI
```bash
npm i -g @railway/cli
railway login
```

### Deploy Backend
```bash
cd backend
railway init
railway up
railway open
# Copy the URL and set it as environment variable for frontend
```

### Deploy Frontend
```bash
cd ../frontend
railway init
railway variables --set NEXT_PUBLIC_API_BASE=https://your-backend-url.railway.app
railway up
railway open
```

## Important Notes

### Backend Configuration
- The backend uses Railway's `$PORT` environment variable automatically
- FFmpeg is installed in the Docker container
- Downloads are stored in `/tmp` which is ephemeral in Railway
- Files are auto-deleted after download to save space

### Frontend Configuration
- The `NEXT_PUBLIC_API_BASE` environment variable **must** be set
- This variable is baked into the build, so you need to redeploy if you change it
- Format: `https://your-backend-url.railway.app` (no trailing slash)

### CORS
- Backend is configured with `allow_origins=["*"]` for all domains
- Works with any frontend URL

## Troubleshooting

### Backend Issues
1. **FFmpeg not found**
   - Check Dockerfile has `ffmpeg` installation
   - Rebuild: `railway up --detach`

2. **Port issues**
   - Railway sets `$PORT` automatically
   - Don't hardcode port 8000

3. **Download failures**
   - Check Railway logs: `railway logs`
   - Instagram may require cookies (not supported in serverless)

### Frontend Issues
1. **CORS errors**
   - Verify `NEXT_PUBLIC_API_BASE` is set correctly
   - Redeploy after changing environment variables

2. **API not found**
   - Check backend URL is correct
   - Ensure backend is deployed and running

3. **Build failures**
   - Check Node.js version (should be 20)
   - Verify all dependencies in package.json

## Monitoring
- View logs: Railway Dashboard → Service → Logs
- Check metrics: CPU, Memory, Network usage
- Set up alerts for downtime

## Cost Optimization
- Railway offers $5 free credit per month
- Backend: ~0.1 vCPU, ~512MB RAM
- Frontend: ~0.1 vCPU, ~256MB RAM
- Monitor usage in Railway dashboard

## Updating
When you push to GitHub:
- Railway auto-deploys if connected to GitHub
- Or manually trigger: `railway up`

## Domain Setup (Optional)
1. Go to Service Settings → Networking
2. Add custom domain
3. Configure DNS records as instructed
4. Update `NEXT_PUBLIC_API_BASE` in frontend if backend domain changes
