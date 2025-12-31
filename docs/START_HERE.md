# 🎯 CUSPERA RAG SYSTEM - START HERE

## Welcome! 👋

You have a **complete Retrieval-Augmented Generation (RAG) system** ready to use.

This page is your map to everything.

---

## ⚡ FASTEST START (2 minutes)

```bash
# 1. Get API key
# Go to: https://makersuite.google.com/app/apikey
# Copy your key

# 2. Setup
cp .env.example .env
# Paste API key into .env file

# 3. Install
pip install -r requirements.txt

# 4. Run
python run_poc.py

# 5. Open browser
# http://localhost:8501
```

Done! You're using the RAG system.

---

## 📚 Documentation Map

### For Different Needs:

| Need | Read This | Time |
|------|-----------|------|
| **Just start it** | [QUICK_START.md](QUICK_START.md) | 2 min |
| **Understand POC** | [POC_GUIDE.md](POC_GUIDE.md) | 10 min |
| **Understand everything** | [OVERVIEW.md](OVERVIEW.md) | 15 min |
| **Technical details** | [ARCHITECTURE.md](ARCHITECTURE.md) | 20 min |
| **Deploy to prod** | [DEPLOYMENT.md](DEPLOYMENT.md) | 30 min |
| **Full system guide** | [README.md](README.md) | 40 min |
| **File by file** | [FILE_MANIFEST.md](FILE_MANIFEST.md) | 10 min |

---

## 🚀 What You're Getting

### 💬 Chat Interface
Ask questions in natural language. Get answers grounded in real data.

```
You: "What are the key capabilities?"
System: [Searches database] → [Asks Gemini] → [Returns answer]
```

### 📊 Analytics Engine
Analyze startup scenarios with customizable parameters.

```
You: Set team size, budget, timeline
System: [Finds relevant data] → [Generates insights]
```

### 📋 Strategic Reports
Generate comprehensive strategic analysis automatically.

```
You: "Growth strategy for B2B SaaS"
System: [Retrieves docs] → [Synthesizes with AI] → [Returns report]
```

### ⚙️ System Status
Monitor API health, database stats, and system info.

---

## 🛠️ What's Under the Hood

```
Your Browser
    ↓
Streamlit UI (http://8501)
    ↓
FastAPI Backend (http://8000)
    ↓
LangGraph RAG Pipeline
    ↓
Vector Database (ChromaDB)
    ↓
6sense Knowledge Base (23 datasets)
    ↓
Google Gemini API
```

---

## 📁 Project Structure

```
Cuspera/
├── 🚀 RUN THESE
│   ├── run_poc.py              ← Start everything
│   └── startup.py              ← Auto-setup
│
├── 💻 CORE SYSTEM
│   ├── streamlit_app.py        ← POC UI
│   ├── api_backend.py          ← API server
│   ├── rag_graph.py            ← RAG pipeline
│   ├── vector_store.py         ← Database
│   └── data_loader.py          ← Data loading
│
├── 📚 KNOWLEDGE BASE
│   └── Database/               ← 6sense data (23 files)
│
└── 📖 DOCUMENTATION
    ├── README.md               ← Full guide
    ├── ARCHITECTURE.md         ← Technical
    ├── DEPLOYMENT.md           ← Production
    ├── QUICK_START.md          ← Quick ref
    ├── POC_GUIDE.md            ← POC details
    ├── OVERVIEW.md             ← Overview
    └── FILE_MANIFEST.md        ← Files list
```

---

## ✅ System Status

| Component | Status | Notes |
|-----------|--------|-------|
| **RAG Engine** | ✅ Complete | LangGraph + Gemini |
| **API Backend** | ✅ Complete | FastAPI, 5 endpoints |
| **POC UI** | ✅ Complete | Streamlit, 4 pages |
| **Database** | ✅ Complete | 6sense (23 datasets) |
| **Documentation** | ✅ Complete | Full guides provided |
| **Scaling Ready** | ✅ Ready | Add products anytime |

