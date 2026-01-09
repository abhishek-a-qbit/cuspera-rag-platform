#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Testing backend RAG directly...")

try:
    from rag_graph import create_persistent_rag_graph, run_rag_query
    print("✅ RAG graph import successful")
    
    # Test persistent RAG
    rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
    print("✅ Persistent RAG graph created")
    
    # Test query
    result = run_rag_query(rag_graph, "What is the ROI of 6sense for a 50-person startup?")
    print("✅ Query successful")
    print(f"Answer length: {len(result['answer'])}")
    print(f"Sources: {len(result['retrieved_docs'])}")
    print("First 300 chars of answer:")
    print(result['answer'][:300])
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
