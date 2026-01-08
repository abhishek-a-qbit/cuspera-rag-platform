# Railway Deployment Fix

## Problem
The Railway deployment is showing a default Railway page instead of our API endpoints. This means the wrong backend file is being deployed.

## Solution
Railway needs to be configured to run `api_backend_simple.py` instead of the basic API.

## Steps to Fix Railway Deployment

### 1. Update Railway Service Configuration
- Go to Railway dashboard
- Select your `cuspera-rag-platform-production` service
- Click on "Settings" tab
- Update the "Start Command" to: `python api_backend_simple.py`
- Update the "Port" to: `8000`

### 2. Update Railway File Structure
Ensure your Railway repository has:
- `api_backend_simple.py` (not just `api_backend.py`)
- `requirements.txt` with all dependencies
- `.env` file with API keys

### 3. Redeploy Railway Service
- Commit and push changes to Railway
- Railway will automatically redeploy with correct backend
- Verify deployment by checking `/health` endpoint

### 4. Test API Endpoints
After deployment, test:
```bash
curl https://cuspera-rag-platform-production.railway.app/health
curl -X POST https://cuspera-rag-platform-production.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "test", "product": "6sense"}'
```

## Current Status
- Streamlit app is configured to call Railway API
- Railway is running wrong backend (default Railway page)
- Fallback responses are working in Streamlit
- Need Railway deployment fix for proper API endpoints

## Expected Result After Fix
- `/health` endpoint returns `{"status": "ok"}`
- `/chat` endpoint returns AI-powered responses
- Streamlit chat works with real RAG pipeline
- No more 404 errors in Streamlit app
