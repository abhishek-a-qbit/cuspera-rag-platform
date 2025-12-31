# Cuspera RAG Platform - Complete System

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    THREE FRONTEND INTERFACES                    │
├──────────────────────┬──────────────────────┬──────────────────┤
│  Chat Consultant     │  Analytics Engine    │  AI Agent Report │
│  (cusp_consultant)   │  (cuspera_analytics) │  (cuspera_agent) │
└──────────────────────┴──────────────────────┴──────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI BACKEND API (8000)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /chat       - Conversational RAG                         │  │
│  │ /analytics  - Scenario analysis & insights              │  │
│  │ /report     - Strategic report generation               │  │
│  │ /query      - Direct RAG (answer + context)             │  │
│  │ /retrieve   - Document retrieval only                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LANGGRAPH RAG PIPELINE                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Retrieval   │→ │  Generation  │→ │  Structured Output   │ │
│  │  (Vector DB) │  │  (Gemini)    │  │  (JSON)              │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   VECTOR STORE + KNOWLEDGE BASE                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ChromaDB: 6sense Dataset (23 JSON files)               │  │
│  │  Google Embeddings: Semantic search capability          │  │
│  │  Ready to scale: Add any product's data                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start (5 minutes)

### 1. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# GOOGLE_API_KEY=your_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install fastapi uvicorn
```

### 3. Start Backend API
```bash
python api_backend.py
# Or: uvicorn api_backend:app --reload
# API will be available at http://localhost:8000
```

### 4. Test the System
```bash
# In a new terminal:
python frontend_integration.py
```

## API Endpoints

### Chat Interface
```bash
POST /chat
{
  "question": "What are the key capabilities?",
  "chat_context": ["Previous message 1", "Previous message 2"]
}
```

### Analytics Interface
```bash
POST /analytics
{
  "scenario": "50-person startup with 10k budget"
}
```

### Agent Report
```bash
POST /report
{
  "topic": "Growth strategy for B2B SaaS",
  "constraints": {
    "team_size": 50,
    "budget": 10000,
    "timeline": "6 months"
  }
}
```

### Direct RAG Query
```bash
POST /query
{
  "question": "Tell me about pricing",
  "top_k": 5
}
```

### Retrieve Documents Only
```bash
POST /retrieve
{
  "question": "What features are available?",
  "top_k": 10
}
```

## Frontend Integration

### 1. Chat UI (`cusp_consultant.html`)
```javascript
const adapter = new ChatInterfaceAdapter();
const response = await adapter.handleUserInput("Your question here");
```

### 2. Analytics UI (`cuspera_analytics.txt`)
```javascript
const adapter = new AnalyticsInterfaceAdapter();
const data = await adapter.analyzeScenario("50-person startup with 10k budget");
// data.metrics, data.pricing, data.features ready for React charts
```

### 3. Agent UI (`cuspera_agent.txt`)
```javascript
const adapter = new AgentInterfaceAdapter();
const report = await adapter.generateStrategicReport("Growth strategy...", {
  team_size: 50,
  budget: 10000
});
// report.kpis, report.insights, report.chartData ready for rendering
```

## Data Flow Examples

### Example 1: Chat Flow
```
User: "What are the capabilities?"
  ↓
ChatInterfaceAdapter.handleUserInput()
  ↓
POST /chat with question + history
  ↓
RAG Pipeline:
  1. Retrieve relevant docs from ChromaDB
  2. Pass to Gemini with context
  3. Generate conversational answer
  ↓
Return answer + follow-up suggestions
```

### Example 2: Analytics Flow
```
User: "Analyze 50-person startup scenario"
  ↓
AnalyticsInterfaceAdapter.analyzeScenario()
  ↓
POST /analytics with scenario
  ↓
RAG Pipeline:
  1. Retrieve pricing, metrics, features from DB
  2. Extract structured analytics
  3. Generate insights
  ↓
Return data for React charts (pricing, metrics, features, integrations)
```

### Example 3: Agent Flow
```
User: "Generate growth strategy report"
  ↓
AgentInterfaceAdapter.generateStrategicReport()
  ↓
POST /report with topic + constraints
  ↓
RAG Pipeline:
  1. Retrieve relevant docs based on topic
  2. Pass to Gemini with system prompt
  3. Generate structured JSON report
  ↓
Return: {title, kpis, insights, recommendation, chartData}
```

## Scaling to Multiple Products

Currently optimized for 6sense, but designed for scale:

### Add New Product (e.g., Salesforce)
```
1. Create new dataset folder:
   Database/salesforce/
   - dataset_01_features.json
   - dataset_02_pricing.json
   - etc.

2. Update data_loader.py to scan multiple products:
   def load_all_products():
       products = {}
       for product_dir in Path(DATABASE_PATH).iterdir():
           if product_dir.is_dir():
               products[product_dir.name] = load_product_data(product_dir)
       return products

3. Update vector store to support product filtering:
   def retrieve(self, query, product=None, top_k=5):
       # Filter by product in metadata
       ...

4. Update API endpoints to accept product parameter:
   POST /query
   {
     "question": "...",
     "product": "salesforce"  // or "6sense", "hubspot", etc.
   }
```

## File Structure
```
Cuspera/
├── Database/                    # Knowledge base
│   ├── dataset_01_capabilities.json
│   ├── dataset_02_customerProfiles.json
│   └── ... (23 total)
│
├── config.py                    # Configuration
├── data_loader.py              # Load & parse datasets
├── vector_store.py             # ChromaDB + embeddings
├── rag_graph.py                # LangGraph pipeline
│
├── api_backend.py              # FastAPI server (Port 8000)
├── frontend_integration.py      # Client adapters for UIs
│
├── cusp_consultant.html        # Chat UI
├── cuspera_analytics.txt       # Analytics React component
├── cuspera_agent.txt           # Agent React component
│
├── .env.example                # Environment template
└── requirements.txt            # Python dependencies
```

## Key Features

✅ **Product-Agnostic**: Add any product's data to Knowledge base
✅ **Scalable**: Designed for thousands of products
✅ **Real Data**: All answers grounded in actual datasets
✅ **Structured Output**: JSON for easy UI rendering
✅ **Conversation History**: Context-aware interactions
✅ **Multi-Interface**: Chat, Analytics, Agent reports
✅ **Retrieval Transparency**: See which documents were used

## Troubleshooting

### API not starting?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000
# Kill process or change port in api_backend.py
```

### ChromaDB errors?
```bash
# Delete and rebuild vector store
rm -rf chroma_db
python api_backend.py  # Will rebuild on startup
```

### Gemini API issues?
```bash
# Verify API key in .env
# Check: https://makersuite.google.com/app/apikey
# Ensure internet connection
```

## Next Steps

1. ✅ Get Gemini API key
2. ✅ Configure .env
3. ✅ Run `python api_backend.py`
4. ✅ Test endpoints with `frontend_integration.py`
5. 🔄 Connect React UIs to the API
6. 🔄 Add more products to knowledge base
7. 🔄 Deploy to production

---

**Note**: 6sense is currently the only product in the knowledge base. The system is designed to seamlessly scale to thousands of products when needed.
