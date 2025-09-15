# Production Dockerfile for RAG Chatbot with Ollama
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Ollama
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama at runtime instead of build time to avoid network issues
# This will be handled by the start.sh script

# Copy requirements first for better caching
COPY requirements_production.txt .
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir --default-timeout=500 -r requirements_production.txt

#RUN pip install --no-cache-dir -r requirements_production.txt

# Note: Model pulling moved to runtime in start.sh to avoid build failures

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p faiss_index

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV OLLAMA_MODEL=llama3.2:3b

# Expose ports
EXPOSE 8501 11434

# Copy and setup startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the startup script
CMD ["/app/start.sh"]
