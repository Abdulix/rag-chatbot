"""
Configuration file for Domain Expert Chat (RAG Assistant)
Customize these settings to optimize performance for your use case.
"""

# Document Processing Configuration
DOCUMENT_CONFIG = {
    "chunk_size": 500,          # Size of text chunks (characters)
    "chunk_overlap": 50,        # Overlap between chunks (characters)
    "supported_formats": ["pdf", "txt"]
}

# Vector Store Configuration
VECTOR_STORE_CONFIG = {
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "index_dir": "faiss_index",
    "index_type": "IndexFlatIP"  # Inner product similarity
}

# RAG Engine Configuration
RAG_CONFIG = {
    "default_model": "llama3.2:3b",
    "temperature": 0.7,
    "top_k": 3,                 # Number of chunks to retrieve
    "max_tokens": 1000,         # Maximum tokens in response
    "top_p": 0.9               # Nucleus sampling parameter
}

# Streamlit UI Configuration
UI_CONFIG = {
    "page_title": "Domain Expert Chat",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Performance Optimization Settings
PERFORMANCE_CONFIG = {
    "enable_caching": True,     # Enable Streamlit caching
    "batch_size": 10,          # Batch size for document processing
    "max_file_size_mb": 50,    # Maximum file size in MB
    "show_progress": True      # Show progress bars
}

# Alternative Models (for different use cases)
ALTERNATIVE_MODELS = {
    "fast": "llama3.2:1b",     # Fastest, least capable
    "balanced": "llama3.2:3b", # Good balance of speed and quality
    "quality": "llama3.2:8b",  # Higher quality, slower
    "multilingual": "mistral:7b"  # Better for non-English
}

# Chunk Size Presets (for different document types)
CHUNK_PRESETS = {
    "small_docs": {"chunk_size": 300, "chunk_overlap": 30},
    "medium_docs": {"chunk_size": 500, "chunk_overlap": 50},
    "large_docs": {"chunk_size": 800, "chunk_overlap": 100},
    "technical_docs": {"chunk_size": 600, "chunk_overlap": 75}
}
