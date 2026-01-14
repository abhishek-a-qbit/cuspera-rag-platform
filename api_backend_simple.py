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
advanced_agent_instance = None

def get_rag_graph():
    """Get or create RAG graph instance."""
    global rag_graph_instance
    if rag_graph_instance is None:
        logger.info("Creating persistent RAG graph...")
        from rag_graph import create_persistent_rag_graph
        rag_graph_instance = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
        logger.info("RAG graph created and cached")
    return rag_graph_instance

def get_advanced_agent():
    """Get or create advanced AI agent instance."""
    global advanced_agent_instance
    if advanced_agent_instance is None:
        logger.info("Creating advanced AI agent...")
        try:
            from advanced_ai_agent import AdvancedAIAgent
            advanced_agent_instance = AdvancedAIAgent()
            logger.info("Advanced AI agent created successfully")
        except Exception as e:
            logger.error(f"Failed to create advanced agent: {e}")
            advanced_agent_instance = None
    return advanced_agent_instance

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
            "/products",
            "/generate-questions"
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
    """Generate questions AND answers with full metrics for both."""
    try:
        # Import data-driven question generator
        from data_driven_question_generator import generate_data_driven_questions
        
        # Extract parameters
        topic = request.get("topic", None)
        num_questions = request.get("num_questions", 10)
        
        logger.info(f"Generating {num_questions} questions for topic: {topic}")
        
        # Generate questions (this now includes answers and answer metrics)
        questions = generate_data_driven_questions(topic, num_questions)
        
        logger.info(f"Generated {len(questions)} question-answer pairs")
        
        # Calculate summary metrics for BOTH questions and answers
        total_questions = len(questions)
        
        # Question metrics
        passed_questions = 0
        coverage_q_sum = 0.0
        specificity_q_sum = 0.0
        insightfulness_q_sum = 0.0
        groundedness_q_sum = 0.0
        overall_q_sum = 0.0
        
        # Answer metrics
        passed_answers = 0
        coverage_a_sum = 0.0
        specificity_a_sum = 0.0
        insightfulness_a_sum = 0.0
        groundedness_a_sum = 0.0
        overall_a_sum = 0.0
        
        for q in questions:
            # Question metrics
            q_metrics = q.get("metrics", {})
            if q_metrics.get("overall_pass"):
                passed_questions += 1
            
            coverage_q_sum += float(q_metrics.get("coverage_final", 0.0))
            specificity_q_sum += float(q_metrics.get("specificity_final", 0.0))
            insightfulness_q_sum += float(q_metrics.get("insightfulness_final", 0.0))
            groundedness_q_sum += float(q_metrics.get("groundedness_final", 0.0))
            overall_q_sum += float(q_metrics.get("overall_score", 0.0))
            
            # Answer metrics
            a_metrics = q.get("answer_metrics", {})
            if a_metrics.get("overall_pass"):
                passed_answers += 1
            
            coverage_a_sum += float(a_metrics.get("coverage_final", 0.0))
            specificity_a_sum += float(a_metrics.get("specificity_final", 0.0))
            insightfulness_a_sum += float(a_metrics.get("insightfulness_final", 0.0))
            groundedness_a_sum += float(a_metrics.get("groundedness_final", 0.0))
            overall_a_sum += float(a_metrics.get("overall_score", 0.0))
        
        denom = float(total_questions) if total_questions > 0 else 1.0
        
        metrics_summary = {
            "total_questions": total_questions,
            
            # Question metrics
            "passed_questions": passed_questions,
            "question_pass_rate": (passed_questions / denom) * 100.0,
            "coverage_q_avg": coverage_q_sum / denom,
            "specificity_q_avg": specificity_q_sum / denom,
            "insightfulness_q_avg": insightfulness_q_sum / denom,
            "groundedness_q_avg": groundedness_q_sum / denom,
            "overall_q_avg": overall_q_sum / denom,
            
            # Answer metrics
            "passed_answers": passed_answers,
            "answer_pass_rate": (passed_answers / denom) * 100.0,
            "coverage_a_avg": coverage_a_sum / denom,
            "specificity_a_avg": specificity_a_sum / denom,
            "insightfulness_a_avg": insightfulness_a_sum / denom,
            "groundedness_a_avg": groundedness_a_sum / denom,
            "overall_a_avg": overall_a_sum / denom,
            
            # Combined metrics
            "combined_pass_rate": ((passed_questions + passed_answers) / (denom * 2)) * 100.0
        }
        
        logger.info(f"Question pass rate: {metrics_summary['question_pass_rate']:.1f}%")
        logger.info(f"Answer pass rate: {metrics_summary['answer_pass_rate']:.1f}%")
        
        return {
            "status": "success",
            "questions": questions,
            "topic": topic,
            "num_generated": len(questions),
            "metrics": metrics_summary,
            "generation_method": "RAG Graph with Real LLM Grading",
            "data_source": "Self-Contained RAG System"
        }
        
    except Exception as e:
        logger.error(f"Question generation error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "status": "error",
            "error": str(e),
            "questions": [],
            "generation_method": "Failed"
        }

# ==================== ADVANCED AI AGENT ENDPOINTS ====================

class AdvancedChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class AdvancedChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    metrics: Dict[str, Any] = {}
    navigation_intent: Optional[str] = None
    tools_used: List[str] = []
    session_id: str

@app.post("/advanced-chat", response_model=AdvancedChatResponse, tags=["Advanced Agent"])
async def advanced_chat(request: AdvancedChatRequest):
    """Advanced AI Agent chat endpoint with LangGraph state management."""
    try:
        agent = get_advanced_agent()
        if agent is None:
            raise HTTPException(status_code=503, detail="Advanced agent not available")
        
        # Use the advanced agent
        result = agent.chat(request.message, request.session_id)
        
        return AdvancedChatResponse(
            response=result.get("response", ""),
            sources=result.get("sources", []),
            metrics=result.get("metrics", {}),
            navigation_intent=result.get("navigation_intent"),
            tools_used=result.get("tools_used", []),
            session_id=result.get("session_id", request.session_id)
        )
        
    except Exception as e:
        logger.error(f"Advanced chat error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return AdvancedChatResponse(
            response=f"I'm having trouble processing your request: {str(e)}",
            sources=[],
            metrics={},
            navigation_intent=None,
            tools_used=["error"],
            session_id=request.session_id
        )

@app.get("/agent-history/{session_id}", tags=["Advanced Agent"])
async def get_agent_history(session_id: str):
    """Get conversation history for a session."""
    try:
        agent = get_advanced_agent()
        if agent is None:
            raise HTTPException(status_code=503, detail="Advanced agent not available")
        
        history = agent.get_conversation_history(session_id)
        return {"session_id": session_id, "history": history}
        
    except Exception as e:
        logger.error(f"History error: {e}")
        return {"session_id": session_id, "history": [], "error": str(e)}

# ==================== START SERVER ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)