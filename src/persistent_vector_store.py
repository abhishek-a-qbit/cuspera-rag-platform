import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Any
import sys
import os
import json
from pathlib import Path
import hashlib
import pickle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CHROMA_DB_PATH, COLLECTION_NAME, GOOGLE_API_KEY, OPENAI_API_KEY, USE_OPENAI_EMBEDDINGS, TOP_K_RETRIEVAL, DATABASE_PATH
from data_loader import create_searchable_text

class PersistentVectorStore:
    """Vector store with persistent chunking and embedding caching."""
    
    def __init__(self, use_hybrid: bool = False):
        """Initialize the persistent vector store."""
        
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
        
        # Cache paths
        self.cache_dir = Path(CHROMA_DB_PATH).parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.chunks_cache_file = self.cache_dir / "processed_chunks.pkl"
        self.metadata_cache_file = self.cache_dir / "processing_metadata.json"
        
        self.use_hybrid = use_hybrid
    
    def get_data_hash(self, database_path: str) -> str:
        """Generate hash of the database files to detect changes."""
        hash_md5 = hashlib.md5()
        
        database_dir = Path(database_path)
        if not database_dir.exists():
            return ""
        
        # Hash all files in both datasets
        for dataset_folder in ['dataset_1', 'dataset_2']:
            folder_path = database_dir / dataset_folder
            if folder_path.exists():
                for file_path in sorted(folder_path.glob("*")):
                    if file_path.is_file():
                        # File content hash
                        with open(file_path, 'rb') as f:
                            for chunk in iter(lambda: f.read(8192), b''):
                                if not chunk:
                                    break
                                hash_md5.update(chunk)
                        
                        # File metadata (size, modified time)
                        file_stat = file_path.stat()
                        hash_md5.update(str(file_stat.st_size).encode())
                        hash_md5.update(str(file_stat.st_mtime).encode())
        
        return hash_md5.hexdigest()
    
    def is_cache_valid(self, database_path: str) -> bool:
        """Check if cached chunks are still valid."""
        if not self.chunks_cache_file.exists() or not self.metadata_cache_file.exists():
            return False
        
        try:
            # Load cache metadata
            with open(self.metadata_cache_file, 'r') as f:
                cache_metadata = json.load(f)
            
            # Check if database has changed
            current_hash = self.get_data_hash(database_path)
            cached_hash = cache_metadata.get("data_hash", "")
            
            if current_hash != cached_hash:
                print("[CACHE] Database has changed, need to reprocess")
                return False
            
            # Check if collection exists
            try:
                self.client.get_collection(name=COLLECTION_NAME)
                print("[CACHE] Cached chunks and collection are valid")
                return True
            except:
                print("[CACHE] Collection missing, need to rebuild")
                return False
                
        except Exception as e:
            print(f"[CACHE] Error checking cache: {e}")
            return False
    
    def load_cached_chunks(self) -> List[Dict[str, Any]]:
        """Load processed chunks from cache."""
        try:
            with open(self.chunks_cache_file, 'rb') as f:
                chunks = pickle.load(f)
            print(f"[CACHE] Loaded {len(chunks)} cached chunks")
            return chunks
        except Exception as e:
            print(f"[CACHE] Error loading cached chunks: {e}")
            return []
    
    def save_chunks_to_cache(self, chunks: List[Dict[str, Any]], database_path: str):
        """Save processed chunks to cache."""
        try:
            # Save chunks
            with open(self.chunks_cache_file, 'wb') as f:
                pickle.dump(chunks, f)
            
            # Save metadata
            cache_metadata = {
                "data_hash": self.get_data_hash(database_path),
                "chunks_count": len(chunks),
                "created_at": str(Path().cwd()),
                "version": "1.0"
            }
            
            with open(self.metadata_cache_file, 'w') as f:
                json.dump(cache_metadata, f, indent=2)
            
            print(f"[CACHE] Saved {len(chunks)} chunks to cache")
            
        except Exception as e:
            print(f"[CACHE] Error saving to cache: {e}")
    
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
        try:
            self.collection = self.client.get_collection(name=COLLECTION_NAME)
            print(f"Loaded existing collection: {COLLECTION_NAME}")
            return True
        except:
            return False
    
    def index_documents_persistent(self, database_path: str, force_reprocess: bool = False):
        """Index documents with persistent caching."""
        
        # Check if we can use cached chunks
        if not force_reprocess and self.is_cache_valid(database_path):
            print("[PERSISTENT] Using cached chunks and embeddings")
            chunks = self.load_cached_chunks()
            
            # Just load the existing collection
            if self.load_collection():
                self._print_statistics(chunks)
                return chunks
            else:
                print("[PERSISTENT] Collection missing, rebuilding from cache")
        
        # Need to reprocess
        print("[PERSISTENT] Processing documents and creating embeddings...")
        
        # Use existing data loader
        from data_loader import create_searchable_text
        
        # Load documents from database path
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
                        print(f"[PERSISTENT] Error loading {filename}: {e}")
        
        # Create chunks from documents
        chunks = []
        for i, doc in enumerate(documents):
            if isinstance(doc, dict) and 'content' in doc:
                chunk = {
                    "id": f"doc_{i}",
                    "content": doc['content'],
                    "metadata": doc.get('metadata', {}),
                    "source": doc.get('source', filename)
                }
                chunks.append(chunk)
        
        if not chunks:
            print("[WARNING] No documents to index.")
            return []
        
        # Create new collection
        self.create_collection()
        
        # Prepare documents for indexing
        ids = []
        texts = []
        metadatas = []
        
        for chunk in chunks:
            # Create searchable text
            searchable_text = create_searchable_text(chunk)
            
            ids.append(chunk["id"])
            texts.append(searchable_text)
            
            # Flatten metadata for ChromaDB compatibility
            metadata = self._flatten_metadata(chunk["metadata"])
            metadatas.append(metadata)
        
        # Add to collection in batches
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
        
        print(f"[SUCCESS] Indexed {len(chunks)} chunks into vector store")
        
        # Save to cache
        self.save_chunks_to_cache(chunks, database_path)
        
        # Print statistics
        self._print_statistics(chunks)
        
        return chunks
    
    def _flatten_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested metadata for ChromaDB compatibility."""
        flattened = {}
        
        for key, value in metadata.items():
            if value is None:
                continue
            elif isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if nested_value is not None:
                        flattened[f"{key}_{nested_key}"] = nested_value
            elif isinstance(value, list):
                flattened[key] = str(value)
            else:
                flattened[key] = value
        
        return flattened
    
    def _print_statistics(self, chunks: List[Dict[str, Any]]):
        """Print processing statistics."""
        print("\n" + "="*60)
        print("PERSISTENT VECTOR STORE STATISTICS")
        print("="*60)
        
        content_types = {}
        dataset_folders = {}
        chunk_sizes = []
        
        for chunk in chunks:
            # Content type stats
            content_type = chunk.get("content_type", "unknown")
            content_types[content_type] = content_types.get(content_type, 0) + 1
            
            # Dataset folder stats
            folder = chunk.get("dataset_folder", "unknown")
            dataset_folders[folder] = dataset_folders.get(folder, 0) + 1
            
            # Chunk size stats
            chunk_sizes.append(len(chunk.get("content", "")))
        
        print(f"Total Chunks: {len(chunks)}")
        if chunk_sizes:
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
        """Retrieve documents from persistent vector store."""
        if self.collection is None:
            if not self.load_collection():
                raise Exception("No collection available")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        retrieved_docs = []
        if results and results["ids"] and len(results["ids"][0]) > 0:
            for idx, doc_id in enumerate(results["ids"][0]):
                retrieved_docs.append({
                    "id": doc_id,
                    "content": results["documents"][0][idx],
                    "metadata": results["metadatas"][0][idx],
                    "distance": results["distances"][0][idx] if results["distances"] else None,
                    "score": 1 - results["distances"][0][idx] if results["distances"] else 0,
                    "search_type": "persistent_semantic"
                })
        
        return retrieved_docs
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        if self.collection is None:
            self.load_collection()
        
        stats = {
            "collection_name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata,
            "persistent_cache": self.chunks_cache_file.exists(),
            "cache_valid": self.is_cache_valid(DATABASE_PATH) if self.chunks_cache_file.exists() else False
        }
        
        # Add cached stats if available
        if self.metadata_cache_file.exists():
            try:
                with open(self.metadata_cache_file, 'r') as f:
                    cache_metadata = json.load(f)
                stats.update({
                    "cached_chunks": cache_metadata.get("chunks_count", 0),
                    "cache_version": cache_metadata.get("version", "unknown"),
                    "cache_created": cache_metadata.get("created_at", "unknown")
                })
            except:
                pass
        
        return stats

# Factory function for easy integration
def create_persistent_vector_store(database_path: str, use_hybrid: bool = False, force_reprocess: bool = False) -> PersistentVectorStore:
    """Create and initialize a persistent vector store."""
    vector_store = PersistentVectorStore(use_hybrid=use_hybrid)
    vector_store.index_documents_persistent(database_path, force_reprocess=force_reprocess)
    return vector_store
