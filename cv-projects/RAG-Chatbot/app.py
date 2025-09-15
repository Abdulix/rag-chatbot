"""
Domain Expert Chat (RAG Assistant) - Streamlit App
A free, local RAG system using FAISS, HuggingFace embeddings, and Ollama LLM.
"""

import streamlit as st
import os
import logging
from pathlib import Path
from typing import List, Dict, Any

# Import our custom modules
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Page configuration
st.set_page_config(
    page_title="Domain Expert Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stats-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    /* Disable cursor during processing */
    .stSpinner {
        pointer-events: none;
    }
    .stSpinner ~ * {
        pointer-events: none;
        cursor: not-allowed !important;
    }
    /* Show not-allowed cursor on form elements when spinner is active */
    .stSpinner ~ div input {
        cursor: not-allowed !important;
    }
    .stSpinner ~ div button {
        cursor: not-allowed !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_components():
    """Initialize RAG components with caching."""
    # Initialize components
    doc_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    vector_store = VectorStore()
    rag_engine = RAGEngine(vector_store)
    
    return doc_processor, vector_store, rag_engine


def display_chat_message(message: str, is_user: bool = True):
    """Display a chat message with simple formatting."""
    if is_user:
        st.markdown(f"**Q:** {message}")
    else:
        st.markdown(f"**A:** {message}")


def display_sources(sources: List[Dict[str, Any]]):
    """Display source information - disabled for now."""
    # Sources display is disabled as per user request
    pass


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🤖 Domain Expert Chat</div>', 
                unsafe_allow_html=True)
    
    # Initialize components
    doc_processor, vector_store, rag_engine = initialize_components()
    
    # Sidebar
    with st.sidebar:
        st.header("Knowledge Base")
        
        # Vector store stats
        stats = vector_store.get_stats()
        st.write(f"Documents: {stats['total_documents']}")
        if stats['total_documents'] > 0:
            st.write(f"Dimensions: {stats['embedding_dimension']}")
        
        # Clear knowledge base
        if st.button("🗑️ Clear Knowledge Base", type="secondary"):
            vector_store.clear()
            st.cache_resource.clear()
            st.rerun()
    
    # Initialize chat history and processing state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False
    if "processing_question" not in st.session_state:
        st.session_state.processing_question = None
    if "form_key" not in st.session_state:
        st.session_state.form_key = 0
    
    # Main content area
    tab1, tab2 = st.tabs(["💬 Chat", "📄 Upload Documents"])
    
    with tab1:
        st.header("Chat with your documents")
        
        # Display chat history
        for message in st.session_state.messages:
            display_chat_message(message["content"], message["role"] == "user")
            
            # Display sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                display_sources(message["sources"])
        
        # Chat input (inside chat tab)
        with st.form("chat_form", clear_on_submit=True):
            prompt = st.text_input("Ask a question about your documents:", key="chat_input")
            submitted = st.form_submit_button("Ask")
            
            if submitted and prompt:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Check if vector store has documents
                if vector_store.is_empty():
                    response = "Please upload some documents first before asking questions."
                    sources = []
                else:
                    # Generate response with spinner
                    with st.spinner("🤔 Thinking..."):
                        result = rag_engine.query(prompt)
                        response = result["answer"]
                        sources = result["sources"]
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "sources": sources
                })
                
                # Rerun to update UI
                st.rerun()
    
    with tab2:
        st.header("Upload Documents")
        st.markdown("Upload a PDF file to build your knowledge base.")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            accept_multiple_files=False,
            help="Upload a single PDF file"
        )
        
        if uploaded_file:
            st.write(f"**Selected file:** {uploaded_file.name}")
            
            # Process file
            if st.button("📥 Process Document", type="primary"):
                with st.spinner("Processing document..."):
                    try:
                        # Process document
                        chunks = doc_processor.process_uploaded_file(uploaded_file)
                        
                        # Add to vector store
                        vector_store.add_documents(chunks)
                        
                        # Show results
                        st.success(f"✅ Successfully processed {uploaded_file.name} with {len(chunks)} chunks.")
                        
                        # Show chunk statistics
                        chunk_stats = doc_processor.get_chunk_stats(chunks)
                        st.info(f"📊 Average chunk size: {chunk_stats.get('avg_chunk_size', 0)} characters")
                        
                        # Clear cache to refresh components
                        st.cache_resource.clear()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        
        # Show current knowledge base info
        if not vector_store.is_empty():
            st.divider()
            st.subheader("📚 Current Knowledge Base")
            
            # Get unique sources
            sources = set()
            for doc in vector_store.documents:
                sources.add(doc.metadata.get('source', 'Unknown'))
            
            st.write(f"**Total documents:** {len(vector_store.documents)}")
            st.write(f"**Files:**")
            for source in sorted(sources):
                st.write(f"• {source}")


if __name__ == "__main__":
    main()
