# Domain Expert Chat (RAG Assistant)

A free, local RAG (Retrieval-Augmented Generation) system that runs entirely offline using FAISS vector database, HuggingFace embeddings, and Ollama LLM. Deployable on Streamlit Cloud with zero API costs.

## 🚀 Features

- **100% Free**: No API costs, runs entirely locally
- **Fast Inference**: Optimized for speed with efficient embeddings and small chunks
- **Document Support**: Upload PDF and TXT files
- **Smart Chunking**: Automatic text splitting with overlap for better context
- **Vector Search**: FAISS-based similarity search with HuggingFace embeddings
- **Local LLM**: Ollama integration for response generation
- **Persistent Storage**: FAISS index saved across sessions
- **Modern UI**: Clean Streamlit interface with chat history
- **Source Attribution**: Shows which documents were used for each answer

## 🛠️ Tech Stack

- **Language**: Python 3.11
- **UI Framework**: Streamlit
- **RAG Framework**: LangChain (minimal use)
- **Vector Database**: FAISS (local, free)
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: Ollama (local, free)
- **Document Processing**: PyPDF2 for PDF parsing

## 📋 Prerequisites

### 1. Install Ollama

**Windows:**
```bash
# Download and install from https://ollama.ai
# Or use winget
winget install Ollama.Ollama
```

**macOS:**
```bash
# Download and install from https://ollama.ai
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama Service

```bash
ollama serve
```

### 3. Pull a Model

```bash
# Recommended lightweight model
ollama pull llama3.2:3b

# Alternative models
ollama pull llama3.2:1b    # Even smaller
ollama pull mistral:7b     # Larger, more capable
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd RAG-Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### 1. Upload Documents

1. Go to the "Upload Documents" tab
2. Select PDF or TXT files
3. Click "Process Documents"
4. Wait for processing to complete

### 2. Chat with Your Documents

1. Go to the "Chat" tab
2. Ask questions about your uploaded documents
3. View answers with source attribution
4. Adjust settings in the sidebar (model, temperature, etc.)

### 3. Settings

- **Model Selection**: Choose from available Ollama models
- **Temperature**: Control response creativity (0.0-1.0)
- **Retrieved Chunks**: Number of document chunks to use (1-10)

## 🏗️ Project Structure

```
RAG-Chatbot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/
│   ├── __init__.py
│   ├── document_processor.py  # Document ingestion and splitting
│   ├── vector_store.py        # FAISS vector database operations
│   └── rag_engine.py          # RAG retrieval and generation
└── faiss_index/          # Generated vector index storage
    ├── faiss_index.bin
    ├── documents.pkl
    └── metadata.pkl
```

## ⚙️ Configuration

### Document Processing

- **Chunk Size**: 500 characters (configurable in `DocumentProcessor`)
- **Chunk Overlap**: 50 characters for better context
- **Supported Formats**: PDF, TXT

### Vector Store

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Index Type**: FAISS IndexFlatIP (inner product similarity)
- **Storage**: Local files in `faiss_index/` directory

### RAG Engine

- **Default Model**: `llama3.2:3b`
- **Temperature**: 0.7 (configurable)
- **Top-K Retrieval**: 3 chunks (configurable)

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path to `app.py`
5. Deploy!

**Note**: For Streamlit Cloud deployment, you'll need to modify the code to use a cloud-based Ollama service or switch to a different LLM provider.

### Local Deployment

```bash
# Run with custom port
streamlit run app.py --server.port 8502

# Run with custom host
streamlit run app.py --server.address 0.0.0.0
```

## 🔧 Troubleshooting

### Common Issues

1. **"No Ollama models found"**
   - Ensure Ollama is running: `ollama serve`
   - Pull a model: `ollama pull llama3.2:3b`

2. **"Error generating response"**
   - Check if Ollama service is running
   - Verify model is available: `ollama list`

3. **Slow performance**
   - Use smaller models (e.g., `llama3.2:1b`)
   - Reduce chunk size in `DocumentProcessor`
   - Decrease `top_k` parameter

4. **Memory issues**
   - Use smaller embedding models
   - Process documents in smaller batches
   - Clear knowledge base regularly

### Performance Optimization

- **For Speed**: Use `llama3.2:1b` model
- **For Quality**: Use `llama3.2:3b` or larger models
- **For Memory**: Reduce chunk size to 300-400 characters
- **For Accuracy**: Increase chunk overlap to 100 characters

## 📊 System Requirements

### Minimum Requirements

- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **CPU**: 2 cores (4 cores recommended)
- **Python**: 3.11+

### Recommended Requirements

- **RAM**: 8GB+
- **Storage**: 5GB+ free space
- **CPU**: 4+ cores
- **GPU**: Optional (for faster embeddings)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing UI framework
- [LangChain](https://langchain.com/) for RAG utilities
- [FAISS](https://faiss.ai/) for efficient vector search
- [HuggingFace](https://huggingface.co/) for embeddings
- [Ollama](https://ollama.ai/) for local LLM inference

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information

---

**Happy chatting with your documents! 🤖📚**
