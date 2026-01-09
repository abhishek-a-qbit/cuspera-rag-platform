#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_graph import create_persistent_rag_graph, run_rag_query

print("Testing API response format...")

try:
    rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
    result = run_rag_query(rag_graph, "What is the ROI of 6sense for a 50-person startup?")
    
    print("Result keys:", result.keys())
    print("Answer type:", type(result.get("answer")))
    print("Metadata type:", type(result.get("metadata", {})))
    print("Retrieval count:", result.get("metadata", {}).get("retrieval_count", "not found"))
    print("Retrieval count type:", type(result.get("metadata", {}).get("retrieval_count", 0)))
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
