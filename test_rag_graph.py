#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing RAG Graph...")
    
    # Test the RAG graph
    from rag_graph import create_enhanced_rag_graph, run_rag_query
    
    print("Creating RAG graph...")
    rag_graph = create_enhanced_rag_graph(use_enhanced=True)
    
    print("Testing query...")
    result = run_rag_query(rag_graph, "What is the ROI of 6sense for a 50-person startup?")
    
    print("Query Results:")
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer'][:300]}...")
    print(f"Sources: {len(result.get('retrieved_docs', []))}")
    print(f"Metadata: {result.get('metadata', {})}")
    
    if result.get('retrieved_docs'):
        print("\nTop Sources:")
        for i, doc in enumerate(result['retrieved_docs'][:3]):
            print(f"  {i+1}. {doc.get('metadata', {}).get('dataset', 'Unknown')}")
            print(f"     Content: {doc.get('content', '')[:100]}...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
