"""
Production configuration for RAG Chatbot
"""

import os
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).parent
FAISS_INDEX_DIR = BASE_DIR / "faiss_index"

# Ollama Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Streamlit Configuration
STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")

# Application Settings
APP_TITLE = os.getenv("APP_TITLE", "Domain Expert Chat")
APP_ICON = os.getenv("APP_ICON", "🤖")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Production Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# Performance
MAX_FILE_SIZE_MB = 10
MAX_CONTEXT_LENGTH = 1500
CACHE_SIZE = 10