---

## 🎓 Learning Path

### Level 1: User (5 minutes)
1. Run: `python run_poc.py`
2. Try Chat, Analytics, Reports
3. See it work!

### Level 2: Operator (30 minutes)
1. Read: [POC_GUIDE.md](POC_GUIDE.md)
2. Understand what each page does
3. Learn how to use the system

### Level 3: Developer (1-2 hours)
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Review: `api_backend.py`, `rag_graph.py`
3. Understand the code

### Level 4: Architect (2-3 hours)
1. Read: [DEPLOYMENT.md](DEPLOYMENT.md)
2. Read: [OVERVIEW.md](OVERVIEW.md)
3. Plan scaling strategy

---

## 🎯 Common Tasks

### "I just want to use it"
```bash
python run_poc.py
# Done! Open http://localhost:8501
```

### "I want to understand it"
→ Read [OVERVIEW.md](OVERVIEW.md)

### "I want to modify it"
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

### "I want to deploy it"
→ Read [DEPLOYMENT.md](DEPLOYMENT.md)

### "I want to scale it"
→ See ARCHITECTURE.md section on scaling

### "Something doesn't work"
→ Check POC_GUIDE.md troubleshooting section

### "I need to add a new product"
→ Copy 6sense database structure, place in `Database/[product]/`

---

## 💡 Quick Answers

**Q: What is this?**
A: A RAG system that answers questions using real product data (currently 6sense).

**Q: How do I start?**
A: `python run_poc.py`

**Q: Where's the data?**
A: In `Database/` folder (6sense, 23 datasets)

**Q: Can I add more products?**
A: Yes! Just add folders to `Database/`

**Q: How does it work?**
A: Retrieves data from vector store → Asks Gemini to generate answer

**Q: Is it production-ready?**
A: POC is ready. Production setup in DEPLOYMENT.md

**Q: What's the cost?**
A: Free (Gemini has free tier). Paid after quota.

**Q: Can I modify it?**
A: Yes! All code is in repo.

**Q: How do I deploy?**
A: See DEPLOYMENT.md for full instructions

---

## 🔗 Key URLs

| Resource | URL |
|----------|-----|
| Streamlit App | http://localhost:8501 |
| API Server | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| API Health | http://localhost:8000/health |

---

## 📋 Pre-Setup Checklist

- [ ] Get Gemini API key (https://makersuite.google.com/app/apikey)
- [ ] Have Python 3.9+ installed
- [ ] Clone/download this repository
- [ ] Ready to proceed

---

## 🚀 Let's Go!

### Step 1: Get API Key
Go to: https://makersuite.google.com/app/apikey
Copy your key

### Step 2: Configure
```bash
cp .env.example .env
# Edit .env, paste API key
```

### Step 3: Install
```bash
pip install -r requirements.txt
```

### Step 4: Run
```bash
python run_poc.py
```

### Step 5: Use
Open: http://localhost:8501

---

## 📞 Need Help?

1. **Setup Issues?** → [POC_GUIDE.md](POC_GUIDE.md) - Troubleshooting
2. **Architecture Questions?** → [ARCHITECTURE.md](ARCHITECTURE.md)
3. **How to Deploy?** → [DEPLOYMENT.md](DEPLOYMENT.md)
4. **API Help?** → Visit http://localhost:8000/docs
5. **Everything?** → [README.md](README.md)

---

## 🎉 You're Ready!

```bash
python run_poc.py
```

That's it. Everything else is in the docs.

---

## Next Steps After POC

1. ✅ Run and validate POC
2. 🔄 Replace Streamlit with React UI
3. 🔄 Add more products (Salesforce, HubSpot, etc.)
4. 🔄 Deploy to production
5. 🔄 Scale to hundreds of products

---

**Version**: 1.0.0 | **Status**: ✅ Ready | **Date**: Dec 31, 2025

**Start here**: `python run_poc.py`

---

*Questions? Check the docs. Everything is documented.*
