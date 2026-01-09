import os
# from dotenv import load_dotenv

# load_dotenv()  # Commented out to avoid Unicode issues

# API Configuration - Direct values to avoid dotenv issues
GOOGLE_API_KEY = None  # os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = None  # os.getenv("OPENAI_API_KEY")

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

# LLM Configuration - Using fallback since no API keys
USE_OPENAI = False  # bool(OPENAI_API_KEY)  # Auto-switch to OpenAI if key is available
USE_OPENAI_EMBEDDINGS = False  # bool(OPENAI_API_KEY)  # Use OpenAI embeddings if available

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
