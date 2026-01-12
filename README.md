# 🧠 Cuspera RAG Platform

A Retrieval-Augmented Generation (RAG) application focused on B2B software intelligence (6sense-centric) with a FastAPI backend and Streamlit frontend.

## ✨ Features

### 🎯 Core Capabilities
- **LLM Integration**: OpenAI (GPT) and/or Google Gemini (configurable via environment variables)
- **Hybrid Search Engine**: Combines semantic search (60%) + keyword search (40%)
- **Local Development**: Local FastAPI backend + Streamlit frontend
- **Interactive Analytics**: Detailed business scenario analysis with charts
- **Real-time Visualizations**: Budget analysis, ROI projections, competitive positioning

### 🎲 Question Generator + Metrics
- **RAG-powered question generation** via API
- **Four-dimensional evaluation** based on `METRICS.txt`:
  - Coverage
  - Specificity
  - Insightfulness
  - Groundedness
- **Score fusion** (statistical + LLM score normalization) and `overall_pass` flag

### 📊 Analytics Dashboard
- **Detailed Input Collection**: Company details, budget breakdown, tech stack analysis
- **Interactive Charts**: Budget allocation pie charts, timeline impact analysis, ROI projections
- **Feature Categorization**: Core features, integrations, reporting capabilities
- **Competitive Analysis**: Pricing comparisons and market positioning

### 🚀 Local Development Setup

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd Cuspera
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   # Copy .env.example to .env and add your API keys
   cp .env.example .env
   # Edit .env with your keys:
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here  # Optional (Gemini)
   ```

3. **Start Services**
   ```bash
   # Terminal 1: Backend API (FastAPI)
   python -m uvicorn api_backend_simple:app --host 0.0.0.0 --port 8000 --reload

   # Terminal 2: Streamlit Frontend
   streamlit run app/cuspera_supreme.py
   ```

4. **Access the Application**
   - **Streamlit App**: http://localhost:8501
   - **API Backend**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

## 📁 Repository Structure

```
Cuspera/
├── app/                         # Streamlit application
│   ├── cuspera_supreme.py        # Main UI
│   └── cuspera_supreme_clean.py  # Cleaned variant (optional)
├── src/                         # RAG system + utilities
│   ├── rag_graph.py              # RAG pipeline (answer + question_generation)
│   ├── data_driven_question_generator.py  # /generate-questions logic
│   ├── vector_store.py           # Vector store
│   ├── persistent_vector_store.py
│   ├── config.py                 # Env-driven configuration
│   └── data_loader.py            # Dataset loader
├── api_backend_simple.py         # FastAPI backend server
├── Database/               # 6sense knowledge base
│   ├── dataset_01_capabilities.json
│   ├── dataset_02_customerProfiles.json
│   └── ... (23 total datasets)
├── tests/                  # Test suite
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── METRICS.txt             # Metric definitions (Coverage/Specificity/Insightfulness/Groundedness)
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Enables OpenAI model usage (recommended)
- `GOOGLE_API_KEY`: Enables Gemini model usage (optional)

### API Endpoints
- `POST /chat`: Chat interface with RAG responses
  - Supports `mode` (`answer` | `question_generation`)
  - Supports `style` (`default` | `loose`)
  - Supports `target_count` (for question generation)
- `POST /generate-questions`: Generate questions + metrics using the data-driven generator
- `POST /analytics`: Business scenario analysis
- `GET /health`: Service health check

### Metrics Schema (Question Generation)
Question-level `metrics` follow `METRICS.txt`:
- **Per-dimension**: `*_math` (0–1), `*_llm` (1–5), `*_final` (0–1)
- **Overall**: `overall_score` (0–1), `overall_pass` (bool)
- **Fusion**: `fusion_lambda` (default 0.5)

The `/generate-questions` endpoint also returns an aggregate `metrics` summary:
- `total_questions`, `passed_questions`, `pass_rate`
- `coverage_final_avg`, `specificity_final_avg`, `insightfulness_final_avg`, `groundedness_final_avg`, `overall_score_avg`

## 📊 Dataset Overview

The platform includes 23 datasets with 261 total documents covering:
- Platform capabilities and features
- Customer profiles and use cases
- Pricing insights and ROI metrics
- Integrations and partnerships
- Competitive analysis
- Security and compliance
- FAQ and support information

## 🚀 Ready for Development

Your local Cuspera RAG Platform is now ready for development and testing with:
- OpenAI-powered chat responses
- Complete 6sense knowledge base
- Interactive analytics dashboard
- Clean, maintainable codebase

**Next Steps**: Ready for second dataset integration!

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                           │
├──────────────────────┬──────────────────────┬──────────────────┤
│  Chat Consultant     │  Analytics Engine    │  AI Agent Report │
└──────────────────────┴──────────────────────┴──────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND API (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /chat       - Conversational RAG                         │  │
│  │ /analytics  - Scenario analysis & insights              │  │
│  │ /report     - Strategic report generation               │  │
│  │ /query      - Direct RAG (answer + context)             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Retrieval   │→ │  Generation  │→ │  Structured Output   │ │
│  │  (Vector DB) │  │  (OpenAI GPT-4) │  │  (JSON)              │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Technology Stack

- **Frontend**: Streamlit, Plotly, Pandas
- **Backend**: FastAPI, Uvicorn
- **AI/ML**: OpenAI + Gemini (optional)
- **Database**: ChromaDB (Vector Store)
- **Search**: BM25 + Semantic (Hybrid Search)
- **Environment**: Python 3.11+

## 🌐 Deployment

### Streamlit Cloud (Frontend)
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Set environment variable `OPENAI_API_KEY` (and optionally `GOOGLE_API_KEY`)
4. Deploy automatically

### Railway (Backend API)
1. Connect GitHub repository to Railway
2. Set up as a web service
3. Configure environment variable `OPENAI_API_KEY` (and optionally `GOOGLE_API_KEY`)
4. Deploy with automatic scaling

## 🔑 Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # optional
```

## 📊 Data Sources

The system uses 23 comprehensive datasets about 6sense:
- Capabilities and features
- Customer profiles and quotes
- Metrics and performance data
- Integrations and partnerships
- Competitor analysis
- Pricing insights
- Security and compliance

## 🎯 Use Cases

- **Product Intelligence**: Deep understanding of 6sense platform
- **Competitive Analysis**: Compare 6sense with alternatives
- **ROI Analysis**: Calculate investment returns
- **Implementation Planning**: Strategic deployment guidance
- **Sales Enablement**: Customer conversation preparation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Add tests if applicable
5. Submit pull request

## 📄 License

This project is proprietary and confidential.

## 🆘 Support

For issues and questions:
- Check the [Issues](../../issues) page
- Review the documentation in `/docs`
- Contact the development team

---

**Built with ❤️ using FastAPI, Streamlit, and a RAG pipeline.**
