from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vector_store import VectorStore
from config import GOOGLE_API_KEY, TOP_K_RETRIEVAL
import os
import json


class RAGGraph:
    """Simple RAG pipeline without LangGraph complexity."""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize RAG pipeline."""
        self.vector_store = vector_store
        
        # Initialize LLM with Google Gemini (faster than Ollama)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            max_output_tokens=2048
        )
        
        # Create prompt template
        self.prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""You are an AI assistant helping users understand the 6sense Revenue AI platform.

Use the following context to answer the user's question. If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}

Provide a comprehensive and helpful answer:"""
        )
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the RAG pipeline."""
        question = state.get("question", "")
        
        # Step 1: Retrieve relevant documents
        retrieved_docs = self.vector_store.retrieve(question, top_k=TOP_K_RETRIEVAL)
        
        # Step 2: Format context from retrieved documents
        if retrieved_docs:
            context_text = "\n\n".join([
                f"Source: {doc['metadata'].get('dataset', 'Unknown')}\n{doc['content'][:500]}..."
                for doc in retrieved_docs
            ])
        else:
            context_text = "No relevant documents found."
        
        # Step 3: Generate answer using LLM
        full_prompt = self.prompt.format(question=question, context=context_text)
        response = self.llm.invoke(full_prompt)
        answer = response.content if hasattr(response, 'content') else str(response)
        
        # Return result in expected format
        return {
            "question": question,
            "retrieved_docs": retrieved_docs,  # Changed from retrieved_context to retrieved_docs
            "answer": answer,
            "metadata": {
                "retrieval_count": len(retrieved_docs),
                "documents_used": len(retrieved_docs)
            }
        }


def create_rag_graph(vector_store: VectorStore):
    """Create a RAG pipeline instance."""
    return RAGGraph(vector_store)


def run_rag_query(graph, question: str) -> Dict[str, Any]:
    """Run a query through the RAG pipeline."""
    state = {
        "question": question,
        "retrieved_docs": [],  # Changed to retrieved_docs
        "answer": "",
        "metadata": {}
    }
    
    # Execute pipeline
    result = graph.invoke(state)
    
    return {
        "question": result["question"],
        "answer": result["answer"],
        "retrieved_docs": result["retrieved_docs"],  # Changed from retrieved_context
        "metadata": result["metadata"]
    }
