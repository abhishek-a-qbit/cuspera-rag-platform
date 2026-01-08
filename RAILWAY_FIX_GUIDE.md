# Railway API Deployment Fix

## 🚨 Current Issue
Railway is showing a default Railway page instead of our API endpoints because the wrong backend is being deployed.

## ✅ Solution Steps

### 1. Update Railway Service Configuration

**In Railway Dashboard:**
1. Go to your `cuspera-rag-platform-production` service
2. Click on **Settings** tab
3. Update the following settings:

#### Start Command:
```
python api_backend_simple.py
```

#### Port:
```
8000
```

#### Environment Variables:
```
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 2. Deploy Correct Files

**Ensure these files are in your Railway repository:**
- `api_backend_simple.py` (main backend file)
- `requirements_railway.txt` (dependencies)
- `.env` (API keys)
- `package.json` (deployment config)

### 3. Redeploy Railway Service

**After updating configuration:**
1. Commit and push changes to Railway
2. Railway will automatically redeploy
3. Wait 2-3 minutes for deployment to complete
4. Test the endpoints

### 4. Test API Endpoints

**Health Check:**
```bash
curl https://cuspera-rag-platform-production.railway.app/health
```
Expected response: `{"status": "ok"}`

**Chat Test:**
```bash
curl -X POST https://cuspera-rag-platform-production.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are features of 6Sense?", "product": "6sense"}'
```

Expected response: JSON with answer, sources, context, confidence

## 🔍 Troubleshooting

### If API still shows Railway default page:
1. **Check build logs** in Railway dashboard
2. **Verify file structure** matches repository
3. **Ensure requirements** are properly installed
4. **Check port configuration** (must be 8000)

### If API returns errors:
1. **Check environment variables** for API keys
2. **Verify dependencies** are installed correctly
3. **Check logs** for specific error messages

## 📋 Deployment Checklist

- [ ] Railway Start Command: `python api_backend_simple.py`
- [ ] Railway Port: `8000`
- [ ] Environment variables set (GOOGLE_API_KEY, OPENAI_API_KEY)
- [ ] Repository contains `api_backend_simple.py`
- [ ] Repository contains `requirements_railway.txt`
- [ ] Repository contains `.env` file
- [ ] Service redeployed after changes
- [ ] `/health` endpoint returns `{"status": "ok"}`
- [ ] `/chat` endpoint returns proper responses

## 🚀 Expected Result

After following these steps:
- Railway API will serve our endpoints instead of default page
- Streamlit Cloud app will connect to working API
- Chat functionality will work with real RAG pipeline
- No more 404 errors or fallback responses

## 📞 Support

If issues persist:
1. Check Railway build logs
2. Verify environment variables
3. Test API endpoints manually
4. Check Streamlit Cloud logs for connection errors
