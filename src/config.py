import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector Store Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "cuspera_docs"
TOP_K_RETRIEVAL = 5  # Reduced from 10 to save memory

# Dataset Configuration
# Handle different deployment environments
if os.path.exists("../Database"):
    DATABASE_PATH = "../Database"
elif os.path.exists("Database"):
    DATABASE_PATH = "Database"
elif os.path.exists("dataset_1"):
    DATABASE_PATH = "."  # Use current directory if dataset folders exist
else:
    DATABASE_PATH = "../Database"  # Default fallback

# LLM Configuration - Using OpenAI for better reliability
# OpenAI models are more stable and widely available
USE_OPENAI = bool(OPENAI_API_KEY)  # Auto-switch to OpenAI if key is available
USE_OPENAI_EMBEDDINGS = bool(OPENAI_API_KEY)  # Use OpenAI embeddings if available

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
