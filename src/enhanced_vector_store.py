import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Any
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHROMA_DB_PATH, COLLECTION_NAME, GOOGLE_API_KEY, OPENAI_API_KEY, USE_OPENAI_EMBEDDINGS, TOP_K_RETRIEVAL, DIVERSITY_THRESHOLD
from data_loader import create_searchable_text
from hybrid_search import HybridSearcher

class EnhancedVectorStore:
    """Enhanced vector store with optimal chunking and retrieval."""
    
    def __init__(self, use_hybrid: bool = True, semantic_weight: float = 0.6, keyword_weight: float = 0.4):
        """Initialize the enhanced vector store."""
        
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
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = None
        
        # Use simple document processing
        self.processor = None
        
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
    
    def index_enhanced_documents(self, database_path: str):
        """Index documents with enhanced chunking."""
        if self.collection is None:
            self.create_collection()
        
        # Process datasets with simple loading
        print("\n[ENHANCED PROCESSING] Starting data processing...")
        documents = []
        if os.path.exists(database_path):
            for filename in os.listdir(database_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(database_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                documents.extend(data)
                            else:
                                documents.append(data)
                    except Exception as e:
                        print(f"[ENHANCED] Error loading {filename}: {e}")
        
        if not documents:
            print("[WARNING] No documents to index. Creating empty collection.")
            return
        
        # Prepare documents for indexing
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            # Create searchable text
            searchable_text = create_searchable_text(doc)
            
            ids.append(doc["id"])
            texts.append(searchable_text)
            
            # Enhanced metadata for better retrieval
            metadata = doc["metadata"].copy()
            metadata.update({
                "content_length": len(searchable_text),
                "chunk_index": doc["chunk_index"],
                "total_chunks": doc["total_chunks"],
                "content_type": doc["content_type"],
                "dataset_folder": doc["dataset_folder"]
            })
            
            # Flatten metadata for ChromaDB compatibility
            flattened_metadata = self._flatten_metadata(metadata)
            metadatas.append(flattened_metadata)
        
        # Add to collection in batches for better performance
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i+batch_size]
            batch_texts = texts[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            
            self.collection.add(
                ids=batch_ids,
                documents=batch_texts,
                metadatas=batch_metadatas
            )
            
            print(f"[PROGRESS] Indexed batch {i//batch_size + 1}/{(len(ids)-1)//batch_size + 1} ({len(batch_ids)} chunks)")
        
        print(f"[SUCCESS] Indexed {len(documents)} enhanced chunks into vector store")
        
        # Build hybrid search indices
        if self.use_hybrid and self.hybrid_searcher:
            self.hybrid_searcher.initialize(documents=documents)
            print(f"[OK] Hybrid search ready with enhanced chunks")
        
        # Print statistics
        self._print_indexing_statistics(documents)
    
    def _flatten_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested metadata for ChromaDB compatibility."""
        flattened = {}
        
        for key, value in metadata.items():
            if value is None:
                # Skip None values
                continue
            elif isinstance(value, dict):
                # Flatten nested dictionaries with prefix
                for nested_key, nested_value in value.items():
                    if nested_value is not None:
                        flattened[f"{key}_{nested_key}"] = nested_value
            elif isinstance(value, list):
                # Convert lists to strings
                flattened[key] = str(value)
            else:
                flattened[key] = value
        
        return flattened
    
    def _print_indexing_statistics(self, documents: List[Dict[str, Any]]):
        """Print detailed indexing statistics."""
        print("\n" + "="*60)
        print("ENHANCED INDEXING STATISTICS")
        print("="*60)
        
        # Content type distribution
        content_types = {}
        dataset_folders = {}
        chunk_sizes = []
        
        for doc in documents:
            # Content type stats
            content_type = doc["content_type"]
            content_types[content_type] = content_types.get(content_type, 0) + 1
            
            # Dataset folder stats
            folder = doc["dataset_folder"]
            dataset_folders[folder] = dataset_folders.get(folder, 0) + 1
            
            # Chunk size stats
            chunk_sizes.append(len(doc["content"]))
        
        print(f"Total Chunks: {len(documents)}")
        print(f"Average Chunk Size: {sum(chunk_sizes)/len(chunk_sizes):.1f} characters")
        print(f"Min Chunk Size: {min(chunk_sizes)} characters")
        print(f"Max Chunk Size: {max(chunk_sizes)} characters")
        
        print("\nContent Type Distribution:")
        for content_type, count in sorted(content_types.items()):
            print(f"  {content_type}: {count} chunks")
        
        print("\nDataset Distribution:")
        for folder, count in sorted(dataset_folders.items()):
            print(f"  {folder}: {count} chunks")
        
        print("="*60)
    
    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> List[Dict[str, Any]]:
        """Enhanced retrieval with diversity and multiple search strategies."""
        if self.collection is None:
            self.load_collection()
        
        # Use hybrid search if enabled
        if self.use_hybrid and self.hybrid_searcher:
            # Retrieve more candidates for diversity
            candidate_k = min(top_k * 3, 30)  # Get 3x candidates for diversity
            hybrid_results = self.hybrid_searcher.hybrid_search(
                query=query,
                top_k=candidate_k
            )
            
            # Apply diversity filtering and return top_k
            diverse_results = self._apply_diversity_filtering(hybrid_results, top_k)
            return diverse_results
        
        # Enhanced semantic-only search with diversity
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k * 2,  # Get more candidates for diversity
            include=["documents", "metadatas", "distances"]
        )
        
        # Apply diversity filtering
        diverse_results = self._apply_diversity_filtering_semantic(results, top_k)
        return diverse_results
    
    def _apply_diversity_filtering(self, results: List[Dict], top_k: int) -> List[Dict]:
        """Apply diversity filtering to ensure varied sources."""
        if not results:
            return []
        
        # Sort by score first
        sorted_results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)
        
        # Apply Maximal Marginal Relevance (MMR) for diversity
        selected_results = []
        remaining_results = sorted_results.copy()
        
        # Select first result (always include the best one)
        if remaining_results:
            selected_results.append(remaining_results.pop(0))
        
        # Select diverse remaining results
        while len(selected_results) < top_k and remaining_results:
            # Find result most different from selected ones
            best_candidate = None
            best_similarity = -1
            
            for candidate in remaining_results:
                # Calculate similarity to already selected results
                min_similarity = 1.0
                for selected in selected_results:
                    # Use content similarity (simplified)
                    similarity = self._calculate_content_similarity(
                        candidate.get('content', ''), 
                        selected.get('content', '')
                    )
                    min_similarity = min(min_similarity, similarity)
                
                # Prefer diverse results
                if min_similarity < DIVERSITY_THRESHOLD and len(selected_results) > 0:
                    if best_candidate is None or min_similarity < best_similarity:
                        best_candidate = candidate
                        best_similarity = min_similarity
            
            if best_candidate:
                selected_results.append(best_candidate)
                remaining_results.remove(best_candidate)
            else:
                # Add next best if diversity threshold not met
                if remaining_results:
                    selected_results.append(remaining_results.pop(0))
        
        return selected_results[:top_k]
    
    def _apply_diversity_filtering_semantic(self, results: Dict, top_k: int) -> List[Dict]:
        """Apply diversity filtering to semantic search results."""
        if not results or not results.get("ids"):
            return []
        
        retrieved_docs = []
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0] if results["distances"] else [0] * len(ids)
        
        # Create result objects
        result_objects = []
        for idx, doc_id in enumerate(ids):
            result_objects.append({
                "id": doc_id,
                "content": documents[idx],
                "metadata": metadatas[idx],
                "distance": distances[idx],
                "score": 1 - distances[idx] if distances[idx] is not None else 0,
                "search_type": "enhanced_semantic_diverse"
            })
        
        # Apply diversity filtering
        diverse_results = self._apply_diversity_filtering(result_objects, top_k)
        return diverse_results
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate simple content similarity for diversity filtering."""
        if not content1 or not content2:
            return 0.0
        
        # Simple word overlap similarity
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get enhanced statistics about the collection."""
        if self.collection is None:
            self.load_collection()
        
        # Get basic stats
        basic_stats = {
            "collection_name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }
        
        # Get enhanced stats if possible
        try:
            # Sample some documents to get content type distribution
            sample_results = self.collection.get(limit=1000)
            
            content_types = {}
            dataset_folders = {}
            
            for metadata in sample_results.get("metadatas", []):
                if metadata:
                    content_type = metadata.get("content_type", "unknown")
                    content_types[content_type] = content_types.get(content_type, 0) + 1
                    
                    folder = metadata.get("dataset_folder", "unknown")
                    dataset_folders[folder] = dataset_folders.get(folder, 0) + 1
            
            basic_stats.update({
                "content_type_distribution": content_types,
                "dataset_distribution": dataset_folders,
                "sample_size": len(sample_results.get("ids", []))
            })
            
        except Exception as e:
            print(f"[WARNING] Could not get enhanced stats: {e}")
        
        return basic_stats

# Factory function for easy integration
def create_enhanced_vector_store(database_path: str, use_hybrid: bool = True) -> EnhancedVectorStore:
    """Create and initialize an enhanced vector store."""
    vector_store = EnhancedVectorStore(use_hybrid=use_hybrid)
    vector_store.index_enhanced_documents(database_path)
    return vector_store
