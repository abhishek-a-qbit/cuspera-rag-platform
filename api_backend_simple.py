from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
import os
from dotenv import load_dotenv
import json
import sys
import logging

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# ==================== MODELS ====================

class ChatRequest(BaseModel):
    question: str
    product: str = "6sense"

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []
    context: str = "Response generated using RAG pipeline"
    confidence: float = 0.8
    follow_up_suggestions: List[str] = []

class AnalyticsRequest(BaseModel):
    company: str
    industry: str
    budget: int
    timeline: str
    team_size: int

class AnalyticsResponse(BaseModel):
    analytics: Dict[str, Any]

class ReportsRequest(BaseModel):
    topic: str
    report_type: str
    constraints: Dict[str, Any]

class ReportsResponse(BaseModel):
    report: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "Cuspera RAG API"
    backend: str = "api_backend_simple.py"
    rag_ready: bool = True
    vector_store_ready: bool = True

class StatsResponse(BaseModel):
    vector_store: Dict[str, Any]
    product: Dict[str, Any]

class ProductsResponse(BaseModel):
    products: List[Dict[str, Any]]

# ==================== ENDPOINTS ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Cuspera RAG API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/health",
            "/chat", 
            "/analytics",
            "/reports",
            "/stats",
            "/products"
        ]
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint."""
    return HealthResponse()

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """Chat endpoint with complete self-contained RAG system."""
    try:
        # Import self-contained RAG system
        from self_contained_rag import SelfContainedRAG
        
        # Initialize RAG system with data path
        rag = SelfContainedRAG(data_path="./data")
        
        # Process question
        result = rag.query(request.question, request.product)
        
        return ChatResponse(
            answer=result.get("answer"),
            sources=result.get("sources", []),
            context=result.get("context", "Generated using self-contained RAG system"),
            confidence=result.get("confidence", 0.8),
            follow_up_suggestions=result.get("follow_up_suggestions", [])
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            answer=f"I'm having trouble processing your question about '{request.question}'. Please try again or contact support.",
            sources=[],
            context="Error occurred during processing",
            confidence=0.1,
            follow_up_suggestions=["Try rephrasing your question", "Check your network connection"]
        )

@app.post("/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
async def analytics(request: AnalyticsRequest):
    """Analytics endpoint."""
    try:
        # Mock analytics response for now
        analytics_data = {
            "company": request.company,
            "industry": request.industry,
            "metrics": [
                {"label": "Revenue Impact", "value": "+25%", "category": "Growth"},
                {"label": "Lead Quality", "value": "High", "category": "Quality"},
                {"label": "ROI", "value": "3.5x", "category": "Return"},
                {"label": "Customer Satisfaction", "value": "92%", "category": "Satisfaction"}
            ],
            "recommendations": [
                f"Implement {request.product} platform",
                "Focus on high-value accounts",
                "Develop predictive lead scoring"
            ]
        }
        
        return AnalyticsResponse(analytics=analytics_data)
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return AnalyticsResponse(analytics={"error": str(e)})

@app.post("/reports", response_model=ReportsResponse, tags=["Reports"])
async def reports(request: ReportsRequest):
    """Reports endpoint."""
    try:
        # Mock reports response for now
        report_data = {
            "summary": f"Strategic analysis for {request.topic}",
            "recommendation": f"Implement {request.product} for optimal results",
            "insights": [
                f"Market opportunity in {request.industry}",
                f"Competitive advantage for {request.company}",
                "Technology integration benefits"
            ]
        }
        
        return ReportsResponse(report=report_data)
    except Exception as e:
        logger.error(f"Reports error: {e}")
        return ReportsResponse(report={"error": str(e)})

@app.get("/stats", response_model=StatsResponse, tags=["Stats"])
async def stats():
    """Statistics endpoint."""
    try:
        # Mock stats response for now
        stats_data = {
            "vector_store": {
                "count": 1000,
                "collection_name": "documents"
            },
            "product": {
                "name": "6sense",
                "version": "1.0.0",
                "features": ["AI-powered targeting", "Revenue intelligence"]
            }
        }
        
        return StatsResponse(**stats_data)
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return StatsResponse(vector_store={}, product={"error": str(e)})

@app.get("/products", response_model=ProductsResponse, tags=["Products"])
async def products():
    """Products endpoint."""
    try:
        products_data = [
            {
                "name": "6sense",
                "description": "B2B Revenue AI Platform",
                "features": [
                    "AI-powered account identification",
                    "Predictive lead scoring", 
                    "Revenue intelligence",
                    "Market insights"
                ]
            }
        ]
        
        return ProductsResponse(products=products_data)
    except Exception as e:
        logger.error(f"Products error: {e}")
        return ProductsResponse(products=[{"error": str(e)}])

@app.post("/generate-questions", response_model=Dict[str, Any], tags=["Questions"])
async def generate_questions(request: Dict[str, Any]):
    """Generate questions using RAG graph from actual data."""
    try:
        # Import data-driven question generator
        from data_driven_question_generator import generate_data_driven_questions
        
        # Extract parameters
        topic = request.get("topic", None)
        num_questions = request.get("num_questions", 10)
        
        # Generate questions using RAG graph
        questions = generate_data_driven_questions(topic, num_questions)
        
        return {
            "status": "success",
            "questions": questions,
            "topic": topic,
            "num_generated": len(questions),
            "generation_method": "RAG Graph Invoke",
            "data_source": "Self-Contained RAG System"
        }
    except Exception as e:
        logger.error(f"Question generation error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "questions": [],
            "generation_method": "Fallback"
        }

# ==================== START SERVER ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

