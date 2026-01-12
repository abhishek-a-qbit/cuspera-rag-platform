#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_graph import create_persistent_rag_graph, run_rag_query

print("Testing successful response...")

try:
    rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
    result = run_rag_query(rag_graph, "What is the ROI of 6sense?")
    
    # Test creating ChatResponse manually
    from pydantic import BaseModel
    from typing import List, Dict, Any
    
    class ChatResponse(BaseModel):
        answer: str
        sources: List[Dict[str, Any]] = []
        context: str = "Response generated using RAG pipeline"
        confidence: float = 0.8
        follow_up_suggestions: List[str] = []
    
    # Test successful response
    response = ChatResponse(
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
        follow_up_suggestions=[
            "What are the key features of 6sense?",
            "How does 6sense help with revenue growth?", 
            "What industries benefit most from 6sense?",
            "What is the ROI of 6sense for startups?"
        ]
    )
    
    print("✅ ChatResponse created successfully!")
    print(f"Answer length: {len(response.answer)}")
    print(f"Context: {response.context}")
    print(f"Context type: {type(response.context)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
