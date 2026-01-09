from typing import Dict, List, Any
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
                # Create a comprehensive prompt for proper answer generation
                full_prompt = f"""You are a B2B software expert specializing in ROI analysis and software recommendations. Based on the provided context, generate a comprehensive, insightful answer to the user's question.

CONTEXT:
{context_text}

USER QUESTION: {question}

INSTRUCTIONS:
1. Provide a direct, comprehensive answer based on the context
2. Include specific ROI data, metrics, and examples from the sources
3. Structure your answer with clear sections and bullet points
4. Focus on business value and practical insights
5. If the context contains ROI data, extract and highlight it
6. Be conversational but professional

ANSWER:"""
                
                response = self.llm.invoke(full_prompt)
                answer = response.content if hasattr(response, 'content') else str(response)
                
                # Enhance answer if no documents found
                if not retrieved_docs or len(retrieved_docs) == 0:
                    answer = f"""Based on your question about "{question}", here's what I can tell you about 6sense Revenue AI:

6sense is a leading B2B Revenue AI platform that helps companies identify and engage high-value customers. Here are the key aspects:

**Core Capabilities:**
- Predictive analytics to identify in-market buyers
- Real-time intent data from website visits and content consumption  
- Account-based marketing (ABM) capabilities
- Integration with existing CRM and marketing automation tools
- AI-powered lead scoring and prioritization

**Key Benefits:**
- Increased conversion rates through better targeting
- Shortened sales cycles with predictive insights
- Improved marketing ROI through data-driven decisions
- Enhanced customer understanding across all touchpoints

**Implementation:**
- Typically integrates with Salesforce, HubSpot, Marketo, and other major platforms
- Requires 2-4 weeks for initial setup
- Includes comprehensive training and ongoing support

Since you asked specifically about "{question.lower()}", could you let me know which aspect you'd like to explore further? I can provide more detailed information about implementation, pricing, specific features, or how it compares to alternatives."""
            else:
                # Fallback when no LLM is available - provide structured analysis
                answer = f"""Based on the available information about your question "{question}", here's what I found:

**Key Insights from Database:**
{context_text}

**Analysis:**
This information comes from the 6sense database and covers various aspects of the platform including features, benefits, and customer experiences. The data suggests strong ROI potential with documented success cases.

**Recommendation:**
For specific ROI calculations and implementation guidance, I recommend contacting 6sense directly for a personalized consultation based on your company's specific needs and scale."""
        except Exception as e:
            print(f"[ERROR] RAG pipeline failed: {e}")
            # Fallback response
            answer = f"I apologize, but I encountered an error processing your question about 6sense. Please try again or rephrase your question."
        
        # Return result in expected format
        return {
            "question": question,
            "retrieved_docs": retrieved_docs,  
            "answer": answer,
            "metadata": {
                "retrieval_count": len(retrieved_docs),
                "documents_used": len(retrieved_docs)
            }
        }


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
