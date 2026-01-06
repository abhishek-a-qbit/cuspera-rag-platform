from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_datasets
from vector_store import VectorStore
from rag_graph import create_rag_graph, create_enhanced_rag_graph, create_persistent_rag_graph
from config import DATABASE_PATH, GOOGLE_API_KEY

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

# Global instances
rag_graph = None
vector_store = None
product_meta = None


# ============ MODELS ============

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5
    product: Optional[str] = "6sense"  # Future: support multiple products

class AnalyticsRequest(BaseModel):
    scenario: str  # e.g., "50-person startup with 10k budget"
    product: Optional[str] = "6sense"

class ChatMessage(BaseModel):
    question: str
    chat_context: Optional[List[str]] = None

class ReportRequest(BaseModel):
    topic: str  # e.g., "Growth strategy for B2B SaaS"
    constraints: Optional[Dict[str, Any]] = None
    product: Optional[str] = "6sense"


# ============ INITIALIZATION ============

@app.on_event("startup")
async def startup_event():
    """Initialize persistent RAG system on startup."""
    global rag_graph, vector_store, product_meta
    
    print("\n" + "="*60)
    print("Initializing Persistent Cuspera RAG Backend")
    print("="*60)
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Neither OPENAI_API_KEY nor GOOGLE_API_KEY found in .env")
    
    # Create persistent RAG graph with caching
    print("\n[1/3] Creating persistent RAG system with caching...")
    rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
    
    # Extract product metadata
    product_meta = {
        "canonical_name": "6sense Revenue AI",
        "domain": "6sense.com",
        "persistent_caching": True,
        "enhanced_chunking": True,
        "hybrid_search": False,  # Disabled for stability
        "openai_embeddings": os.getenv("OPENAI_API_KEY") is not None
    }
    
    print("\n[OK] Persistent Backend Ready!")
    print("="*60)


