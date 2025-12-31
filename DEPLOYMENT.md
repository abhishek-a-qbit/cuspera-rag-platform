# 🚀 Deployment Guide

## 📋 Prerequisites

1. **GitHub Account**: For code hosting
2. **Google Gemini API Key**: For AI functionality
3. **Render Account**: For backend API hosting (Free tier available)
4. **Streamlit Cloud Account**: For frontend hosting (Free tier available)

## 🎯 Step 1: Prepare GitHub Repository

### 1.1 Install Git (if not already installed)
```bash
# Download Git from https://git-scm.com/download/win
# Or use Windows Package Manager:
winget install Git.Git
```

### 1.2 Initialize Git Repository
```bash
cd "c:/Users/Abhishek A/Desktop/Cuspera"
git init
git add .
git commit -m "Initial commit: Cuspera RAG Platform with enhanced analytics and reports"
```

### 1.3 Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `cuspera-rag-platform`
4. Description: `Advanced RAG platform with 6sense intelligence, interactive analytics, and strategic reports`
5. Make it **Private** (recommended)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 1.4 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/cuspera-rag-platform.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend API to Render

### 2.1 Prepare for Render (Backend API)
1. Go to [Render](https://render.com)
2. Sign up/login with GitHub
3. Click "New" → "Web Service"
4. Select your `cuspera-rag-platform` repository
5. Configure:

**Build Settings:**
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

**Environment Variables:**
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `PYTHON_VERSION`: `3.11.7`

**Advanced Settings:**
- Health Check Path: `/health`
- Auto-Deploy: `Yes`

### 2.2 Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-3 minutes)
3. Note your API URL: `https://your-app-name.onrender.com`

### 2.3 Test the API
```bash
curl https://your-app-name.onrender.com/health
```

## 🌐 Step 3: Deploy Frontend to Streamlit Cloud

### 3.1 Prepare for Streamlit Cloud
1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Sign up/login with GitHub
3. Click "New app"
4. Select your `cuspera-rag-platform` repository
5. Configure:

**App Settings:**
- Main file path: `app/streamlit_app.py`
- Python version: `3.11`

**Environment Variables:**
- `API_URL`: Your Render API URL (e.g., `https://your-app-name.onrender.com`)
- `GOOGLE_API_KEY`: Your Google Gemini API key

**Advanced Settings:**
- Auto-sleep: `Never` (for better user experience)

### 3.2 Deploy
1. Click "Deploy"
2. Wait for deployment (1-2 minutes)
3. Your app will be available at: `https://your-username-cuspera-rag-platform.streamlit.app`

## 🔐 Step 4: Configure Environment Variables

### Required Environment Variables
```bash
# For both Render and Streamlit Cloud
GOOGLE_API_KEY=your_google_gemini_api_key

# For Streamlit Cloud only
API_URL=https://your-render-app.onrender.com
```

### Getting Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to both Render and Streamlit Cloud environment variables

## ✅ Step 5: Verify Deployment

### 5.1 Test Backend API
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "product": {
    "canonical_name": "6sense Revenue AI",
    "domain": "6sense.com",
    "total_documents": 261,
    "datasets": 23
  },
  "rag_ready": true,
  "vector_store_ready": true
}
```

### 5.2 Test Frontend
1. Open your Streamlit Cloud URL
2. Test the chat functionality
3. Test the analytics section
4. Test the report generation

## 🎉 Step 6: Share Your Application

### URLs to Share
- **Frontend**: `https://your-username-cuspera-rag-platform.streamlit.app`
- **API Documentation**: `https://your-app-name.onrender.com/docs`

### Features to Showcase
1. **Enhanced Analytics**: Detailed inputs with interactive charts
2. **Strategic Reports**: AI-generated reports with infographics
3. **Hybrid Search**: 9% better accuracy than semantic alone
4. **Real-time Visualizations**: Budget analysis, ROI projections
5. **Google Gemini Integration**: Fast, intelligent responses

## 🔧 Troubleshooting

### Common Issues

**1. API Connection Error**
- Ensure `API_URL` is correctly set in Streamlit Cloud
- Check that Render service is running
- Verify environment variables are set

**2. Google API Errors**
- Validate your Google Gemini API key
- Check API quota limits
- Ensure key is correctly copied (no extra spaces)

**3. Deployment Failures**
- Check `requirements.txt` for correct dependencies
- Verify Python version compatibility
- Review build logs for specific errors

**4. Frontend Issues**
- Clear browser cache
- Check Streamlit Cloud logs
- Verify all environment variables

### Performance Optimization

**For Better Performance:**
- Use Render's paid tier for better resources
- Implement caching for frequently accessed data
- Consider CDN for static assets
- Monitor API usage and optimize queries

## 📊 Monitoring

### Render Monitoring
- Access Render dashboard for API metrics
- Check response times and error rates
- Monitor resource usage

### Streamlit Cloud Monitoring
- View app statistics in Streamlit Cloud
- Monitor user engagement
- Check error logs

## 🔄 Updates and Maintenance

### Updating the Application
1. Make changes to your code
2. Commit and push to GitHub
3. Both Render and Streamlit Cloud will auto-deploy

### Regular Maintenance
- Monitor API usage and costs
- Update dependencies regularly
- Backup important data
- Review and optimize performance

---

## 🎯 Success Metrics

Your deployed application should provide:
- ✅ **99%+ Uptime**: Reliable 24/7 access
- ✅ **Fast Response**: <2 second API responses
- ✅ **Rich Analytics**: Interactive charts and insights
- ✅ **AI-Powered Reports**: Strategic analysis with visualizations
- ✅ **User-Friendly Interface**: Intuitive Streamlit frontend

Congratulations! 🎉 Your Cuspera RAG Platform is now live and ready to impress users!
