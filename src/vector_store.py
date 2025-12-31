import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHROMA_DB_PATH, COLLECTION_NAME, GOOGLE_API_KEY, TOP_K_RETRIEVAL
from data_loader import create_searchable_text
from hybrid_search import HybridSearcher


class VectorStore:
    """Vector store for managing embeddings and retrieval."""
    
    def __init__(self, use_hybrid: bool = True, semantic_weight: float = 0.6, keyword_weight: float = 0.4):
        """Initialize the vector store with ChromaDB and Google embeddings.
        
        Args:
            use_hybrid: Whether to use hybrid search (semantic + keyword)
            semantic_weight: Weight for semantic similarity (0-1)
            keyword_weight: Weight for keyword matching (0-1)
        """
        # Initialize embeddings with Google (faster than HuggingFace)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = None
        
        # Initialize hybrid search
        self.use_hybrid = use_hybrid
        self.hybrid_searcher = None
        if use_hybrid:
            self.hybrid_searcher = HybridSearcher(
                semantic_weight=semantic_weight,
                keyword_weight=keyword_weight
            )
    
    def create_collection(self):
        """Create a new collection (drops existing if present)."""
        try:
            self.client.delete_collection(name=COLLECTION_NAME)
            print(f"Deleted existing collection: {COLLECTION_NAME}")
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Created new collection: {COLLECTION_NAME}")
    
    def load_collection(self):
        """Load existing collection."""
        self.collection = self.client.get_collection(name=COLLECTION_NAME)
        print(f"Loaded existing collection: {COLLECTION_NAME}")
    
    def index_documents(self, documents: List[Dict[str, Any]]):
        """Index documents into the vector store."""
        if self.collection is None:
            self.create_collection()
        
        # Prepare documents for indexing
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            ids.append(doc["id"])
            texts.append(create_searchable_text(doc))
            metadatas.append(doc["metadata"])
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"Indexed {len(documents)} documents into vector store")
        
        # Build hybrid search indices
        if self.use_hybrid and self.hybrid_searcher:
            self.hybrid_searcher.collection = self.collection
            self.hybrid_searcher.build_keyword_index(documents)
            print(f"[OK] Hybrid search ready (semantic + keyword)")
    
    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> List[Dict[str, Any]]:
        """Retrieve top-k relevant documents for a query."""
        if self.collection is None:
            self.load_collection()
        
        # Use hybrid search if enabled
        if self.use_hybrid and self.hybrid_searcher:
            # Retrieve more candidates for hybrid ranking
            candidate_k = min(top_k * 2, 20)
            hybrid_results = self.hybrid_searcher.hybrid_search(
                query=query,
                top_k=candidate_k
            )
            
            # Format and return top_k results
            return hybrid_results[:top_k]
        
        # Fall back to semantic-only search using ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results
        retrieved_docs = []
        if results and results["ids"] and len(results["ids"]) > 0:
            for idx, doc_id in enumerate(results["ids"][0]):
                retrieved_docs.append({
                    "id": doc_id,
                    "content": results["documents"][0][idx],
                    "metadata": results["metadatas"][0][idx],
                    "distance": results["distances"][0][idx] if results["distances"] else None,
                    "score": 1 - results["distances"][0][idx] if results["distances"] else 0,
                    "search_type": "semantic"
                })
        
        return retrieved_docs
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        if self.collection is None:
            self.load_collection()
        
        return {
            "collection_name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }
