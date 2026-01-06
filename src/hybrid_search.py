"""
Hybrid Search Module - Combines Semantic + Keyword Search
Uses BM25 for keyword matching and embeddings for semantic search
"""

from typing import List, Dict, Any, Tuple
import json
import numpy as np
from pathlib import Path
from rank_bm25 import BM25Okapi
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os


class HybridSearcher:
    """Hybrid search combining semantic and keyword-based retrieval."""
    
    def __init__(self, semantic_weight: float = 0.6, keyword_weight: float = 0.4):
        """
        Initialize hybrid searcher.
        
        Args:
            semantic_weight: Weight for semantic similarity (0-1)
            keyword_weight: Weight for keyword matching (0-1)
        """
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        
        # Ensure weights sum to 1
        total = semantic_weight + keyword_weight
        self.semantic_weight /= total
        self.keyword_weight /= total
        
        # Components
        self.embeddings = None
        self.chromadb_client = None
        self.collection = None
        self.bm25_index = None
        self.documents = []
    
    def initialize(self, db_path: str = "./chroma_db", collection_name: str = "cuspera", documents: List[Dict[str, Any]] = None):
        """Initialize vector store and keyword index."""
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Initialize ChromaDB
        self.chromadb_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chromadb_client.get_collection(name=collection_name)
        
        # Build keyword index if documents provided
        if documents:
            self.build_keyword_index(documents)
        
        print("[OK] Hybrid searcher initialized")
    
    def build_keyword_index(self, documents: List[Dict[str, Any]]):
        """Build BM25 keyword index from documents."""
        # Extract text from documents
        self.documents = documents
        texts = []
        
        for doc in documents:
            # Combine all searchable text
            parts = []
            if "label" in doc:
                parts.append(doc["label"])
            if "question" in doc:
                parts.append(doc["question"])
            if "description" in doc:
                parts.append(doc["description"])
            if "content" in doc:
                # Just first 500 chars to keep index size reasonable
                parts.append(doc["content"][:500])
            
            text = " ".join(filter(None, parts))
            texts.append(text.lower())
        
        # Tokenize and build BM25 index
        tokenized_texts = [text.split() for text in texts]
        self.bm25_index = BM25Okapi(tokenized_texts)
        
        print(f"[OK] Built BM25 keyword index for {len(documents)} documents")
    
    def semantic_search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Perform semantic search using vector similarity.
        
        Returns: List of (doc_id, score) tuples
        """
        # Query the vector store
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        doc_scores = []
        if results and results["ids"] and len(results["ids"]) > 0:
            for idx, doc_id in enumerate(results["ids"][0]):
                # Distance to similarity (cosine distance to similarity)
                distance = results["distances"][0][idx] if results["distances"] else 0
                similarity = 1 - distance  # Convert distance to similarity
                doc_scores.append((doc_id, similarity))
        
        return doc_scores
    
    def keyword_search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Perform keyword search using BM25.
        
        Returns: List of (doc_id, score) tuples
        """
        if self.bm25_index is None:
            return []
        
        # Tokenize query
        query_tokens = query.lower().split()
        
        # Get BM25 scores
        bm25_scores = self.bm25_index.get_scores(query_tokens)
        
        # Get top-k
        doc_scores = []
        for idx, score in enumerate(bm25_scores):
            if idx < len(self.documents):
                doc_id = self.documents[idx].get("id", str(idx))
                # Normalize BM25 score to 0-1 range (roughly)
                normalized_score = min(1.0, score / 10.0)  # Adjust divisor as needed
                doc_scores.append((doc_id, normalized_score))
        
        # Sort and return top-k
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        return doc_scores[:top_k]
    
    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search.
        
        Returns: List of documents ranked by combined score
        """
        # Get semantic results
        semantic_results = self.semantic_search(query, top_k=top_k * 2)
        
        # Get keyword results
        keyword_results = self.keyword_search(query, top_k=top_k * 2)
        
        # Combine scores
        doc_scores = {}
        
        # Add semantic scores
        for doc_id, score in semantic_results:
            doc_scores[doc_id] = self.semantic_weight * score
        
        # Add keyword scores
        for doc_id, score in keyword_results:
            if doc_id in doc_scores:
                doc_scores[doc_id] += self.keyword_weight * score
            else:
                doc_scores[doc_id] = self.keyword_weight * score
        
        # Sort by combined score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Fetch full documents from ChromaDB
        top_doc_ids = [doc_id for doc_id, _ in sorted_docs[:top_k]]
        
        if not top_doc_ids:
            return []
        
        results = self.collection.get(ids=top_doc_ids)
        
        # Reconstruct with scores
        retrieved_docs = []
        for idx, doc_id in enumerate(top_doc_ids):
            if results and results["ids"] and doc_id in results["ids"]:
                doc_idx = results["ids"].index(doc_id)
                retrieved_docs.append({
                    "id": doc_id,
                    "content": results["documents"][doc_idx] if doc_idx < len(results["documents"]) else "",
                    "metadata": results["metadatas"][doc_idx] if doc_idx < len(results["metadatas"]) else {},
                    "combined_score": doc_scores[doc_id],
                    "semantic_score": next((s for d, s in semantic_results if d == doc_id), 0),
                    "keyword_score": next((s for d, s in keyword_results if d == doc_id), 0)
                })
        
        return retrieved_docs
    
    def get_search_scores(self, query: str) -> Dict[str, Any]:
        """Get detailed breakdown of search scores."""
        semantic = self.semantic_search(query, top_k=5)
        keyword = self.keyword_search(query, top_k=5)
        
        return {
            "query": query,
            "semantic_results": semantic,
            "keyword_results": keyword,
            "weights": {
                "semantic": self.semantic_weight,
                "keyword": self.keyword_weight
            }
        }


# Example usage
if __name__ == "__main__":
    # Initialize
    searcher = HybridSearcher(semantic_weight=0.6, keyword_weight=0.4)
    
    # Example documents
    documents = [
        {
            "id": "doc1",
            "label": "AI Capabilities",
            "content": "6sense uses artificial intelligence to identify high-intent accounts"
        },
        {
            "id": "doc2",
            "label": "Pricing Plans",
            "content": "Our pricing starts at $5000 per year for basic tier"
        },
        {
            "id": "doc3",
            "label": "Integration Support",
            "content": "We integrate with Salesforce, HubSpot, and Pipedrive"
        }
    ]
    
    # Build keyword index
    searcher.build_keyword_index(documents)
    
    # Example query
    query = "AI and machine learning capabilities"
    print(f"\nSearching for: '{query}'")
    print(f"Semantic weight: {searcher.semantic_weight}")
    print(f"Keyword weight: {searcher.keyword_weight}")
