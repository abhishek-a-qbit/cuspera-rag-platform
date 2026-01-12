import logging
import sys
import os
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global RAG instance to avoid recreating
rag_graph_instance = None

def get_rag_graph():
    """Get or create RAG graph instance."""
    global rag_graph_instance
    if rag_graph_instance is None:
        logger.info("Creating persistent RAG graph...")
        from rag_graph import create_persistent_rag_graph
        rag_graph_instance = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
        logger.info("RAG graph created and cached")
    return rag_graph_instance

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


@app.on_event("startup")
async def _warm_rag_graph_on_startup():
    start = time.time()
    try:
        get_rag_graph()
        logger.info(f"RAG warmup complete in {time.time() - start:.2f}s")
    except Exception as e:
        logger.error(f"RAG warmup failed after {time.time() - start:.2f}s: {e}")

# ==================== MODELS ====================

class ChatRequest(BaseModel):
    question: str
    product: str = "6sense"
    mode: Optional[str] = None  # answer | question_generation
    style: Optional[str] = None  # default | loose
    target_count: Optional[int] = None

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
    """Chat endpoint using persistent RAG graph with caching."""
    try:
        overall_start = time.time()
        # Import persistent RAG graph
        from rag_graph import create_persistent_rag_graph, run_rag_query
        
        # Get or create RAG graph instance
        graph_start = time.time()
        rag_graph = get_rag_graph()
        logger.info(f"/chat rag_graph ready in {time.time() - graph_start:.2f}s")
        
        # Process question using persistent RAG graph
        query_start = time.time()
        result = run_rag_query(
            rag_graph,
            request.question,
            mode=request.mode,
            style=request.style,
            target_count=request.target_count,
        )
        logger.info(
            f"/chat run_rag_query completed in {time.time() - query_start:.2f}s; total {time.time() - overall_start:.2f}s"
        )
        
        # Format response for API
        return ChatResponse(
            answer=result.get("answer", "I'm having trouble processing your question."),
            sources=[
                {
                    "id": doc.get("id", "unknown"),
                    "content": doc.get("content", "")[:200] + "..." if len(doc.get("content", "")) > 200 else doc.get("content", ""),
                    "metadata": doc.get("metadata", {})
                }
                for doc in result.get("retrieved_docs", [])
            ],
            context=str(result.get("metadata", {}).get("retrieval_count", 0)),
            confidence=result.get("confidence", 0.6),
           
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
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

        total_questions = int(len(questions))
        passed_questions = 0
        coverage_final_sum = 0.0
        specificity_final_sum = 0.0
        insightfulness_final_sum = 0.0
        groundedness_final_sum = 0.0
        overall_score_sum = 0.0

        for q in questions:
            m = (q or {}).get("metrics") or {}
            if bool(m.get("overall_pass")):
                passed_questions += 1
            coverage_final_sum += float(m.get("coverage_final") or 0.0)
            specificity_final_sum += float(m.get("specificity_final") or 0.0)
            insightfulness_final_sum += float(m.get("insightfulness_final") or 0.0)
            groundedness_final_sum += float(m.get("groundedness_final") or 0.0)
            overall_score_sum += float(m.get("overall_score") or 0.0)

        denom = float(total_questions) if total_questions else 1.0
        metrics_summary = {
            "total_questions": total_questions,
            "passed_questions": passed_questions,
            "pass_rate": (passed_questions / denom) * 100.0 if total_questions else 0.0,
            "coverage_final_avg": coverage_final_sum / denom,
            "specificity_final_avg": specificity_final_sum / denom,
            "insightfulness_final_avg": insightfulness_final_sum / denom,
            "groundedness_final_avg": groundedness_final_sum / denom,
            "overall_score_avg": overall_score_sum / denom,
        }
        
        return {
            "status": "success",
            "questions": questions,
            "topic": topic,
            "num_generated": len(questions),
            "metrics": metrics_summary,
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

