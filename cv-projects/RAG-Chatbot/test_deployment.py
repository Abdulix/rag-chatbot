#!/usr/bin/env python3
"""
Test script to verify RAG Chatbot deployment
"""

import requests
import time
import sys

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            models = response.json().get('models', [])
            if any('llama3.2:3b' in model.get('name', '') for model in models):
                print("✅ llama3.2:3b model is available")
                return True
            else:
                print("❌ llama3.2:3b model not found")
                return False
        else:
            print("❌ Ollama is not responding")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Ollama")
        return False

def test_streamlit_connection():
    """Test if Streamlit app is running"""
    try:
        response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit app is running")
            return True
        else:
            print("❌ Streamlit app is not responding")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Streamlit app")
        return False

def test_app_functionality():
    """Test basic app functionality"""
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("✅ App is accessible")
            return True
        else:
            print("❌ App is not accessible")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot access app")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing RAG Chatbot Deployment")
    print("=" * 40)
    
    # Wait a bit for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Test Ollama
    ollama_ok = test_ollama_connection()
    
    # Test Streamlit
    streamlit_ok = test_streamlit_connection()
    
    # Test app
    app_ok = test_app_functionality()
    
    print("\n📊 Test Results:")
    print(f"Ollama: {'✅' if ollama_ok else '❌'}")
    print(f"Streamlit: {'✅' if streamlit_ok else '❌'}")
    print(f"App: {'✅' if app_ok else '❌'}")
    
    if all([ollama_ok, streamlit_ok, app_ok]):
        print("\n🎉 All tests passed! Your RAG Chatbot is ready!")
        print("🌐 Access your app at: http://localhost:8501")
        return 0
    else:
        print("\n❌ Some tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
