# CUSPERA RAG - STREAMLIT POC GUIDE

## Quick Start (2 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy template
cp .env.example .env

# Edit .env and add your Gemini API key
# GOOGLE_API_KEY=your_key_here
```

Get key from: https://makersuite.google.com/app/apikey

### 3. Run POC
```bash
python run_poc.py
```

This will:
- Start FastAPI backend (port 8000)
- Start Streamlit app (port 8501)
- Open browser automatically

---

## What You Get

### 💬 Chat Interface
- Ask natural language questions
- Get answers grounded in real data
- See conversation history
- Suggested follow-ups

### 📊 Analytics
- Define startup scenario (team size, budget, industry)
- Get pricing analysis
- See feature breakdowns
- Integration recommendations

### 📋 Reports
- Generate strategic reports
- Customize parameters (team, budget, timeline, industry)
- Get KPIs, insights, recommendations
- Download as JSON

### ⚙️ Status
- Check API health
- View database statistics
- See available products
- System diagnostics

---

## Architecture

```
Browser (Streamlit UI)
        ↓
  http://localhost:8501
        ↓
Streamlit App
        ↓
  HTTP Requests
        ↓
FastAPI Backend
(http://localhost:8000)
        ↓
LangGraph RAG
        ↓
Vector Store (ChromaDB)
        ↓
6sense Database (23 datasets)
```

---

## File Structure

```
Cuspera/
├── streamlit_app.py       ← Streamlit UI
├── run_poc.py            ← Quick start script
├── api_backend.py        ← FastAPI (already created)
├── rag_graph.py          ← RAG engine
├── vector_store.py       ← ChromaDB
├── data_loader.py        ← Dataset loader
└── Database/             ← Knowledge base (6sense data)
```

---

## Commands

### Start Everything at Once
```bash
python run_poc.py
```

### Start Backend Only
```bash
python api_backend.py
```

### Start Streamlit Only (with backend already running)
```bash
streamlit run streamlit_app.py
```

### Access Streamlit
```
http://localhost:8501
```

### Access API Docs
```
http://localhost:8000/docs
```

---

## Troubleshooting

### "API connection error"
- Make sure `python api_backend.py` is running
- Check `.env` has valid API key
- Try accessing http://localhost:8000/health

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
- Change port in code or kill existing process
- Streamlit: `--server.port 8502`
- FastAPI: Change `port=8000` to `port=8001` in api_backend.py

### "API slow/timeout"
- Gemini API can be slow first time
- Wait 5-10 seconds for response
- Check internet connection

---

## POC Features

✅ **Chat Interface**
- Multi-turn conversation
- Chat history tracking
- Follow-up suggestions
- Source documents

✅ **Analytics**
- Scenario-based analysis
- Interactive sliders
- Pricing comparison
- Feature breakdown

✅ **Reports**
- Strategic report generation
- Customizable parameters
- KPI metrics
- JSON export

✅ **System Status**
- API health check
- Database statistics
- Product information
- System diagnostics

---

## Next Steps (After POC)

1. **Replace with Production UIs**
   - React (Analytics)
   - Custom Dashboard
   - Advanced visualizations

2. **Enhance RAG**
   - Add more products
   - Implement filtering
   - Add re-ranking

3. **Scale Database**
   - Add 10+ products
   - Implement multi-product queries
   - Add competitive analysis

4. **Advanced Features**
   - Real-time pricing
   - Competitor tracking
   - Custom training
   - Multi-modal search

---

## Features at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| Chat | ✅ Working | Conversational RAG |
| Analytics | ✅ Working | Scenario analysis |
| Reports | ✅ Working | Strategic reports |
| API Health | ✅ Working | Endpoint monitoring |
| Data Integration | ✅ Working | 6sense (23 datasets) |
| Scaling Ready | ✅ Ready | Add more products |

---

## Example Queries

### Chat
- "What are the key capabilities?"
- "Tell me about pricing"
- "What integrations are supported?"
- "How does this compare to competitors?"

### Analytics
- Team: 50 people
- Budget: ₹10,000
- Timeline: 6 months
- Industry: B2B SaaS

### Reports
- Topic: "Growth strategy for B2B SaaS"
- Topic: "Lead generation roadmap"
- Topic: "Team productivity optimization"

---

## Performance

- **Response Time**: 2-5 seconds
- **Retrieval Time**: <100ms
- **Generation Time**: 1-4 seconds
- **Concurrent Users**: 5-10 (Streamlit single-threaded)

---

## Tips & Tricks

1. **Faster Testing**: Use cached API responses
2. **Development Mode**: `streamlit run streamlit_app.py --logger.level=debug`
3. **API Testing**: Use `/docs` endpoint for Swagger UI
4. **Data Insights**: Check `/stats` for database info

---

**This is a POC. Use for testing and validation only.**

For production deployment, consider:
- React frontend
- Gunicorn/Uvicorn backend
- PostgreSQL for persistence
- Redis for caching
- Docker containerization

---

**Ready to start?**
```bash
python run_poc.py
```

**Questions?** Check `ARCHITECTURE.md` for detailed system info.
