from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vector_store import VectorStore
from enhanced_vector_store import EnhancedVectorStore, create_enhanced_vector_store
from persistent_vector_store import PersistentVectorStore, create_persistent_vector_store
from config import GOOGLE_API_KEY, OPENAI_API_KEY, USE_OPENAI, TOP_K_RETRIEVAL, DATABASE_PATH
import os
import json


class RAGGraph:
    """Simple RAG pipeline without LangGraph complexity."""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize RAG pipeline."""
        self.vector_store = vector_store
        
        # Initialize LLM with OpenAI or Google Gemini
        if USE_OPENAI and OPENAI_API_KEY:
            print("[LLM] Using OpenAI GPT-4 for responses")
            self.llm = ChatOpenAI(
                model="gpt-4",
                api_key=OPENAI_API_KEY,
                temperature=0.7,
                max_tokens=2048
            )
        elif GOOGLE_API_KEY:
            print("[LLM] Using Google Gemini for responses")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.7,
                max_output_tokens=2048
            )
        else:
            print("[LLM] No API key found - using fallback responses only")
            self.llm = None
        
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
        mode = state.get("mode", "answer")  # answer | question_generation
        style = state.get("style", "default")  # default | loose
        target_count = int(state.get("target_count", 10) or 10)
        
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
        answer = ""
        try:
            if self.llm:
                if mode == "question_generation":
                    # Produce structured questions for the frontend (Streamlit) to consume.
                    # IMPORTANT: callers should still validate JSON; models can be imperfect.
                    q_prompt = f"""You are generating customer questions about B2B software.

Use the context below ONLY as a knowledge base. Do not invent facts.

CONTEXT:
{context_text}

TASK:
Generate EXACTLY {target_count} unique, grammatically correct questions. Each question must end with a '?'.

OUTPUT FORMAT (STRICT):
Return ONLY valid JSON. Either:
1) A JSON array of strings
OR
2) {{"questions": ["...", "..."]}}

PROMPT/FOCUS:
{question}
"""
                    response = self.llm.invoke(q_prompt)
                    answer = response.content if hasattr(response, 'content') else str(response)
                else:
                    # Draft answer (grounded)
                    draft_prompt = f"""You are a helpful B2B software assistant.

Use ONLY the context below. If the context is insufficient, say what is missing.

CONTEXT:
{context_text}

QUESTION:
{question}

Write a clear, helpful answer."""

                    response = self.llm.invoke(draft_prompt)
                    draft = response.content if hasattr(response, 'content') else str(response)

                    if style == "loose":
                        # Rewrite step: make it less rigid, more conversational, while staying grounded.
                        rewrite_prompt = f"""Rewrite the answer below to be more conversational, slightly more expansive, and easier to read.



ANSWER TO REWRITE:
{draft}
"""
                        response2 = self.llm.invoke(rewrite_prompt)
                        answer = response2.content if hasattr(response2, 'content') else str(response2)
                    else:
                        answer = draft
                


def create_rag_graph(vector_store: VectorStore):
    """Create a RAG pipeline instance."""
    return RAGGraph(vector_store)

def create_enhanced_rag_graph(use_enhanced: bool = True):
    """Create an enhanced RAG pipeline with optimal chunking."""
    if use_enhanced:
        print("[RAG] Creating enhanced RAG graph with optimal chunking...")
        vector_store = create_enhanced_vector_store(DATABASE_PATH, use_hybrid=False)
    else:
        print("[RAG] Creating standard RAG graph...")
        vector_store = VectorStore(use_hybrid=False)
        from data_loader import load_all_datasets
        documents = load_all_datasets(DATABASE_PATH)
        vector_store.index_documents(documents)
    
    return RAGGraph(vector_store)

def create_persistent_rag_graph(use_persistent: bool = True, force_reprocess: bool = False):
    """Create a persistent RAG pipeline with caching."""
    if use_persistent:
        print("[RAG] Creating persistent RAG graph with caching...")
        vector_store = create_persistent_vector_store(DATABASE_PATH, use_hybrid=False, force_reprocess=force_reprocess)
    else:
        print("[RAG] Creating enhanced RAG graph...")
        vector_store = create_enhanced_vector_store(DATABASE_PATH, use_hybrid=False)
    
    return RAGGraph(vector_store)


def run_rag_query(
    graph,
    question: str,
    mode: str = "answer",
    style: str = "default",
    target_count: Optional[int] = None,
) -> Dict[str, Any]:
    """Run a query through the RAG pipeline."""
    state = {
        "question": question,
        "mode": mode or "answer",
        "style": style or "default",
        "target_count": target_count,
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
