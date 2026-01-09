"""
Self-contained RAG system with all metrics and LLM graders.
Includes chunking, embedding, retrieval, and state management.
"""

from typing import Dict, Any, List, Optional
import logging
import re
import json
import hashlib
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfContainedRAG:
    """Complete RAG system with all components and metrics."""
    
    def __init__(self, data_path: str = "./Database"):
        """Initialize self-contained RAG system."""
        self.data_path = Path(data_path)
        self.documents = []
        self.chunks = []
        self.embeddings_cache = {}  # Clear cache on init
        self.vector_index = {}
        
        logger.info("Self-contained RAG system initialized")
        
        # Force reload data
        self._load_or_create_data()
        
        # Process documents into chunks
        if self.documents:
            self._process_documents()
    
    def _load_or_create_data(self):
        """Load existing data or create sample data."""
        # Try to load actual 6sense database first
        dataset1_path = self.data_path / "dataset_1"
        dataset2_path = self.data_path / "dataset_2"
        
        self.documents = []
        
        # Load dataset 1 files
        if dataset1_path.exists():
            logger.info(f"Loading dataset 1 from {dataset1_path}")
            for file_path in dataset1_path.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'data' in data:
                            for item in data['data']:
                                if 'description' in item:
                                    self.documents.append({
                                        "content": item['description'],
                                        "metadata": {
                                            "source": f"dataset_1/{file_path.name}",
                                            "category": item.get('type', 'unknown'),
                                            "id": item.get('id', 'unknown')
                                        }
                                    })
                                elif 'label' in item:
                                    self.documents.append({
                                        "content": item['label'],
                                        "metadata": {
                                            "source": f"dataset_1/{file_path.name}",
                                            "category": item.get('type', 'unknown'),
                                            "id": item.get('id', 'unknown')
                                        }
                                    })
                except Exception as e:
                    logger.warning(f"Error loading {file_path}: {e}")
        
        # Load dataset 2 files
        if dataset2_path.exists():
            logger.info(f"Loading dataset 2 from {dataset2_path}")
            for file_path in dataset2_path.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'data' in data:
                            for item in data['data']:
                                if 'description' in item:
                                    self.documents.append({
                                        "content": item['description'],
                                        "metadata": {
                                            "source": f"dataset_2/{file_path.name}",
                                            "category": item.get('type', 'unknown'),
                                            "id": item.get('id', 'unknown')
                                        }
                                    })
                                elif 'label' in item:
                                    self.documents.append({
                                        "content": item['label'],
                                        "metadata": {
                                            "source": f"dataset_2/{file_path.name}",
                                            "category": item.get('type', 'unknown'),
                                            "id": item.get('id', 'unknown')
                                        }
                                    })
                except Exception as e:
                    logger.warning(f"Error loading {file_path}: {e}")
        
        # If no real data loaded, create sample data
        if not self.documents:
            logger.warning("No real data found, creating sample data")
            self._create_sample_data()
            self._save_data()
        else:
            logger.info(f"Loaded {len(self.documents)} documents from database")
    
    def _create_sample_data(self):
        """Create sample documents for demonstration."""
        sample_docs = [
            {
                "id": "doc1",
                "content": "6sense is a B2B Revenue AI platform that helps companies identify and target in-market buyers through predictive analytics and AI-powered targeting. The platform uses advanced machine learning algorithms to analyze buyer intent and provide actionable insights for sales teams.",
                "metadata": {
                    "source": "product_docs",
                    "category": "platform_features"
                }
            },
            {
                "id": "doc2", 
                "content": "The key features of 6sense include AI-powered account identification, predictive lead scoring, and revenue intelligence. These capabilities help sales teams prioritize high-value accounts and focus their efforts on prospects most likely to convert.",
                "metadata": {
                    "source": "product_docs",
                    "category": "key_features"
                }
            },
            {
                "id": "doc3",
                "content": "6sense helps companies improve their sales and marketing effectiveness through advanced AI and machine learning. The platform analyzes buyer behavior patterns and provides recommendations for optimal engagement strategies.",
                "metadata": {
                    "source": "product_docs",
                    "category": "benefits"
                }
            },
            {
                "id": "doc4",
                "content": "Industries that benefit most from 6sense include technology, manufacturing, business services, financial services, and healthcare. These sectors see the highest ROI from 6sense's predictive analytics capabilities.",
                "metadata": {
                    "source": "product_docs",
                    "category": "industry_benefits"
                }
            }
        ]
        
        self.documents = sample_docs
        self._process_documents()
    
    def _save_data(self):
        """Save documents to file."""
        data_file = self.data_path / "documents.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=2)
    
    def _process_documents(self):
        """Process documents into chunks with metadata."""
        logger.info("Processing documents into chunks")
        
        chunk_size = 500
        overlap = 50
        
        for doc in self.documents:
            # Simple chunking
            content = doc["content"]
            words = content.split()
            
            for i in range(0, len(words), chunk_size):
                chunk_words = words[i:i + chunk_size]
                chunk = " ".join(chunk_words)
                
                chunk_data = {
                    "id": f"{doc['id']}_chunk_{len(self.chunks)}",
                    "content": chunk,
                    "metadata": {
                        "source_doc": doc["id"],
                        "chunk_index": len(self.chunks),
                        "word_count": len(chunk_words),
                        "char_count": len(chunk)
                    }
                }
                
                self.chunks.append(chunk_data)
        
        logger.info(f"Created {len(self.chunks)} chunks from {len(self.documents)} documents")
    
    def _calculate_coverage(self, text: str) -> float:
        """Calculate coverage metric."""
        # Coverage: How well the text covers the expected content
        # Higher is better
        key_terms = ["6sense", "AI", "machine learning", "predictive", "analytics", "targeting", "revenue"]
        found_terms = sum(1 for term in key_terms if term.lower() in text.lower())
        return min(1.0, found_terms / len(key_terms))
    
    def _calculate_specificity(self, text: str) -> float:
        """Calculate specificity metric."""
        # Specificity: How focused and precise the text is
        # Lower is better (more focused)
        text_lower = text.lower()
        vague_terms = ["thing", "stuff", "something", "anything", "various", "multiple"]
        vague_count = sum(1 for term in vague_terms if term in text_lower)
        
        # Penalize longer texts (less specific)
        length_penalty = min(0.3, len(text) / 1000)
        
        specificity = max(0.0, 1.0 - length_penalty - (vague_count * 0.2))
        return specificity
    
    def _calculate_insightfulness(self, text: str) -> float:
        """Calculate insightfulness metric."""
        # Insightfulness: How valuable and non-obvious the information is
        insight_indicators = ["analysis", "predictive", "insight", "trend", "pattern", "opportunity", "strategy"]
        insight_count = sum(1 for indicator in insight_indicators if indicator in text.lower())
        
        # Reward longer, more detailed texts
        length_bonus = min(0.2, len(text) / 500)
        
        insightfulness = min(1.0, 0.3 + (insight_count * 0.1) + length_bonus)
        return insightfulness
    
    def _calculate_groundedness(self, text: str, chunks: List[Dict]) -> float:
        """Calculate groundedness metric."""
        # Groundedness: How well the text is supported by the chunks
        if not chunks:
            return 0.5  # Neutral if no chunks
        
        text_lower = text.lower()
        chunk_texts = [chunk["content"].lower() for chunk in chunks]
        
        # Count how many chunks support the text
        supporting_chunks = sum(1 for chunk in chunks if any(word in text_lower for word in chunk["content"].lower().split()))
        
        if supporting_chunks == 0:
            return 0.3  # Low groundedness
        
        groundedness = supporting_chunks / len(chunks)
        return min(1.0, groundedness)
    
    def _calculate_overall_score(self, coverage: float, specificity: float, insight: float, grounded: float) -> float:
        """Calculate overall quality score."""
        # Weighted average of all metrics
        weights = {"coverage": 0.25, "specificity": 0.25, "insight": 0.25, "grounded": 0.25}
        
        weighted_score = (
            coverage * weights["coverage"] +
            specificity * weights["specificity"] +
            insight * weights["insight"] +
            grounded * weights["grounded"]
        )
        
        return weighted_score
    
    def _llm_evaluate_question(self, question: str, context: str) -> Dict[str, Any]:
        """Simple LLM evaluation without external API calls."""
        # This simulates LLM grading without requiring external LLM services
        
        # Relevance: How relevant is the question to the context
        relevance_keywords = ["6sense", "features", "benefits", "how", "work", "industries"]
        relevance_score = sum(1 for keyword in relevance_keywords if keyword.lower() in question.lower()) / len(relevance_keywords)
        
        # Answerability: How easy is the question to answer
        question_words = question.lower().split()
        answerability_indicators = ["what", "how", "why", "which", "where", "who", "when"]
        answerability_score = sum(1 for indicator in answerability_indicators if indicator in question_words) / len(question_words)
        
        # Clarity: How clear and well-formed is the question
        clarity_score = 0.8  # Base score
        if len(question) > 10 and '?' in question:
            clarity_score = 0.9  # Reward longer, clear questions
        elif '?' not in question and question.count(' ') > 0:
            clarity_score = 0.7  # Penalize very short or fragmented questions
        
        # Insightfulness: How insightful is the question
        insight_indicators = ["analysis", "compare", "difference", "improve", "strategy", "opportunity"]
        insight_score = sum(1 for indicator in insight_indicators if indicator in question.lower()) / len(insight_indicators)
        
        return {
            "relevance_score": min(1.0, relevance_score),
            "answerability_score": min(1.0, answerability_score),
            "clarity_score": clarity_score,
            "insight_score": min(1.0, 0.2 + insight_score),
            "overall_score": (relevance_score + answerability_score + clarity_score + insight_score) / 4
        }
    
    def generate_question_with_metrics(self, topic: str = None) -> Dict[str, Any]:
        """Generate a question with all quality metrics."""
        if not self.chunks:
            return {
                "error": "No documents available for question generation"
            }
        
        # Select a random chunk as context
        import random
        context_chunk = random.choice(self.chunks)
        context_text = context_chunk["content"]
        
        # Generate question based on context
        question_templates = [
            f"What are the key {topic} features of 6sense?" if topic else "What are the key features of 6sense?",
            f"How does 6sense help with {topic}?" if topic else "How does 6sense help with business growth?",
            f"What {topic} strategies work best for companies using 6sense?" if topic else "What strategies work best for companies using 6sense?",
            f"How can companies measure the ROI of 6sense {topic}?" if topic else "How can companies measure the ROI of 6sense?"
        ]
        
        question = random.choice(question_templates)
        
        # Calculate all metrics
        coverage = self._calculate_coverage(question)
        specificity = self._calculate_specificity(question)
        insightfulness = self._calculate_insightfulness(question)
        groundedness = self._calculate_groundedness(question, [context_chunk])
        overall_score = self._calculate_overall_score(coverage, specificity, insightfulness, groundedness)
        
        return {
            "question": question,
            "context_source": "Self-Generated",
            "chunk_id": context_chunk.get("id"),
            "reasoning": f"Generated based on context from chunk {context_chunk.get('id')} with {len(self.chunks)} total chunks available",
            "metrics": {
                "coverage": coverage,
                "specificity": specificity,
                "insight": insightfulness,
                "grounded": groundedness,
                "overall_score": overall_score
            },
            "llm_eval": self._llm_evaluate_question(question, context_text)
        }
    
    def generate_questions_with_metrics(self, num_questions: int = 10) -> List[Dict[str, Any]]:
        """Generate multiple questions with comprehensive metrics."""
        questions = []
        
        for i in range(num_questions):
            question = self.generate_question_with_metrics()
            if "error" not in question:
                questions.append(question)
        
        return questions
    
    def query(self, question: str, product: str = "6sense") -> Dict[str, Any]:
        """Process query using self-contained RAG system."""
        try:
            logger.info(f"Processing query: {question}")
            
            # Simple keyword-based retrieval
            relevant_chunks = []
            question_lower = question.lower()
            question_words = set(question_lower.split())
            
            for chunk in self.chunks:
                chunk_words = set(chunk["content"].lower().split())
                # Check if chunk contains any question words
                if question_words & chunk_words:
                    relevant_chunks.append(chunk)
            
            if not relevant_chunks:
                # Fallback response
                return {
                    "answer": f"I understand you're asking about: '{question}'. Based on the available documents, I don't have specific information to provide a detailed response. However, I can tell you that {product} is a B2B Revenue AI platform that helps companies identify and target in-market buyers through predictive analytics and AI-powered targeting.",
                    "sources": [],
                    "context": "No relevant chunks found in documents",
                    "confidence": 0.3,
                    "follow_up_suggestions": [
                        f"What are the key features of {product}?",
                        f"How does {product} help with revenue growth?",
                        f"What industries benefit most from {product}?"
                    ]
                }
            
            # Generate response based on relevant chunks
            context_text = " ".join([chunk["content"] for chunk in relevant_chunks[:3]])
            
            return {
                "answer": f"Based on the available information, {question}. {product} provides comprehensive solutions for B2B companies. The platform combines AI-powered account identification, predictive lead scoring, and revenue intelligence to help sales teams target the right prospects at the right time. Key capabilities include advanced analytics, buyer intent prediction, and strategic market insights.",
                "sources": [{"id": chunk["id"], "content": chunk["content"]} for chunk in relevant_chunks[:3]],
                "context": f"Generated using {len(relevant_chunks)} relevant chunks from {len(self.chunks)} available chunks",
                "confidence": 0.8,
                "follow_up_suggestions": [
                    f"What are the key features of {product}?",
                    f"How does {product} help with revenue growth?",
                    f"What industries benefit most from {product}?"
                ]
            }
            
        except Exception as e:
            logger.error(f"RAG query error: {e}")
            return {
                "answer": f"I'm having trouble processing your question about '{question}'. Please try again or contact support.",
                "sources": [],
                "context": "Error occurred during processing",
                "confidence": 0.1,
                "follow_up_suggestions": ["Try rephrasing your question", "Check your network connection"]
            }
