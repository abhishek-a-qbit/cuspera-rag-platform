import json
import os
from pathlib import Path
from typing import List, Dict, Any

def load_all_datasets(database_path: str) -> List[Dict[str, Any]]:
    """Load all JSON datasets from the database folder."""
    documents = []
    database_dir = Path(database_path)
    doc_counter = 0  # Counter for generating unique IDs
    
    if not database_dir.exists():
        raise FileNotFoundError(f"Database path {database_path} does not exist")
    
    # Get all JSON files sorted by name
    json_files = sorted(database_dir.glob("*.json"))
    
    print(f"Found {len(json_files)} JSON files in {database_path}")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract dataset info from meta
            meta = data.get("meta", {})
            dataset_id = meta.get("datasetId", json_file.stem)
            product_name = meta.get("canonicalProductName", "Unknown")
            
            # Process data items
            items = data.get("data", [])
            if isinstance(items, dict):
                # If data is a dict, convert to list
                items = [items]
            elif isinstance(items, str):
                # If it's a string, skip
                continue
            
            for idx, item in enumerate(items):
                if isinstance(item, str):
                    # Skip if item is string
                    continue
                    
                doc_counter += 1
                
                # Create a document with searchable content
                doc = {
                    "id": f"{json_file.stem}_{idx}_{doc_counter}",  # Generate unique ID
                    "dataset_id": dataset_id,
                    "product_name": product_name,
                    "source_file": json_file.name,
                    "content": json.dumps(item, indent=2),  # Full item as content
                    "metadata": {
                        "dataset": dataset_id,
                        "product": product_name,
                        "source_file": json_file.name
                    }
                }
                
                # Add type-specific metadata
                if "type" in item:
                    doc["metadata"]["type"] = item["type"]
                if "label" in item:
                    doc["metadata"]["label"] = item["label"]
                if "question" in item:
                    doc["metadata"]["question"] = item["question"]
                
                documents.append(doc)
            
            print(f"[OK] Loaded {len(items)} items from {json_file.name}")
            
        except Exception as e:
            print(f"[ERROR] Error loading {json_file.name}: {str(e)}")
    
    print(f"\nTotal documents processed: {len(documents)}")
    return documents


def create_searchable_text(doc: Dict[str, Any]) -> str:
    """Create searchable text from a document."""
    parts = []
    
    # Add label/question if present
    if "label" in doc:
        parts.append(doc["label"])
    if "question" in doc:
        parts.append(doc["question"])
    if "description" in doc:
        parts.append(doc["description"])
    if "answer" in doc:
        parts.append(doc["answer"])
    
    # Add full content
    parts.append(doc.get("content", ""))
    
    return " ".join(filter(None, parts))
