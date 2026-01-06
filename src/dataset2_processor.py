import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
from dataclasses import dataclass

class Dataset2Processor:
    """Specialized processor for dataset_2 with mixed file formats."""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_dataset_2(self, dataset_path: str) -> List[Dict[str, Any]]:
        """Process all files in dataset_2 with format-specific handling."""
        documents = []
        dataset_dir = Path(dataset_path)
        
        if not dataset_dir.exists():
            print(f"[WARNING] Dataset 2 path {dataset_path} does not exist")
            return documents
        
        print(f"\n[DATASET_2] Processing files from {dataset_path}")
        
        # Process each file based on its extension
        for file_path in sorted(dataset_dir.glob("*")):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.json':
                        docs = self._process_json_file(file_path)
                    elif file_path.suffix.lower() == '.tsv':
                        docs = self._process_tsv_file(file_path)
                    elif file_path.suffix.lower() == '.txt':
                        docs = self._process_txt_file(file_path)
                    else:
                        print(f"[SKIP] Unsupported file type: {file_path.name}")
                        continue
                    
                    documents.extend(docs)
                    print(f"[OK] Processed {len(docs)} documents from {file_path.name}")
                    
                except Exception as e:
                    print(f"[ERROR] Error processing {file_path.name}: {str(e)}")
        
        print(f"\n[DATASET_2] Total documents processed: {len(documents)}")
        return documents
    
    def _process_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process JSON files (like crawled data)."""
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle array of objects (crawled data)
        if isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    docs = self._process_crawled_item(item, file_path.name, i)
                    documents.extend(docs)
        
        # Handle single object with meta/data structure
        elif isinstance(data, dict) and "data" in data:
            meta = data.get("meta", {})
            items = data.get("data", [])
            
            if isinstance(items, list):
                for i, item in enumerate(items):
                    if isinstance(item, dict):
                        docs = self._process_structured_item(item, meta, file_path.name, i)
                        documents.extend(docs)
        
        return documents
    
    def _process_crawled_item(self, item: Dict[str, Any], source_file: str, index: int) -> List[Dict[str, Any]]:
        """Process crawled website data."""
        documents = []
        
        # Extract content from crawled data
        url = item.get("url", "")
        title = item.get("title", "")
        meta_description = item.get("meta_description", "")
        paragraphs = item.get("p", [])
        
        # Create searchable content
        content_parts = []
        
        if title:
            content_parts.append(f"TITLE: {title}")
        
        if meta_description:
            content_parts.append(f"DESCRIPTION: {meta_description}")
        
        if paragraphs:
            for i, paragraph in enumerate(paragraphs):
                if paragraph and len(paragraph.strip()) > 20:  # Filter short paragraphs
                    content_parts.append(f"CONTENT_{i+1}: {paragraph.strip()}")
        
        full_content = "\n\n".join(content_parts)
        
        # Create chunks from the content
        chunks = self._chunk_content(full_content, "crawled_content")
        
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"dataset_2_{source_file}_{index}_{i}",  # Ensure uniqueness with dataset_2 prefix
                "content": chunk,
                "content_type": "crawled_content",
                "dataset_id": "dataset_2_crawled",
                "product_name": "6sense Revenue AI",
                "dataset_folder": "dataset_2",
                "source_file": source_file,
                "item_id": f"crawl_{index}",
                "chunk_index": i,
                "total_chunks": len(chunks),
                "url": url,
                "title": title,
                "metadata": {
                    "dataset": "dataset_2_crawled",
                    "product": "6sense Revenue AI",
                    "source_file": source_file,
                    "content_type": "crawled_content",
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "item_id": f"crawl_{index}",
                    "url": url,
                    "title": title,
                    "source_type": "web_crawl",
                    "has_title": bool(title),
                    "has_description": bool(meta_description),
                    "paragraph_count": len([p for p in paragraphs if len(p.strip()) > 20])
                }
            }
            documents.append(doc)
        
        return documents
    
    def _process_structured_item(self, item: Dict[str, Any], meta: Dict[str, Any], source_file: str, index: int) -> List[Dict[str, Any]]:
        """Process structured data items."""
        documents = []
        
        # Create searchable content
        content_parts = []
        
        # Add all string fields
        for key, value in item.items():
            if isinstance(value, str) and len(value.strip()) > 10:
                content_parts.append(f"{key.upper()}: {value.strip()}")
        
        full_content = "\n\n".join(content_parts)
        
        # Create chunks
        chunks = self._chunk_content(full_content, "structured_content")
        
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"dataset_2_{source_file}_{index}_{i}",  # Ensure uniqueness
                "content": chunk,
                "content_type": "structured_content",
                "dataset_id": "dataset_2_structured",
                "product_name": "6sense Revenue AI",
                "dataset_folder": "dataset_2",
                "source_file": source_file,
                "item_id": f"structured_{index}",
                "chunk_index": i,
                "total_chunks": len(chunks),
                "metadata": {
                    "dataset": "dataset_2_structured",
                    "product": "6sense Revenue AI",
                    "source_file": source_file,
                    "content_type": "structured_content",
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "item_id": f"structured_{index}",
                    "source_type": "structured_data",
                    "field_count": len([k for k, v in item.items() if isinstance(v, str) and len(v.strip()) > 10])
                }
            }
            documents.append(doc)
        
        return documents
    
    def _process_tsv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process TSV files (case studies, reviews)."""
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # Try to detect delimiter and read as CSV
            content = f.read()
            
            # Check if it's tab-separated or comma-separated
            delimiter = '\t' if '\t' in content else ','
            
            f.seek(0)
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for i, row in enumerate(reader):
                if not row:
                    continue
                
                # Create searchable content from row
                content_parts = []
                
                for key, value in row.items():
                    if value and len(str(value).strip()) > 5:
                        content_parts.append(f"{key}: {str(value).strip()}")
                
                full_content = "\n\n".join(content_parts)
                
                # Determine content type from filename
                if "case_study" in file_path.name.lower():
                    content_type = "case_study"
                elif "review" in file_path.name.lower():
                    content_type = "review"
                else:
                    content_type = "tabular_data"
                
                # Create chunks
                chunks = self._chunk_content(full_content, content_type)
                
                for j, chunk in enumerate(chunks):
                    doc = {
                        "id": f"dataset_2_{file_path.stem}_{i}_{j}",  # Ensure uniqueness
                        "content": chunk,
                        "content_type": content_type,
                        "dataset_id": f"dataset_2_{content_type}",
                        "product_name": "6sense Revenue AI",
                        "dataset_folder": "dataset_2",
                        "source_file": file_path.name,
                        "item_id": f"{content_type}_{i}",
                        "chunk_index": j,
                        "total_chunks": len(chunks),
                        "metadata": {
                            "dataset": f"dataset_2_{content_type}",
                            "product": "6sense Revenue AI",
                            "source_file": file_path.name,
                            "content_type": content_type,
                            "chunk_index": j,
                            "total_chunks": len(chunks),
                            "item_id": f"{content_type}_{i}",
                            "source_type": "tabular_data",
                            "row_index": i,
                            "field_count": len([k for k, v in row.items() if v and len(str(v).strip()) > 5])
                        }
                    }
                    documents.append(doc)
        
        return documents
    
    def _process_txt_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process TXT files (reports, articles, keywords)."""
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine content type from filename
        filename_lower = file_path.name.lower()
        
        if "keyword" in filename_lower:
            content_type = "keywords"
        elif "report" in filename_lower or "wave" in filename_lower:
            content_type = "industry_report"
        elif "case_study" in filename_lower or "b2b" in filename_lower:
            content_type = "market_analysis"
        elif "stack" in filename_lower:
            content_type = "tech_stack"
        else:
            content_type = "text_content"
        
        # Clean and structure the content
        cleaned_content = self._clean_text_content(content)
        
        # Create chunks
        chunks = self._chunk_content(cleaned_content, content_type)
        
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"dataset_2_{file_path.stem}_{i}",  # Ensure uniqueness
                "content": chunk,
                "content_type": content_type,
                "dataset_id": f"dataset_2_{content_type}",
                "product_name": "6sense Revenue AI",
                "dataset_folder": "dataset_2",
                "source_file": file_path.name,
                "item_id": f"{content_type}_doc",
                "chunk_index": i,
                "total_chunks": len(chunks),
                "metadata": {
                    "dataset": f"dataset_2_{content_type}",
                    "product": "6sense Revenue AI",
                    "source_file": file_path.name,
                    "content_type": content_type,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "item_id": f"{content_type}_doc",
                    "source_type": "text_file",
                    "file_size": len(content),
                    "word_count": len(content.split())
                }
            }
            documents.append(doc)
        
        return documents
    
    def _clean_text_content(self, content: str) -> str:
        """Clean and structure text content."""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove special characters that might interfere
        content = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\'\/\n\t]', '', content)
        
        # Structure content by paragraphs
        paragraphs = content.split('\n')
        structured_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if len(para) > 20:  # Keep meaningful paragraphs
                structured_paragraphs.append(para)
        
        return '\n\n'.join(structured_paragraphs)
    
    def _chunk_content(self, content: str, content_type: str) -> List[str]:
        """Chunk content based on type with optimal sizes."""
        
        # Define chunking strategies for different content types
        chunk_strategies = {
            "crawled_content": {"size": 300, "overlap": 50},
            "structured_content": {"size": 250, "overlap": 40},
            "case_study": {"size": 400, "overlap": 80},
            "review": {"size": 200, "overlap": 30},
            "keywords": {"size": 150, "overlap": 20},
            "industry_report": {"size": 350, "overlap": 70},
            "market_analysis": {"size": 300, "overlap": 60},
            "tech_stack": {"size": 200, "overlap": 30},
            "text_content": {"size": 250, "overlap": 40},
            "tabular_data": {"size": 200, "overlap": 30}
        }
        
        strategy = chunk_strategies.get(content_type, {"size": 250, "overlap": 40})
        chunk_size = strategy["size"]
        overlap = strategy["overlap"]
        
        # Split by sentences first
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # Add overlap from previous chunk
                if overlap > 0 and chunks:
                    last_chunk = chunks[-1]
                    words = last_chunk.split()
                    overlap_words = words[-overlap//10:] if len(words) > overlap//10 else words
                    current_chunk = " ".join(overlap_words) + " " + sentence + " "
                else:
                    current_chunk = sentence + " "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]

def create_dataset2_searchable_text(doc: Dict[str, Any]) -> str:
    """Create enhanced searchable text for dataset_2 documents."""
    
    # Start with main content
    searchable_parts = [doc["content"]]
    
    # Add metadata for better retrieval
    metadata = doc.get("metadata", {})
    
    # Add content type context
    if metadata.get("content_type"):
        searchable_parts.append(f"CONTENT_TYPE: {metadata['content_type']}")
    
    # Add source type context
    if metadata.get("source_type"):
        searchable_parts.append(f"SOURCE_TYPE: {metadata['source_type']}")
    
    # Add URL if available
    if doc.get("url"):
        searchable_parts.append(f"SOURCE_URL: {doc['url']}")
    
    # Add title if available
    if doc.get("title"):
        searchable_parts.append(f"TITLE: {doc['title']}")
    
    # Add file context
    if metadata.get("source_file"):
        searchable_parts.append(f"DOCUMENT: {metadata['source_file']}")
    
    return "\n\n".join(searchable_parts)
