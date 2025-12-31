# 🚀 CUSPERA POC - QUICK REFERENCE

## One-Command Start
```bash
python run_poc.py
```

That's it! The script will:
1. Check your API key
2. Start FastAPI backend
3. Start Streamlit app
4. Open browser automatically

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Streamlit UI | http://localhost:8501 | Main interface |
| FastAPI Docs | http://localhost:8000/docs | API documentation |
| API Health | http://localhost:8000/health | Check API status |

## What Each Page Does

### 💬 Chat
```
Ask: "What are the capabilities?"
↓
Get: AI answer + sources + follow-ups
```

### 📊 Analytics
```
Set: Team size, Budget, Timeline, Industry
↓
Get: Pricing analysis, Features, Integrations
```

### 📋 Reports
```
Enter: Topic + Constraints
↓
Get: Strategic report with KPIs & insights
```

### ⚙️ Status
```
View: API health, Database stats, Products
```

## If Something Breaks

| Problem | Solution |
|---------|----------|
| "Cannot connect to API" | Run `python api_backend.py` in new terminal |
| "API key error" | Edit `.env` with valid Gemini API key |
| "Port in use" | Kill existing process or change port |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Slow responses" | Gemini API can be slow, wait 5-10 seconds |

## File Manifest

```
Cuspera/
├── streamlit_app.py      ← POC UI (you are here)
├── run_poc.py           ← Quick start
├── api_backend.py       ← API backend
├── rag_graph.py         ← RAG engine
├── vector_store.py      ← Database
├── data_loader.py       ← Data loader
├── config.py            ← Settings
├── Database/            ← Knowledge base
├── requirements.txt     ← Dependencies
├── .env                 ← API key (CREATE THIS!)
└── POC_GUIDE.md         ← Full guide
```

## Setup Checklist

- [ ] Have Gemini API key? Get from https://makersuite.google.com/app/apikey
- [ ] Create `.env` file with API key
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python run_poc.py`
- [ ] Open http://localhost:8501

## Example Interactions

### Chat Example
```
You: What are the main capabilities?
AI: [Shows answer grounded in real data]
   Follow-ups:
   - Tell me about pricing
   - What about integrations?
```

### Analytics Example
```
Team Size: 50
Budget: ₹10,000
Timeline: 6 months
Industry: B2B SaaS
↓
Results: Pricing analysis, features, integrations
```

### Report Example
```
Topic: Growth strategy for B2B SaaS
Budget: ₹10,000
↓
Results: Strategic report with KPIs, insights, recommendations
```

## Tips

1. **First response is slow** - Initializing embeddings, give it 5-10 seconds
2. **Chat history persists** - Until you click "Clear History"
3. **Scenario analysis is fast** - Data already in vector store
4. **Reports are comprehensive** - Uses Gemini to synthesize insights

## Next Steps

After POC validation:
1. Replace Streamlit with React
2. Add more products
3. Implement advanced features
4. Deploy to production

## Support

- Full architecture: See `ARCHITECTURE.md`
- Deployment guide: See `DEPLOYMENT.md`
- API docs: Visit http://localhost:8000/docs

---

**Status**: ✅ POC Ready | 🚀 Production Ready | 📈 Scalable

**Start now**: `python run_poc.py`
