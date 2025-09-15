"""
Vector store module for RAG Assistant.
Handles FAISS vector database operations with HuggingFace embeddings.
"""

import os
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.schema import Document


class VectorStore:
    """FAISS-based vector store with HuggingFace embeddings."""
    
    def __init__(self, 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 index_dir: str = "faiss_index"):
        """
        Initialize vector store.
        
        Args:
            embedding_model: HuggingFace model name for embeddings
            index_dir: Directory to store FAISS index files
        """
        self.embedding_model_name = embedding_model
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(exist_ok=True)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = None
        self.documents = []
        self.metadata = []
        
        # File paths
        self.index_path = self.index_dir / "faiss_index.bin"
        self.documents_path = self.index_dir / "documents.pkl"
        self.metadata_path = self.index_dir / "metadata.pkl"
        
        # Load existing index if available
        self._load_index()
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            return
        
        # Extract texts and metadata
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Generate embeddings with optimized settings
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False, convert_to_tensor=False)
        embeddings = embeddings.astype('float32')
        
        # Create new FAISS index if none exists
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for similarity
        
        # Add embeddings to index
        self.index.add(embeddings)
        
        # Store documents and metadata
        self.documents.extend(documents)
        self.metadata.extend(metadatas)
        
        # Save updated index
        self._save_index()
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Perform similarity search for the given query.
        
        Args:
            query: Search query string
            k: Number of top results to return
            
        Returns:
            List of dictionaries with document content and metadata
        """
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Generate query embedding with optimized settings
        query_embedding = self.embedding_model.encode([query], show_progress_bar=False, convert_to_tensor=False)
        query_embedding = query_embedding.astype('float32')
        
        # Search in FAISS index
        scores, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        # Retrieve documents and metadata
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue
                
            result = {
                "content": self.documents[idx].page_content,
                "metadata": self.metadata[idx],
                "score": float(score)
            }
            results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get vector store statistics.
        
        Returns:
            Dictionary with store statistics
        """
        if self.index is None:
            return {
                "total_documents": 0,
                "embedding_dimension": self.embedding_dim,
                "model_name": self.embedding_model_name
            }
        
        return {
            "total_documents": self.index.ntotal,
            "embedding_dimension": self.embedding_dim,
            "model_name": self.embedding_model_name,
            "index_type": "FAISS IndexFlatIP"
        }
    
    def clear(self) -> None:
        """Clear all documents from the vector store."""
        self.index = None
        self.documents = []
        self.metadata = []
        
        # Remove saved files
        for path in [self.index_path, self.documents_path, self.metadata_path]:
            if path.exists():
                path.unlink()
    
    def _save_index(self) -> None:
        """Save FAISS index and associated data to disk."""
        if self.index is None:
            return
        
        # Save FAISS index
        faiss.write_index(self.index, str(self.index_path))
        
        # Save documents and metadata
        with open(self.documents_path, 'wb') as f:
            pickle.dump(self.documents, f)
        
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def _load_index(self) -> None:
        """Load FAISS index and associated data from disk."""
        if not all(path.exists() for path in [self.index_path, self.documents_path, self.metadata_path]):
            return
        
        try:
            # Load FAISS index
            self.index = faiss.read_index(str(self.index_path))
            
            # Load documents and metadata
            with open(self.documents_path, 'rb') as f:
                self.documents = pickle.load(f)
            
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
                
        except Exception as e:
            print(f"Error loading index: {e}")
            # Reset if loading fails
            self.index = None
            self.documents = []
            self.metadata = []
    
    def is_empty(self) -> bool:
        """Check if the vector store is empty."""
        return self.index is None or self.index.ntotal == 0
