try:
    import chromadb
except Exception:
    chromadb = None

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except Exception:
    GoogleGenerativeAIEmbeddings = None

try:
    from langchain_openai import OpenAIEmbeddings
except Exception:
    OpenAIEmbeddings = None
from typing import List, Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHROMA_DB_PATH, COLLECTION_NAME, GOOGLE_API_KEY, OPENAI_API_KEY, USE_OPENAI_EMBEDDINGS, TOP_K_RETRIEVAL
from data_loader import create_searchable_text
from hybrid_search import HybridSearcher


class VectorStore:
    """Vector store for managing embeddings and retrieval."""
    
    def __init__(self, use_hybrid: bool = False, semantic_weight: float = 0.6, keyword_weight: float = 0.4):
        """Initialize the vector store with ChromaDB and Google embeddings.
        
        Args:
            use_hybrid: Whether to use hybrid search (semantic + keyword)
            semantic_weight: Weight for semantic similarity (0-1)
            keyword_weight: Weight for keyword matching (0-1)
        """
        # Initialize embeddings with OpenAI or Google
        if USE_OPENAI_EMBEDDINGS and OPENAI_API_KEY:
            print("[EMBEDDINGS] Using OpenAI embeddings")
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=OPENAI_API_KEY
            )
        elif GOOGLE_API_KEY:
            print("[EMBEDDINGS] Using Google embeddings")
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=GOOGLE_API_KEY
            )
        else:
            print("[EMBEDDINGS] No API key found - embeddings disabled")
            self.embeddings = None

        # Initialize ChromaDB (or fallback in-memory client when chromadb isn't installed)
        if chromadb is not None:
            self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        else:
            # Minimal in-memory fallback to allow tests to run without chromadb
            class _InMemoryCollection:
                def __init__(self, name):
                    self.name = name
                    self._docs = []
                    self.metadata = {}

                def add(self, ids, documents, metadatas):
                    for i, _id in enumerate(ids):
                        self._docs.append((ids[i], documents[i], metadatas[i]))

                def query(self, query_texts, n_results):
                    docs = self._docs[:n_results]
                    return {
                        "ids": [[d[0] for d in docs]],
                        "documents": [[d[1] for d in docs]],
                        "metadatas": [[d[2] for d in docs]],
                        "distances": [[0.0 for _ in docs]]
                    }

                def count(self):
                    return len(self._docs)

            class _InMemoryClient:
                def __init__(self, path=None):
                    self._collections = {}

                def delete_collection(self, name):
                    self._collections.pop(name, None)

                def create_collection(self, name, metadata=None):
                    coll = _InMemoryCollection(name)
                    coll.metadata = metadata or {}
                    self._collections[name] = coll
                    return coll

                def get_collection(self, name):
                    return self._collections.get(name, _InMemoryCollection(name))

            self.client = _InMemoryClient(path=CHROMA_DB_PATH)
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
        
        if not documents:
            print("[WARNING] No documents to index. Creating empty collection.")
            return
        
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
        if self.use_hybrid:
            if self.hybrid_searcher:
                # Initialize hybrid searcher with collection
                self.hybrid_searcher.initialize(documents=documents)
                print(f"[OK] Hybrid search ready (semantic + keyword)")
            else:
                print("[WARNING] Hybrid search disabled - searcher not initialized")
    
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
