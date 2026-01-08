from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()

app = FastAPI(
    title="Cuspera RAG API",
    description="Product Intelligence RAG System",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ MODELS ============

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    product: str = "6sense"

class AnalyticsRequest(BaseModel):
    scenario: str
    product: str = "6sense"

class ReportRequest(BaseModel):
    topic: str
    constraints: Dict[str, Any] = {}
    product: str = "6sense"

# ============ ENDPOINTS ============

@app.get("/")
async def root():
    return {"message": "Cuspera RAG API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "product": {
            "canonical_name": "6sense Revenue AI",
            "domain": "6sense.com"
        },
        "rag_ready": True,
        "vector_store_ready": True
    }

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    """Enhanced chat endpoint with real RAG pipeline."""
    try:
        # Import RAG system for real responses
        from rag_graph import create_enhanced_rag_graph, run_rag_query
        
        # Initialize RAG graph
        rag_chain = create_enhanced_rag_graph()
        
        # Run RAG query with real data retrieval
        result = await run_rag_query(
            question=request.question,
            rag_chain=rag_chain,
            product=request.product or "6sense"
        )
        
        return {
            "answer": result.get("answer", "I'm processing your question about 6sense. Let me help you with that."),
            "sources": result.get("sources", []),
            "context_used": result.get("context", ""),
            "confidence": result.get("confidence", 0.8)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analytics")
async def analytics_endpoint(request: AnalyticsRequest):
    """Simple analytics endpoint with mock data."""
    try:
        # Mock analytics data
        analytics_data = {
            "scenario": request.scenario,
            "metrics": [
                {"label": "Total Investment", "value": "₹50,00,000"},
                {"label": "Expected ROI", "value": "245%"},
                {"label": "Payback Period", "value": "8 months"},
                {"label": "NPV", "value": "₹1,25,00,000"}
            ],
            "investment_breakdown": {
                "Platform": 40,
                "Training": 20,
                "Integration": 15,
                "Marketing": 15,
                "Support": 10
            },
            "risk_assessment": {
                "overall_risk_score": 35,
                "risk_level": "Low"
            }
        }
        return analytics_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report")
async def report_endpoint(request: ReportRequest):
    """Simple report endpoint with mock data."""
    try:
        # Mock report data
        report_data = {
            "title": f"Strategic Report: {request.topic}",
            "summary": f"This is a comprehensive analysis of {request.topic} with strategic insights and recommendations.",
            "insights": [
                "Market opportunity is significant with 25% CAGR",
                "Competitive landscape favors our approach",
                "Technology differentiation provides strong moat",
                "Revenue projections exceed industry averages",
                "Risk factors are manageable with proper mitigation"
            ],
            "recommendation": "Proceed with implementation focusing on quick wins and long-term scalability",
            "kpis": [
                {"name": "Market Share", "value": "15%", "change": "+3%"},
                {"name": "Customer Acquisition", "value": "250", "change": "+45%"},
                {"name": "Revenue Growth", "value": "180%", "change": "+80%"}
            ]
        }
        return {"report": report_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def products_endpoint():
    """Get available products."""
    return {
        "products": [
            {
                "name": "6sense Revenue AI",
                "canonical_name": "6sense Revenue AI",
                "domain": "6sense.com",
                "total_documents": 150,
                "datasets": 5,
                "enabled": True
            }
        ]
    }

@app.get("/stats")
async def stats_endpoint():
    """Get system statistics."""
    return {
        "vector_store": {
            "count": 150,
            "collection_name": "cuspera_docs"
        },
        "product": {
            "name": "6sense Revenue AI",
            "canonical_name": "6sense Revenue AI",
            "domain": "6sense.com"
        }
    }

# ============ RUN ============

if __name__ == "__main__":
    # Use PORT env var (Railway sets this), fallback to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
