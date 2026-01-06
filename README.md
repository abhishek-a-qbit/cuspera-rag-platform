# 🧠 Cuspera RAG Platform

A sophisticated Retrieval-Augmented Generation (RAG) application focused on 6sense platform intelligence with OpenAI integration, hybrid search, and interactive analytics.

## ✨ Features

### 🎯 Core Capabilities
- **OpenAI Integration**: GPT-4 powered responses with fallback support
- **Hybrid Search Engine**: Combines semantic search (60%) + keyword search (40%)
- **Local Development**: Complete offline functionality with local API
- **Interactive Analytics**: Detailed business scenario analysis with charts
- **Real-time Visualizations**: Budget analysis, ROI projections, competitive positioning

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
   GOOGLE_API_KEY=your_google_api_key_here  # Optional fallback
   ```

3. **Start Services**
   ```bash
   # Terminal 1: Backend API
   python app.py

   # Terminal 2: Streamlit Frontend
   streamlit run app/streamlit_app.py
   ```

4. **Access the Application**
   - **Streamlit App**: http://localhost:8501
   - **API Backend**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

## 📁 Repository Structure

```
Cuspera/
├── app/                    # Local Streamlit application
│   └── streamlit_app.py   # Main frontend interface
├── src/                    # Backend API and RAG system
│   ├── api_backend.py      # FastAPI backend server
│   ├── rag_graph.py        # RAG pipeline with OpenAI
│   ├── vector_store.py     # Vector database management
│   ├── config.py           # Configuration settings
│   └── data_loader.py      # Data processing utilities
├── Database/               # 6sense knowledge base
│   ├── dataset_01_capabilities.json
│   ├── dataset_02_customerProfiles.json
│   └── ... (23 total datasets)
├── tests/                  # Test suite
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for GPT-4 responses (primary)
- `GOOGLE_API_KEY`: Google Gemini API key (fallback option)

### API Endpoints
- `POST /chat`: Chat interface with RAG responses
- `POST /analytics`: Business scenario analysis
- `GET /health`: Service health check

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
│  │  (Vector DB) │  │  (Gemini)    │  │  (JSON)              │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Technology Stack

- **Frontend**: Streamlit, Plotly, Pandas
- **Backend**: FastAPI, Uvicorn
- **AI/ML**: Google Gemini, Google Embeddings
- **Database**: ChromaDB (Vector Store)
- **Search**: BM25 + Semantic (Hybrid Search)
- **Environment**: Python 3.11+

## 📁 Project Structure

```
Cuspera/
├── app/                    # Streamlit frontend
│   └── streamlit_app.py   # Main application
├── src/                    # Backend services
│   ├── api_backend.py     # FastAPI server
│   ├── rag_graph.py       # RAG pipeline
│   ├── vector_store.py    # Vector database
│   ├── hybrid_search.py   # Search engine
│   └── data_loader.py     # Data processing
├── Database/               # 6sense datasets (23 files)
├── config/                 # Configuration files
├── docs/                   # Documentation
└── requirements.txt        # Dependencies
```

## 🌐 Deployment

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Set environment variables
4. Deploy automatically

### Render (Backend API)
1. Connect GitHub repository to Render
2. Set up as Web Service
3. Configure environment variables
4. Deploy with automatic scaling

## 🔑 Environment Variables

```bash
GOOGLE_API_KEY=your_google_gemini_api_key
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

**Built with ❤️ using Google Gemini, ChromaDB, and Streamlit**
