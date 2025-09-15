#!/bin/bash

# RAG Chatbot Startup Script
echo "🚀 Starting RAG Chatbot..."

# Start Ollama in background
echo "📦 Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to initialize..."
sleep 15

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama failed to start"
    exit 1
fi

echo "✅ Ollama is running"

# Verify model is available (should be pre-installed)
if ollama list | grep -q "llama3.2:3b"; then
    echo "✅ Model llama3.2:3b is ready (pre-installed)"
else
    echo "📥 Model not found, pulling llama3.2:3b..."
    ollama pull llama3.2:3b
    if ollama list | grep -q "llama3.2:3b"; then
        echo "✅ Model llama3.2:3b is ready"
    else
        echo "❌ Failed to pull model"
        exit 1
    fi
fi

# Start Streamlit
echo "🌐 Starting Streamlit application..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
