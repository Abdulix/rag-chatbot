"""
Setup script for Domain Expert Chat (RAG Assistant)
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def check_ollama():
    """Check if Ollama is installed and running."""
    print("🔍 Checking Ollama installation...")
    
    # Check if ollama command exists
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            print(f"   Version: {result.stdout.strip()}")
        else:
            print("❌ Ollama is not installed")
            return False
    except:
        print("❌ Ollama is not installed")
        return False
    
    # Check if ollama service is running
    try:
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama service is running")
            models = result.stdout.strip()
            if models:
                print(f"   Available models: {models}")
            else:
                print("   No models installed yet")
            return True
        else:
            print("❌ Ollama service is not running")
            print("   Please run: ollama serve")
            return False
    except:
        print("❌ Cannot connect to Ollama service")
        return False


def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing dependencies")


def pull_ollama_model():
    """Pull a lightweight Ollama model."""
    print("🤖 Setting up Ollama model...")
    
    # Check if llama3.2:3b is already installed
    try:
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        if "llama3.2:3b" in result.stdout:
            print("✅ llama3.2:3b model is already installed")
            return True
    except:
        pass
    
    # Pull the model
    return run_command("ollama pull llama3.2:3b", 
                      "Pulling llama3.2:3b model")


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = ["faiss_index", "src"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def main():
    """Main setup function."""
    print("🚀 Setting up Domain Expert Chat (RAG Assistant)")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Install Python dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Check Ollama
    ollama_ok = check_ollama()
    
    if ollama_ok:
        # Pull model if needed
        pull_ollama_model()
    else:
        print("\n⚠️  Ollama setup incomplete. Please:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Start the service: ollama serve")
        print("   3. Pull a model: ollama pull llama3.2:3b")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\nTo run the application:")
    print("   streamlit run app.py")
    print("\nTo start Ollama service (if not running):")
    print("   ollama serve")
    
    return True


if __name__ == "__main__":
    main()
