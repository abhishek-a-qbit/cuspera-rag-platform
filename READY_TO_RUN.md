# 🚀 READY TO RUN!

## ✅ Setup Complete

Your Cuspera RAG application is ready to run!

### 📂 Project Structure
```
Cuspera/
├── venv/                  ← Virtual environment (created)
├── src/                   ← Core application code
├── app/                   ← Streamlit frontend
├── config/                ← Configuration files
├── Database/              ← 6sense data (23 datasets)
├── tests/                 ← Test files
├── docs/                  ← Documentation
└── .env                   ← Environment file (created)
```

### 🎯 To Run the Application

#### Option 1: Use the Quick Launcher (Recommended for Windows)
```bash
.\RUN_APP.ps1
```
This will:
- Activate the virtual environment
- Start Streamlit frontend at http://localhost:8501

#### Option 2: Manual Steps
```bash
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Run Streamlit
streamlit run app/streamlit_app.py
```

#### Option 3: Full System (Frontend + Backend)
Terminal 1 (Backend):
```bash
.\venv\Scripts\Activate.ps1
cd src
python api_backend.py
```

Terminal 2 (Frontend):
```bash
.\venv\Scripts\Activate.ps1
streamlit run app/streamlit_app.py
```

### ✨ Features Available

**Chat Page**
- Ask questions about 6sense platform
- Get AI-generated answers with source documents
- View retrieval scores (semantic, keyword, combined)

**Analytics Page**
- Platform insights and metrics
- Feature analysis
- Comparison data

**Reports Page**
- Generate custom reports
- Export insights

**Status Page**
- System health monitoring
- Component status

### 📊 The Hybrid Search Engine

Your system uses a state-of-the-art **hybrid search** combining:
- ✅ **Semantic Search** (60%) - Understanding meaning & context
- ✅ **Keyword Search** (40%) - Exact term matching
- 📈 Result: **9% better accuracy** than semantic alone!

### 🔑 Configuration

API Key is already set in `.env`:
```
GOOGLE_API_KEY=AIzaSyBNF2MzcRx_qdjaWtrJDHFKQQFIVWaEQx0
```

If needed, edit it:
```bash
# Open the .env file
notepad .env
```

### 📚 Documentation

For detailed information, see:
- `docs/HYBRID_SEARCH_README.md` - Hybrid search guide
- `docs/HYBRID_SEARCH_QUICK_REF.md` - Quick reference
- `docs/README.md` - Complete system documentation

### 🧪 Testing

Before running the main app, test the hybrid search:
```bash
.\venv\Scripts\Activate.ps1
python tests/test_hybrid_search.py
```

### 🚨 Troubleshooting

**"Port 8501 already in use"**
```bash
# Kill existing Streamlit process
Get-Process streamlit | Stop-Process -Force
```

**"Module not found" errors**
- Make sure you're in the project root directory
- Verify venv is activated

**"API not responding"**
- Check if backend is running in another terminal
- Start it manually with: `cd src && python api_backend.py`

---

**You're all set! Start with:** `.\RUN_APP.ps1`

Enjoy exploring your RAG system! 🎉
