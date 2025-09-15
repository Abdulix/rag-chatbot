"""
Example usage of the RAG Assistant components.
This script demonstrates how to use the core modules programmatically.
"""

import os
from pathlib import Path
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine


def create_sample_document():
    """Create a sample document for testing."""
    sample_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create 
    intelligent machines that can perform tasks that typically require human intelligence. 
    These tasks include learning, reasoning, problem-solving, perception, and language understanding.
    
    Machine Learning (ML) is a subset of AI that focuses on the development of algorithms 
    and statistical models that enable computer systems to improve their performance on a 
    specific task through experience, without being explicitly programmed.
    
    Deep Learning is a subset of machine learning that uses artificial neural networks 
    with multiple layers (deep neural networks) to model and understand complex patterns 
    in data. It has been particularly successful in areas such as image recognition, 
    natural language processing, and speech recognition.
    
    Natural Language Processing (NLP) is a field of AI that focuses on the interaction 
    between computers and humans through natural language. The ultimate objective of NLP 
    is to read, decipher, understand, and make sense of human language in a valuable way.
    
    Computer Vision is a field of AI that trains computers to interpret and understand 
    the visual world. Using digital images from cameras and videos and deep learning models, 
    machines can accurately identify and classify objects and react to what they see.
    """
    
    # Create sample document
    sample_file = Path("sample_ai_document.txt")
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    return sample_file


def main():
    """Demonstrate RAG Assistant functionality."""
    print("🤖 RAG Assistant Example Usage")
    print("=" * 40)
    
    # Create sample document
    print("📄 Creating sample document...")
    sample_file = create_sample_document()
    print(f"✅ Created: {sample_file}")
    
    try:
        # Initialize components
        print("\n🔧 Initializing components...")
        doc_processor = DocumentProcessor(chunk_size=200, chunk_overlap=50)
        vector_store = VectorStore(index_dir="example_faiss_index")
        rag_engine = RAGEngine(vector_store, model_name="llama3.2:3b")
        print("✅ Components initialized")
        
        # Process document
        print("\n📚 Processing document...")
        with open(sample_file, "rb") as f:
            # Simulate uploaded file object
            class MockFile:
                def __init__(self, content, name):
                    self._content = content
                    self.name = name
                
                def getvalue(self):
                    return self._content
            
            mock_file = MockFile(f.read(), sample_file.name)
            chunks = doc_processor.process_uploaded_file(mock_file)
        
        print(f"✅ Processed into {len(chunks)} chunks")
        
        # Add to vector store
        print("\n🗄️ Adding to vector store...")
        vector_store.add_documents(chunks)
        print("✅ Documents added to vector store")
        
        # Show vector store stats
        stats = vector_store.get_stats()
        print(f"📊 Vector store stats: {stats}")
        
        # Example queries
        queries = [
            "What is artificial intelligence?",
            "What is the difference between machine learning and deep learning?",
            "What is natural language processing?",
            "How does computer vision work?"
        ]
        
        print("\n💬 Running example queries...")
        for i, query in enumerate(queries, 1):
            print(f"\n--- Query {i} ---")
            print(f"Q: {query}")
            
            # Get response
            result = rag_engine.query(query)
            print(f"A: {result['answer']}")
            
            # Show sources
            if result['sources']:
                print("📚 Sources:")
                for source in result['sources']:
                    print(f"  - {source['source']} (Score: {source['relevance_score']:.3f})")
        
        print("\n🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("\nAnd you have a model installed:")
        print("  ollama pull llama3.2:3b")
    
    finally:
        # Cleanup
        if sample_file.exists():
            sample_file.unlink()
            print(f"\n🧹 Cleaned up: {sample_file}")


if __name__ == "__main__":
    main()