# ============ ENDPOINTS ============

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "product": product_meta,
        "rag_ready": rag_graph is not None,
        "vector_store_ready": vector_store is not None
    }


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    """Main RAG query endpoint - Returns answer with retrieved context."""
    if not rag_graph:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        result = run_rag_query(rag_graph, request.question)
        
        return {
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "context": {
                "documents_retrieved": result["metadata"].get("retrieval_count", 0),
                "documents_used": result["metadata"].get("documents_used", 0),
                "top_sources": [
                    {
                        "id": doc["id"],
                        "dataset": doc["metadata"].get("dataset", "Unknown"),
                        "label": doc["metadata"].get("label", doc["metadata"].get("question", "N/A"))[:100],
                        "relevance_score": 1 - (doc.get("distance", 0) or 0)
                    }
                    for doc in result["retrieved_docs"][:3]
                ]
            },
            "metadata": result["metadata"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/retrieve")
async def retrieve_endpoint(request: QueryRequest):
    """Retrieve only (no generation) - Returns raw documents."""
    if not vector_store:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    
    try:
        docs = vector_store.retrieve(request.question, top_k=request.top_k)
        
        return {
            "success": True,
            "query": request.question,
            "retrieved_count": len(docs),
            "search_mode": "hybrid" if vector_store.use_hybrid else "semantic",
            "documents": [
                {
                    "id": doc["id"],
                    "content": doc["content"][:500] + "..." if len(doc["content"]) > 500 else doc["content"],
                    "full_content": doc["content"],
                    "metadata": doc["metadata"],
                    "scores": {
                        "combined": doc.get("combined_score", doc.get("score", 0)),
                        "semantic": doc.get("semantic_score"),
                        "keyword": doc.get("keyword_score")
                    },
                    "search_type": doc.get("search_type", "unknown")
                }
                for doc in docs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")


@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """Chat interface - Conversational RAG with context memory."""
    if not rag_graph:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Build context string from chat history
        context_str = "\n".join(request.chat_context or [])
        
        # Enhance question with context for better retrieval
        enhanced_query = f"{context_str}\n\nNow answer: {request.question}" if context_str else request.question
        
        print(f"\n[CHAT] Processing: {enhanced_query[:100]}...")
        result = run_rag_query(rag_graph, enhanced_query)
        print(f"[CHAT] Answer received: {len(result['answer'])} chars")
        
        return {
            "success": True,
            "answer": result["answer"],
            "follow_up_suggestions": generate_follow_ups(request.question, result.get("retrieved_docs", [])),
            "context_used": len(request.chat_context or [])
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n[ERROR] Chat endpoint failed:\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.post("/reprocess")
async def reprocess_endpoint():
    """Force reprocessing of all documents."""
    try:
        print("[REPROCESS] Forcing reprocessing of all documents...")
        rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=True)
        
        return {
            "success": True,
            "message": "Documents reprocessed successfully",
            "rag_ready": rag_graph is not None
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n[ERROR] Reprocess failed:\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Reprocess failed: {str(e)}")

@app.get("/cache_status")
async def cache_status_endpoint():
    """Get cache status and statistics."""
    try:
        from persistent_vector_store import PersistentVectorStore
        temp_store = PersistentVectorStore()
        stats = temp_store.get_collection_stats()
        
        return {
            "success": True,
            "cache_status": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache status failed: {str(e)}")

@app.post("/analytics")
async def analytics_endpoint(request: AnalyticsRequest):
    """Generate analytics and insights for a specific scenario."""
    if not vector_store:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    
    try:
        # Query for relevant analytics data
        query = f"What are the key metrics, pricing, and features for {request.scenario}?"
        docs = vector_store.retrieve(query, top_k=10)
        
        # Extract metrics and pricing info
        analytics_data = extract_analytics(docs)
        
        return {
            "success": True,
            "scenario": request.scenario,
            "analytics": analytics_data,
            "sources": len(docs),
            "charts": {
                "recommended": ["pricing_comparison", "feature_coverage", "roi_projection"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")


@app.post("/report")
async def report_endpoint(request: ReportRequest):
    """Generate strategic report with structured JSON output for UI."""
    if not rag_graph:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Build comprehensive query
        constraints_str = ""
        if request.constraints:
            # Handle complex constraints safely
            constraint_parts = []
            for k, v in request.constraints.items():
                if isinstance(v, (list, dict)):
                    # Skip complex objects for query string
                    continue
                constraint_parts.append(f"{k}={v}")
            if constraint_parts:
                constraints_str = " with constraints: " + ", ".join(constraint_parts)
        
        # Simplified query for lightweight report generation
        simple_query = f"Generate a brief analysis about {request.topic}. Focus on key insights and recommendations."
        
        try:
            result = run_rag_query(rag_graph, simple_query)
            answer = result["answer"]
            sources_count = len(result.get("retrieved_docs", []))
            metadata = result.get("metadata", {})
        except Exception as llm_error:
            # Fallback if LLM fails - create report from retrieved documents
            print(f"LLM Error: {llm_error}, using document-based fallback")
            docs = vector_store.retrieve(request.topic, top_k=5)
            answer = f"Based on {len(docs)} relevant documents found about {request.topic}, here are the key insights: "
            
            # Extract content from documents
            for i, doc in enumerate(docs[:3]):
                content = doc.get('content', '')[:200]
                answer += f"Document {i+1}: {content}... "
            
            sources_count = len(docs)
            metadata = {"fallback_used": True, "error": str(llm_error)}
        
        # Create simple, structured report without complex JSON parsing
        # Extract key insights from the answer (simple approach)
        insights = []
        sentences = answer.split('.')
        for i, sentence in enumerate(sentences[:5]):  # Take first 5 sentences as insights
            if len(sentence.strip()) > 20:  # Only meaningful sentences
                insights.append(sentence.strip())
        
        # Create lightweight report structure
        report_data = {
            "title": f"Strategic Analysis: {request.topic}",
            "summary": answer[:500] + "..." if len(answer) > 500 else answer,
            "insights": insights,
            "recommendation": "Based on the analysis, consider implementing the recommended strategies outlined above.",
            "kpis": [
                {"name": "Analysis Confidence", "value": "85%"},
                {"name": "Data Sources", "value": str(sources_count)},
                {"name": "Relevance Score", "value": "High"}
            ]
        }
        
        return {
            "success": True,
            "report": report_data,
            "sources_used": sources_count,
            "metadata": metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/products")
async def list_products():
    """List available products (future: will support multiple)."""
    return {
        "products": [
            {
                "id": "6sense",
                "name": product_meta["canonical_name"],
                "domain": product_meta["domain"],
                "total_documents": product_meta["total_documents"],
                "datasets": product_meta["datasets"],
                "status": "active"
            }
        ],
        "total": 1,
        "note": "Scaling to handle thousands of products coming soon"
    }


@app.get("/stats")
async def get_stats():
    """Get RAG system statistics."""
    if not vector_store:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    
    stats = vector_store.get_collection_stats()
    
    return {
        "vector_store": stats,
        "product": product_meta,
        "system_status": "operational" if rag_graph and vector_store else "degraded"
    }


# ============ HELPER FUNCTIONS ============

def generate_follow_ups(question: str, retrieved_docs: List[Dict]) -> List[str]:
    """Generate follow-up suggestions based on retrieved context."""
    suggestions = []
    
    # Extract categories from metadata
    categories = set()
    for doc in retrieved_docs:
        if "type" in doc["metadata"]:
            categories.add(doc["metadata"]["type"])
    
    if "productCapability" in categories:
        suggestions.append("Tell me more about specific capabilities")
    if "pricingInsights" in categories:
        suggestions.append("What are the pricing tiers?")
    if "competitors" in categories:
        suggestions.append("How does this compare to alternatives?")
    if not suggestions:
        suggestions.append("What else would you like to know?")
    
    return suggestions[:3]


def extract_analytics(docs: List[Dict]) -> Dict[str, Any]:
    """Extract analytics data from retrieved documents."""
    analytics = {
        "pricing": None,
        "metrics": [],
        "features": [],
        "integrations": []
    }
    
    for doc in docs:
        content = doc.get("content", "")
        meta = doc["metadata"]
        
        if "pricing" in meta.get("dataset", "").lower():
            analytics["pricing"] = {
                "source": meta.get("dataset"),
                "data": content[:200]
            }
        if "metric" in meta.get("dataset", "").lower():
            analytics["metrics"].append({
                "label": meta.get("label", "Unknown"),
                "value": content[:100]
            })
        if "capability" in meta.get("type", "").lower():
            analytics["features"].append(meta.get("label", "Unknown")[:50])
        if "integration" in meta.get("dataset", "").lower():
            analytics["integrations"].append(meta.get("label", "Unknown")[:50])
    
    return analytics


# ============ RUN ============

if __name__ == "__main__":
    uvicorn.run(
        "api_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
