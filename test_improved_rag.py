#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_graph import create_persistent_rag_graph, run_rag_query

print("Testing IMPROVED RAG with proper LLM generation...")

try:
    rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
    result = run_rag_query(rag_graph, "What is the ROI of 6sense for a 50-person startup?")
    
    print("=" * 60)
    print("🎯 IMPROVED RAG RESPONSE:")
    print("=" * 60)
    print(f"Question: {result['question']}")
    print(f"Sources Found: {len(result['retrieved_docs'])}")
    print("-" * 60)
    print("ANSWER:")
    print(result['answer'])
    print("-" * 60)
    print("✅ SUCCESS: Proper LLM generation working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
