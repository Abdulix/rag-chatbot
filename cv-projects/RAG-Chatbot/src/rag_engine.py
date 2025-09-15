"""
RAG Engine module for Domain Expert Chat.
Handles retrieval and response generation using Ollama LLM.
"""

import ollama
import hashlib
from typing import List, Dict, Any, Optional


class RAGEngine:
    """RAG engine that combines retrieval with Ollama LLM generation."""
    
    def __init__(self, 
                 vector_store,
                 model_name: str = "llama3.2:3b",
                 temperature: float = 0.1,
                 top_k: int = 2):
        """
        Initialize RAG engine.
        
        Args:
            vector_store: VectorStore instance for document retrieval
            model_name: Ollama model name to use
            temperature: LLM temperature for response generation
            top_k: Number of top documents to retrieve
        """
        self.vector_store = vector_store
        self.model_name = model_name
        self.temperature = temperature
        self.top_k = top_k
        
        # Simple cache for recent queries
        self._query_cache = {}
        self._cache_size = 10
        
        # Check if Ollama is running and model is available
        self._check_ollama_setup()
    
    def _check_ollama_setup(self) -> None:
        """Check if Ollama is running and model is available."""
        try:
            # Check if Ollama is running
            models = ollama.list()
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models:
                print(f"Warning: Model '{self.model_name}' not found. Available models: {available_models}")
                print(f"Please run: ollama pull {self.model_name}")
                
        except Exception as e:
            # Silently handle Ollama not being available
            pass
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Process a user question and return a response with sources.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing answer, sources, and metadata
        """
        # Check cache first for speed
        query_hash = hashlib.md5(question.lower().strip().encode()).hexdigest()
        if query_hash in self._query_cache:
            return self._query_cache[query_hash]
        
        # Retrieve relevant documents
        retrieved_docs = self.vector_store.similarity_search(question, k=self.top_k)
        
        if not retrieved_docs:
            return {
                "answer": "I don't have any relevant information to answer your question. Please upload some documents first.",
                "sources": [],
                "retrieved_docs": [],
                "model_used": self.model_name
            }
        
        # Prepare context from retrieved documents
        context = self._prepare_context(retrieved_docs)
        
        # Generate response using Ollama
        answer = self._generate_response(question, context)
        
        # Format sources
        sources = self._format_sources(retrieved_docs)
        
        result = {
            "answer": answer,
            "sources": sources,
            "retrieved_docs": retrieved_docs,
            "model_used": self.model_name,
            "context_length": len(context)
        }
        
        # Cache the result
        self._query_cache[query_hash] = result
        
        # Manage cache size
        if len(self._query_cache) > self._cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self._query_cache))
            del self._query_cache[oldest_key]
        
        return result
    
    def _prepare_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Prepare context string from retrieved documents.
        
        Args:
            retrieved_docs: List of retrieved document dictionaries
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return ""
        
        # Use multiple documents for better context
        context_parts = []
        total_length = 0
        max_length = 1500  # Increased for better context
        
        for doc in retrieved_docs:
            content = doc['content']
            if total_length + len(content) <= max_length:
                context_parts.append(content)
                total_length += len(content)
            else:
                # Add partial content if there's space
                remaining_space = max_length - total_length
                if remaining_space > 100:  # Only add if meaningful space
                    context_parts.append(content[:remaining_space] + "...")
                break
        
        return "\n\n".join(context_parts)
    
    def _generate_response(self, question: str, context: str) -> str:
        """
        Generate response using Ollama LLM.
        
        Args:
            question: User's question
            context: Retrieved context from documents
            
        Returns:
            Generated answer string
        """
        # Create prompt for the LLM
        prompt = self._create_prompt(question, context)
        
        try:
            # Generate response using Ollama with optimized settings for speed
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'top_p': 0.7,
                    'max_tokens': 400,
                    'num_predict': 400,
                    'stop': ['\n\n', 'Context:', 'Question:', 'Answer:'],
                    'repeat_penalty': 1.1,
                    'num_ctx': 2048
                }
            )
            
            # Get the raw response
            raw_response = response['response'].strip()
            
            # Clean up any unwanted prefixes
            prefixes_to_remove = ['Q:', 'A:', 'Question:', 'Answer:', 'Response:']
            cleaned_response = raw_response
            
            for prefix in prefixes_to_remove:
                if cleaned_response.startswith(prefix):
                    cleaned_response = cleaned_response[len(prefix):].strip()
            
            # If response seems incomplete (ends with colon or is very short), try to get more
            if cleaned_response.endswith(':') or len(cleaned_response) < 50:
                # Try generating again with a different approach
                try:
                    retry_prompt = f"""Use ONLY the context below to answer the question. Do not provide generic information.

Context: {context}

Question: {question}

Answer based on the context:"""
                    
                    retry_response = ollama.generate(
                        model=self.model_name,
                        prompt=retry_prompt,
                        options={
                            'temperature': self.temperature,
                            'top_p': 0.7,
                            'max_tokens': 400,
                            'num_predict': 400,
                            'stop': ['\n\n', 'Context:', 'Question:'],
                            'repeat_penalty': 1.1,
                            'num_ctx': 2048
                        }
                    )
                    
                    retry_text = retry_response['response'].strip()
                    for prefix in prefixes_to_remove:
                        if retry_text.startswith(prefix):
                            retry_text = retry_text[len(prefix):].strip()
                    
                    if len(retry_text) > len(cleaned_response):
                        cleaned_response = retry_text
                        
                except:
                    pass  # Use original response if retry fails
            
            return cleaned_response
            
        except Exception as e:
            return f"❌ Ollama is not available. Please install and start Ollama to enable chat functionality.\n\nTo fix this:\n1. Install Ollama from https://ollama.ai\n2. Start the service: `ollama serve`\n3. Pull a model: `ollama pull llama3.2:3b`"
    
    def _create_prompt(self, question: str, context: str) -> str:
        """
        Create prompt for the LLM.
        
        Args:
            question: User's question
            context: Retrieved context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You must answer based ONLY on the provided context. Do not provide generic information.

Context: {context}

Question: {question}

Based on the context above, provide a detailed answer. If the context doesn't contain enough information to answer the question, say "The context doesn't contain enough information to answer this question." Start your response directly:"""
        
        return prompt
    
    def _format_sources(self, retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format sources for display.
        
        Args:
            retrieved_docs: List of retrieved document dictionaries
            
        Returns:
            List of formatted source dictionaries
        """
        sources = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            source = {
                "id": i,
                "source": doc['metadata'].get('source', 'Unknown'),
                "relevance_score": round(doc['score'], 3),
                "chunk_id": doc['metadata'].get('chunk_id', 'N/A'),
                "preview": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
            }
            sources.append(source)
        
        return sources
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Ollama models.
        
        Returns:
            List of available model names
        """
        try:
            models = ollama.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            # Return empty list if Ollama is not available
            return []
    
    def change_model(self, new_model_name: str) -> bool:
        """
        Change the LLM model.
        
        Args:
            new_model_name: Name of the new model to use
            
        Returns:
            True if model change was successful, False otherwise
        """
        available_models = self.get_available_models()
        
        if new_model_name in available_models:
            self.model_name = new_model_name
            return True
        else:
            print(f"Model '{new_model_name}' not available. Available models: {available_models}")
            return False
