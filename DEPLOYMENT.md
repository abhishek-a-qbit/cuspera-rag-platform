# 🚀 Deployment Guide

## 📊 Step 1: Deploy API to Railway

### Prerequisites
- Railway account
- GitHub repository access

### Steps
1. **Push to GitHub** (if not already done)
2. **Connect Railway to GitHub**
3. **Configure Environment Variables** in Railway:
   ```
   GOOGLE_API_KEY=your_google_api_key
   DATABASE_PATH=./data/chroma.db
   ```

4. **Deploy Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.api_backend:app --host 0.0.0.0 --port 8000`
   - Health Check: `/health`

### Get Railway API URL
After deployment, Railway will provide a URL like:
`https://your-app-name.railway.app`

---

## 🌐 Step 2: Deploy Streamlit App

### Prerequisites
- Streamlit Cloud account
- GitHub repository

### Steps
1. **Update API URL** in Streamlit Cloud:
   - Go to Streamlit Cloud dashboard
   - Add environment variable: `API_URL=https://your-app-name.railway.app`

2. **Connect Streamlit Cloud to GitHub**
3. **Deploy Settings**:
   - Main file path: `app/streamlit_app.py`
   - Python version: 3.11

---

## 🔧 Environment Variables

### Railway (API)
```
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_PATH=./data/chroma.db
```

### Streamlit Cloud (Frontend)
```
API_URL=https://your-railway-app-url.railway.app
```

---

## ✅ Verification

1. **API Health Check**: `https://your-app.railway.app/health`
2. **Streamlit App**: `https://your-app.streamlit.app`

---

## 🚨 Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure API allows all origins
2. **Environment Variables**: Double-check API keys
3. **Database Path**: Ensure persistent storage in Railway
4. **Port Conflicts**: Railway uses port 8000, Streamlit uses 8501

### Debug Commands
```bash
# Check API health
curl https://your-app.railway.app/health

# Check Streamlit logs
# View in Streamlit Cloud dashboard
```
