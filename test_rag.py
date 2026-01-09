#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from self_contained_rag import SelfContainedRAG
    
    print("Testing RAG system...")
    rag = SelfContainedRAG(data_path="./Database")
    
    print(f"Documents loaded: {len(rag.documents)}")
    
    if rag.documents:
        print("First document sample:")
        print(rag.documents[0])
        
        print("\nTesting query...")
        result = rag.query("What is the ROI of 6sense?", "6sense")
        print("Query result:")
        print(result)
    else:
        print("No documents loaded!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
