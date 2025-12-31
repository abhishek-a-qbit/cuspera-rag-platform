# 🧠 Cuspera RAG Platform

A sophisticated Retrieval-Augmented Generation (RAG) application focused on 6sense platform intelligence with hybrid search, interactive visualizations, and strategic reporting.

## ✨ Features

### 🎯 Core Capabilities
- **Hybrid Search Engine**: Combines semantic search (60%) + keyword search (40%)
- **Google Gemini Integration**: Fast AI-powered responses
- **Interactive Analytics**: Detailed business scenario analysis with charts
- **Strategic Reports**: AI-generated reports with infographics
- **Real-time Visualizations**: Budget analysis, ROI projections, competitive positioning

### 📊 Analytics Dashboard
- **Detailed Input Collection**: Company details, budget breakdown, tech stack analysis
- **Interactive Charts**: Budget allocation pie charts, timeline impact analysis, ROI projections
- **Feature Categorization**: Core features, integrations, reporting capabilities
- **Competitive Analysis**: Pricing comparisons and market positioning

### 📋 Strategic Reports
- **Enhanced Configuration**: Report types, depth levels, focus areas
- **Rich Visualizations**: Executive summary gauges, KPI dashboards, market analysis
- **Risk Assessment**: Visual risk matrix and mitigation strategies
- **Action Items**: Prioritized recommendations with tracking

## 🚀 Quick Start

### Local Development

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
   # Create .env file with your Google API key
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Start Services**
   ```bash
   # Terminal 1: Backend API
   cd src
   python api_backend.py

   # Terminal 2: Frontend
   streamlit run app/streamlit_app.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

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
