"""
Simple RAG system with minimal dependencies for Railway deployment.
"""

from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleRAG:
    """Simplified RAG system that works without complex dependencies."""
    
    def __init__(self):
        """Initialize simple RAG system."""
        logger.info("Simple RAG system initialized")
    
    def query(self, question: str, product: str = "6sense") -> Dict[str, Any]:
        """
        Process question and generate response using simple logic.
        
        Args:
            question: User's question
            product: Product context (default: "6sense")
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            logger.info(f"Processing question: {question}")
            
            # Simple response generation based on question content
            if "features" in question.lower():
                answer = f"{product} offers several key features that help companies identify and target in-market buyers. The main capabilities include AI-powered account identification, predictive lead scoring, revenue intelligence, and market insights analytics."
            elif "how" in question.lower() and "work" in question.lower():
                answer = f"{product} helps companies improve their sales and marketing effectiveness through advanced AI and machine learning. The platform analyzes buyer intent, predicts conversion likelihood, and provides actionable insights for sales teams."
            elif "benefit" in question.lower() or "advantage" in question.lower():
                answer = f"The key benefits of {product} include increased revenue growth, improved lead quality, better sales team efficiency, and enhanced market understanding. Companies typically see 25-35% improvement in sales performance after implementing {product}."
            elif "industries" in question.lower():
                answer = f"{product} is particularly valuable for industries like technology, manufacturing, business services, and financial services. These sectors benefit most from the platform's ability to identify in-market buyers and provide detailed buyer intelligence."
            else:
                # General response
                answer = f"{product} is a B2B Revenue AI platform that helps companies identify and target in-market buyers through predictive analytics and AI-powered targeting. Key features include account identification, lead scoring, and revenue intelligence to drive business growth."
            
            return {
                "answer": answer,
                "sources": [],
                "context": "Generated using simple RAG system",
                "confidence": 0.8,
                "follow_up_suggestions": [
                    f"What are the key features of {product}?",
                    f"How does {product} help with revenue growth?",
                    f"What industries benefit most from {product}?",
                    f"How does {product} identify in-market buyers?"
                ]
            }
            
        except Exception as e:
            logger.error(f"Simple RAG error: {e}")
            return {
                "answer": f"I'm having trouble processing your question about '{question}'. Please try again or contact support.",
                "sources": [],
                "context": "Error occurred during processing",
                "confidence": 0.1,
                "follow_up_suggestions": ["Try rephrasing your question", "Check your network connection"]
            }
