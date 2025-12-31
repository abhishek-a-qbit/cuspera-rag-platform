import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Vector Store Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "cuspera_knowledge_base"

# Dataset Configuration
DATABASE_PATH = "./Database"

# LLM Configuration - Using Google Gemini for faster performance
# Google embeddings are used for better performance and speed

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 5
