"""
Document processing module for RAG Assistant.
Handles PDF and TXT file ingestion and text splitting.
"""

import os
import tempfile
from typing import List, Dict, Any
from pathlib import Path

import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DocumentProcessor:
    """Handles document ingestion and text splitting for RAG system."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document processor.
        
        Args:
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        """
        Process uploaded file and return list of document chunks.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            List of Document objects with metadata
        """
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self._process_pdf(uploaded_file)
        elif file_extension == 'txt':
            return self._process_txt(uploaded_file)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    def _process_pdf(self, uploaded_file) -> List[Document]:
        """Process PDF file and extract text."""
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Extract text from PDF
            text = self._extract_pdf_text(tmp_file_path)
            
            # Create document with metadata
            doc = Document(
                page_content=text,
                metadata={
                    "source": uploaded_file.name,
                    "type": "pdf",
                    "file_size": len(uploaded_file.getvalue())
                }
            )
            
            # Split into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            # Add chunk metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                })
            
            return chunks
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
    
    def _process_txt(self, uploaded_file) -> List[Document]:
        """Process TXT file and extract text."""
        # Decode text content
        try:
            text = uploaded_file.getvalue().decode('utf-8')
        except UnicodeDecodeError:
            text = uploaded_file.getvalue().decode('latin-1')
        
        # Create document with metadata
        doc = Document(
            page_content=text,
            metadata={
                "source": uploaded_file.name,
                "type": "txt",
                "file_size": len(uploaded_file.getvalue())
            }
        )
        
        # Split into chunks
        chunks = self.text_splitter.split_documents([doc])
        
        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "chunk_id": i,
                "total_chunks": len(chunks)
            })
        
        return chunks
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    def get_chunk_stats(self, chunks: List[Document]) -> Dict[str, Any]:
        """
        Get statistics about processed chunks.
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {"total_chunks": 0, "avg_chunk_size": 0}
        
        total_chars = sum(len(chunk.page_content) for chunk in chunks)
        avg_chunk_size = total_chars / len(chunks)
        
        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": round(avg_chunk_size, 2),
            "total_characters": total_chars,
            "sources": list(set(chunk.metadata.get("source", "unknown") for chunk in chunks))
        }
