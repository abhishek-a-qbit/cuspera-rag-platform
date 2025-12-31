"""
Test script for hybrid search integration.
Tests that both semantic and keyword-based retrieval work together.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_cuspera_data
from vector_store import VectorStore


def test_hybrid_search():
    """Test hybrid search functionality."""
    print("=" * 60)
    print("HYBRID SEARCH TEST")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading data...")
    documents = load_cuspera_data()
    print(f"   ✓ Loaded {len(documents)} documents")
    
    # Create vector store with hybrid search enabled
    print("\n2. Initializing vector store with hybrid search...")
    vector_store = VectorStore(use_hybrid=True)
    print("   ✓ Vector store initialized")
    
    # Index documents
    print("\n3. Indexing documents...")
    vector_store.index_documents(documents)
    print("   ✓ Documents indexed")
    
    # Test queries
    test_queries = [
        "What are the main capabilities of this platform?",
        "Tell me about pricing and ROI",
        "How does this integrate with Salesforce?",
        "What security compliance does it offer?",
        "enterprise readiness",
    ]
    
    print("\n4. Testing hybrid retrieval...\n")
    
    for query in test_queries:
        print(f"Query: '{query}'")
        results = vector_store.retrieve(query, top_k=3)
        
        if results:
            for i, doc in enumerate(results, 1):
                score_info = f"combined={doc.get('combined_score', 0):.3f}"
                if 'semantic_score' in doc:
                    score_info += f", semantic={doc['semantic_score']:.3f}"
                if 'keyword_score' in doc:
                    score_info += f", keyword={doc['keyword_score']:.3f}"
                
                search_type = doc.get('search_type', 'hybrid')
                print(f"  {i}. [{search_type}] {score_info}")
                print(f"     {doc['content'][:80]}...")
        else:
            print("  No results found")
        print()
    
    print("=" * 60)
    print("✓ HYBRID SEARCH TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_hybrid_search()
