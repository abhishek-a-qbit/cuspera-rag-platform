import os
from dotenv import load_dotenv
from data_loader import load_all_datasets
from vector_store import VectorStore
from rag_graph import create_rag_graph, run_rag_query
from config import DATABASE_PATH, GOOGLE_API_KEY
import json

# Load environment variables
load_dotenv()

def initialize_rag_system(rebuild: bool = False):
    """Initialize the RAG system."""
    print("=" * 60)
    print("Initializing RAG System with Gemini API")
    print("=" * 60)
    
    # Check API key
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    print(f"[OK] API Key configured")
    
    # Load datasets
    print("\n[1/3] Loading datasets...")
    documents = load_all_datasets(DATABASE_PATH)
    
    # Initialize vector store
    print("\n[2/3] Setting up vector store...")
    vector_store = VectorStore()
    
    # Index documents
    if rebuild or not os.path.exists("./chroma_db"):
        vector_store.index_documents(documents)
    else:
        vector_store.load_collection()
    
    # Create RAG graph
    print("\n[3/3] Creating RAG graph...")
    graph = create_rag_graph(vector_store)
    
    print("\n" + "=" * 60)
    print("[OK] RAG System Ready!")
    print("=" * 60)
    
    return graph, vector_store


def main():
    """Main function to demonstrate the RAG system."""
    # Initialize
    graph, vector_store = initialize_rag_system(rebuild=False)
    
    # Display stats
    stats = vector_store.get_collection_stats()
    print(f"\nVector Store Stats:")
    print(f"  - Collection: {stats['collection_name']}")
    print(f"  - Documents: {stats['count']}")
    
    # Example queries
    queries = [
        "What are the key capabilities of 6sense Revenue AI?",
        "How does 6sense help with account identification?",
        "What integrations does 6sense support?",
        "What are the pricing options?"
    ]
    
    print("\n" + "=" * 60)
    print("Running RAG Queries")
    print("=" * 60)
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 60)
        
        result = run_rag_query(graph, query)
        
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nDocuments Used: {result['metadata'].get('documents_used', 0)}")
        print(f"Retrieved: {result['metadata'].get('retrieval_count', 0)}")
        
        if result['retrieved_docs']:
            print(f"\nTop Retrieved Documents:")
            for doc in result['retrieved_docs'][:2]:
                print(f"  - {doc['metadata'].get('dataset', 'Unknown')}: {doc['metadata'].get('label', doc['metadata'].get('question', 'N/A'))[:80]}...")
        
        print("\n" + "-" * 60)


def interactive_mode():
    """Run the RAG system in interactive mode."""
    # Initialize
    graph, vector_store = initialize_rag_system(rebuild=False)
    
    print("\n" + "=" * 60)
    print("Interactive RAG Mode - Type 'quit' to exit")
    print("=" * 60)
    
    while True:
        query = input("\n📝 Your question: ").strip()
        
        if query.lower() == 'quit':
            print("\nGoodbye!")
            break
        
        if not query:
            print("Please enter a question.")
            continue
        
        print("\n⏳ Processing...\n")
        result = run_rag_query(graph, query)
        
        print(f"🤖 Answer:\n{result['answer']}")
        print(f"\n📊 Metadata:")
        print(f"   Documents retrieved: {result['metadata'].get('retrieval_count', 0)}")
        print(f"   Documents used: {result['metadata'].get('documents_used', 0)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        main()
