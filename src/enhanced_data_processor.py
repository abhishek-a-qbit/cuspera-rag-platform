import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
from dataclasses import dataclass

# Import dataset_2 processor
from dataset2_processor import Dataset2Processor, create_dataset2_searchable_text

@dataclass
class ChunkConfig:
    chunk_size: int
    overlap: int
    strategy: str
    min_chunk_size: int = 50

class EnhancedDataProcessor:
    """Enhanced data processor with optimal chunking for hybrid retrieval."""
    
    def __init__(self):
        self.chunk_configs = {
            "productCapability": ChunkConfig(200, 50, "semantic_boundary"),
            "faqItems": ChunkConfig(300, 0, "qa_pair"),
            "customerProfiles": ChunkConfig(400, 100, "section_based"),
            "metrics": ChunkConfig(150, 25, "metric_group"),
            "integrations": ChunkConfig(250, 50, "feature_based"),
            "competitors": ChunkConfig(350, 75, "comparison_based"),
            "pricingInsights": ChunkConfig(200, 40, "pricing_tier"),
            "securityCompliance": ChunkConfig(300, 60, "compliance_section"),
            "default": ChunkConfig(250, 50, "semantic_boundary")
        }
    
    def process_datasets(self, database_path: str) -> List[Dict[str, Any]]:
        """Process all datasets with optimal chunking."""
        documents = []
        database_dir = Path(database_path)
        
        # Initialize dataset_2 processor
        dataset2_processor = Dataset2Processor()
        
        # Global counter for unique IDs
        global_doc_counter = 0
        
        # Look for dataset folders
        dataset_folders = []
        for folder in ['dataset_1', 'dataset_2']:
            folder_path = database_dir / folder
            if folder_path.exists():
                dataset_folders.append(folder_path)
        
        total_files = 0
        
        for dataset_folder in dataset_folders:
            if dataset_folder.name == 'dataset_2':
                # Use specialized processor for dataset_2
                print(f"Processing dataset_2 with specialized processor...")
                dataset2_docs = dataset2_processor.process_dataset_2(str(dataset_folder))
                documents.extend(dataset2_docs)
                total_files += len(dataset2_docs)
            else:
                # Use standard processor for dataset_1
                json_files = sorted(dataset_folder.glob("*.json"))
                total_files += len(json_files)
                
                print(f"Processing {len(json_files)} files from {dataset_folder.name}")
                
                for json_file in json_files:
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Extract dataset info
                        meta = data.get("meta", {})
                        dataset_id = meta.get("datasetId", json_file.stem)
                        product_name = meta.get("canonicalProductName", "Unknown")
                        
                        # Process data items
                        items = data.get("data", [])
                        if isinstance(items, dict):
                            items = [items]
                        elif isinstance(items, str):
                            continue
                        
                        for item in items:
                            if isinstance(item, str):
                                continue
                            
                            # Process item with chunking
                            chunks = self._process_item(item, dataset_id, product_name, dataset_folder.name, json_file.name, global_doc_counter)
                            documents.extend(chunks)
                            global_doc_counter += len(chunks)
                        
                        print(f"[OK] Processed {len(items)} items from {json_file.name}")
                        
                    except Exception as e:
                        print(f"[ERROR] Error processing {json_file.name}: {str(e)}")
        
        print(f"\nTotal chunks created: {len(documents)}")
        return documents
    
    def _process_item(self, item: Dict[str, Any], dataset_id: str, product_name: str, 
                     dataset_folder: str, source_file: str, global_counter: int) -> List[Dict[str, Any]]:
        """Process a single item with optimal chunking."""
        
        # Determine content type
        content_type = item.get("type", "default")
        config = self.chunk_configs.get(content_type, self.chunk_configs["default"])
        
        # Create searchable content
        content_parts = []
        
        # Add label if present
        if "label" in item and item["label"]:
            content_parts.append(f"LABEL: {item['label']}")
        
        # Add description if present
        if "description" in item and item["description"]:
            content_parts.append(f"DESCRIPTION: {item['description']}")
        
        # Handle Q&A pairs
        if "question" in item and item["question"]:
            content_parts.append(f"QUESTION: {item['question']}")
        if "answer" in item and item["answer"]:
            content_parts.append(f"ANSWER: {item['answer']}")
        
        # Add other relevant fields
        for field in ["category", "subcategory", "industry", "use_case"]:
            if field in item and item[field]:
                content_parts.append(f"{field.upper()}: {item[field]}")
        
        # Combine content
        full_content = "\n\n".join(content_parts)
        
        # Apply chunking strategy
        chunks = self._chunk_content(full_content, config, content_type)
        
        # Create documents for each chunk
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"{dataset_folder}_{source_file}_{item.get('id', 'unknown')}_{global_counter + i}",  # Use global counter for uniqueness
                "content": chunk,
                "content_type": content_type,
                "dataset_id": dataset_id,
                "product_name": product_name,
                "dataset_folder": dataset_folder,
                "source_file": source_file,
                "item_id": item.get("id", "unknown"),
                "chunk_index": i,
                "total_chunks": len(chunks),
                "metadata": {
                    "dataset": dataset_id,
                    "product": product_name,
                    "source_file": source_file,
                    "content_type": content_type,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "item_id": item.get("id", "unknown"),
                    "original_label": item.get("label", ""),
                    "original_description": item.get("description", ""),
                    "source": item.get("source", {}),
                    "is_ai_related": item.get("isAIRelated", False),
                    "maturity": item.get("maturity", ""),
                    "category": item.get("category", ""),
                    "industry": item.get("industry", "")
                }
            }
            documents.append(doc)
        
        return documents
    
    def _chunk_content(self, content: str, config: ChunkConfig, content_type: str) -> List[str]:
        """Apply chunking strategy based on content type."""
        
        if content_type == "faqItems":
            return self._chunk_qa_pairs(content, config)
        elif content_type == "metrics":
            return self._chunk_metrics(content, config)
        elif content_type == "productCapability":
            return self._chunk_semantic_boundaries(content, config)
        else:
            return self._chunk_semantic_boundaries(content, config)
    
    def _chunk_qa_pairs(self, content: str, config: ChunkConfig) -> List[str]:
        """Chunk Q&A content keeping pairs together."""
        # Split by Q&A pairs
        qa_pairs = re.split(r'\n\nQUESTION:|\n\nANSWER:', content)
        chunks = []
        current_chunk = ""
        
        for pair in qa_pairs:
            if pair.strip():
                if len(current_chunk) + len(pair) <= config.chunk_size:
                    current_chunk += pair + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = pair + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]
    
    def _chunk_metrics(self, content: str, config: ChunkConfig) -> List[str]:
        """Chunk metrics content by metric groups."""
        # Split by metric indicators
        metric_sections = re.split(r'\n\nMETRIC:|\n\nKPI:|\n\nMEASUREMENT:', content)
        chunks = []
        current_chunk = ""
        
        for section in metric_sections:
            if section.strip():
                if len(current_chunk) + len(section) <= config.chunk_size:
                    current_chunk += section + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = section + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]
    
    def _chunk_semantic_boundaries(self, content: str, config: ChunkConfig) -> List[str]:
        """Chunk content using semantic boundaries."""
        # Split by sentences and paragraphs
        sentences = re.split(r'(?<=[.!?])\s+', content)
        paragraphs = re.split(r'\n\n', content)
        
        # Prefer paragraph boundaries
        if paragraphs and len(paragraphs) > 1:
            return self._chunk_by_paragraphs(paragraphs, config)
        else:
            return self._chunk_by_sentences(sentences, config)
    
    def _chunk_by_paragraphs(self, paragraphs: List[str], config: ChunkConfig) -> List[str]:
        """Chunk by paragraphs with overlap."""
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            if len(current_chunk) + len(paragraph) <= config.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else ["\n\n".join(paragraphs)]
    
    def _flatten_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested metadata for ChromaDB compatibility."""
        flattened = {}
        
        for key, value in metadata.items():
            if isinstance(value, dict):
                # Flatten nested dictionaries with prefix
                for nested_key, nested_value in value.items():
                    flattened[f"{key}_{nested_key}"] = nested_value
            elif isinstance(value, list):
                # Convert lists to strings
                flattened[key] = str(value)
            else:
                flattened[key] = value
        
        return flattened
    
    def _chunk_by_sentences(self, sentences: List[str], config: ChunkConfig) -> List[str]:
        chunks = []
        current_chunk = ""
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk) + len(sentence) <= config.chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # Add overlap from previous sentences
                if config.overlap > 0 and len(chunks) > 0:
                    overlap_text = chunks[-1][-config.overlap:] if len(chunks[-1]) > config.overlap else chunks[-1]
                    current_chunk = overlap_text + " " + sentence + " "
                else:
                    current_chunk = sentence + " "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [" ".join(sentences)]

def create_enhanced_searchable_text(doc: Dict[str, Any]) -> str:
    """Create enhanced searchable text from a chunked document."""
    
    # Use appropriate searchable text creation based on dataset
    if doc.get("dataset_folder") == "dataset_2":
        return create_dataset2_searchable_text(doc)
    
    # Start with the main content
    searchable_parts = [doc["content"]]
    
    # Add metadata for better retrieval
    metadata = doc.get("metadata", {})
    
    # Add content type context
    if metadata.get("content_type"):
        searchable_parts.append(f"CONTENT_TYPE: {metadata['content_type']}")
    
    # Add category context
    if metadata.get("category"):
        searchable_parts.append(f"CATEGORY: {metadata['category']}")
    
    # Add industry context
    if metadata.get("industry"):
        searchable_parts.append(f"INDUSTRY: {metadata['industry']}")
    
    # Add AI context
    if metadata.get("is_ai_related"):
        searchable_parts.append("AI_FEATURE: Yes")
    
    # Add maturity level
    if metadata.get("maturity"):
        searchable_parts.append(f"MATURITY: {metadata['maturity']}")
    
    return "\n\n".join(searchable_parts)
