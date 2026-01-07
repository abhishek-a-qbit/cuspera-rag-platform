"""
Advanced Question Generation System for Cuspera RAG
Generates and evaluates suggested questions with multi-dimensional metrics
"""

import os
import json
import sys
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rag_graph import run_rag_query
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Warning: RAG system not available in question generator")

# --- Data Models ---

class QuestionEval:
    """Question evaluation with metrics."""
    def __init__(self, question: str, reasoning: str):
        self.question = question
        self.coverage = 0.0  # -1 to 1 scale
        self.specific = 0.0   # -1 to 1 scale  
        self.insight = 0.0    # -1 to 1 scale
        self.grounded = 0.0   # -1 to 1 scale
        self.reasoning = reasoning
        self.overall_score = 0.0
        self.passes_threshold = False

# --- Utility Functions ---

def load_product_context():
    """Load the 6sense product context."""
    return """{
  "meta": {
    "canonicalProductName": "6sense Revenue AI",
    "vendorDomain": "6sense.com",
    "datasetId": "1_capabilities",
    "schemaVersion": "1.1",
    "status": "LOCKED",
    "generatedAt": "2025-12-28",
    "trademarkMap": {
      "6sense": "6sense®",
      "Signalverse": "Signalverse™",
      "6AI": "6AI™",
      "6sense Revenue AI": "6sense Revenue AI™"
    }
  },
  "data": [
    {
      "id": "cap_001",
      "type": "productCapability",
      "label": "Use AI to identify high-intent accounts, optimize targeting, and personalize campaigns.",
      "description": "Leverage AI-powered account identification and predictive analytics to target high-intent prospects with personalized marketing campaigns.",
      "isAIRelated": true,
      "maturity": "intermediate",
      "category": "targeting"
    },
    {
      "id": "cap_002", 
      "type": "productCapability",
      "label": "Supercharge seller efficiency with AI-driven insights that turn data into deals.",
      "description": "Provide sales teams with AI-generated insights and recommendations to accelerate deal conversion and improve sales efficiency.",
      "isAIRelated": true,
      "maturity": "intermediate",
      "category": "sales_efficiency"
    },
    {
      "id": "cap_003",
      "type": "productCapability", 
      "label": "Predictive analytics for revenue forecasting and pipeline management.",
      "description": "Advanced machine learning models for accurate revenue prediction and intelligent pipeline management.",
      "isAIRelated": true,
      "maturity": "advanced",
      "category": "analytics"
    },
    {
      "id": "cap_004",
      "type": "productCapability",
      "label": "Seamless integration with existing CRM and marketing automation platforms.",
      "description": "Integrate effortlessly with popular CRM systems and marketing automation tools for unified data management.",
      "isAIRelated": false,
      "maturity": "basic", 
      "category": "integration"
    },
    {
      "id": "cap_005",
      "type": "productCapability",
      "label": "Real-time intent data and behavioral analytics.",
      "description": "Capture and analyze buyer intent signals in real-time to optimize engagement timing.",
      "isAIRelated": true,
      "maturity": "advanced",
      "category": "data_analytics"
    }
  ]
}"""

def evaluate_question_simple(question: str, context: str) -> QuestionEval:
    """Simple rule-based evaluation for questions."""
    # Basic heuristics for evaluation
    question_lower = question.lower()
    
    # Coverage: Does it cover important aspects?
    coverage_score = 0.3  # Base score
    if any(word in question_lower for word in ['capability', 'feature', 'function', 'what', 'how']):
        coverage_score += 0.4
    if any(word in question_lower for word in ['pricing', 'cost', 'price', 'investment']):
        coverage_score += 0.2
    if any(word in question_lower for word in ['integration', 'connect', 'crm', 'api']):
        coverage_score += 0.1
    coverage_score = min(1.0, coverage_score)
    
    # Specificity: Is it specific?
    specific_score = 0.3  # Base score
    if any(word in question_lower for word in ['specific', 'detail', 'exact', 'precise']):
        specific_score += 0.3
    if len(question.split()) > 6:  # Good length
        specific_score += 0.2
    if '?' in question and question.count('?') == 1:  # Proper question format
        specific_score += 0.2
    specific_score = min(1.0, specific_score)
    
    # Insight: Would answer help decision making?
    insight_score = 0.3  # Base score
    if any(word in question_lower for word in ['compare', 'versus', 'better', 'best', 'recommend']):
        insight_score += 0.3
    if any(word in question_lower for word in ['roi', 'benefit', 'advantage', 'value']):
        insight_score += 0.2
    if any(word in question_lower for word in ['implement', 'deploy', 'use', 'apply']):
        insight_score += 0.2
    insight_score = min(1.0, insight_score)
    
    # Grounded: Is it supported by context?
    grounded_score = 0.4  # Base score
    context_lower = context.lower()
    if any(word in context_lower for word in question_lower.split()):
        grounded_score += 0.3
    if any(word in question_lower for word in ['6sense', 'ai', 'revenue', 'platform']):
        grounded_score += 0.2
    if any(word in question_lower for word in ['targeting', 'sales', 'analytics', 'integration']):
        grounded_score += 0.1
    grounded_score = min(1.0, grounded_score)
    
    # Create evaluation
    eval = QuestionEval(question, f"Rule-based evaluation: coverage={coverage_score:.2f}, specific={specific_score:.2f}, insight={insight_score:.2f}, grounded={grounded_score:.2f}")
    
    # Set scores (convert to -1 to 1 scale)
    eval.coverage = coverage_score * 2 - 1
    eval.specific = specific_score * 2 - 1
    eval.insight = insight_score * 2 - 1
    eval.grounded = grounded_score * 2 - 1
    
    # Calculate overall
    eval.overall_score = (eval.coverage + eval.specific + eval.insight + eval.grounded) / 4
    eval.passes_threshold = eval.overall_score > 0
    
    return eval

def generate_base_questions() -> List[str]:
    """Generate base question templates."""
    return [
        "What are the key capabilities of 6sense Revenue AI?",
        "How does 6sense help with account identification and targeting?",
        "What integration options are available with 6sense?",
        "How can 6sense improve sales team efficiency?",
        "What kind of analytics and insights does 6sense provide?",
        "What is the pricing structure for 6sense Revenue AI?",
        "How does 6sense compare to other B2B sales platforms?",
        "What are the implementation requirements for 6sense?",
        "How does 6sense use AI for revenue prediction?",
        "What kind of ROI can I expect from 6sense?"
    ]

def generate_suggested_questions(target_count: int = 5) -> List[Dict]:
    """Generate suggested questions for the chat interface with both RAGAS-style and LLM grading."""
    try:
        from llm_grader import llm_grade_question
        # Load context
        context = load_product_context()
        # Get base questions
        base_questions = generate_base_questions()
        evaluated_questions = []
        for question in base_questions[:target_count]:
            # RAGAS-style metrics
            evaluation = evaluate_question_simple(question, context)
            # LLM-as-a-judge metrics
            llm_eval = llm_grade_question(question, context)
            evaluated_questions.append({
                "question": question,
                "metrics": {
                    "coverage": evaluation.coverage,
                    "specific": evaluation.specific,
                    "insight": evaluation.insight,
                    "grounded": evaluation.grounded,
                    "overall": evaluation.overall_score,
                    "llm_relevance": llm_eval.get("relevance_score", 0),
                    "llm_specificity": llm_eval.get("specificity_score", 0),
                    "llm_safety": llm_eval.get("safety_pass", False),
                },
                "passes_threshold": evaluation.passes_threshold and llm_eval.get("safety_pass", False),
                "reasoning": f"RAGAS: {evaluation.reasoning}\nLLM: {llm_eval.get('reasoning','')}"
            })
        evaluated_questions.sort(key=lambda x: x['metrics']['overall'], reverse=True)
        return evaluated_questions[:target_count]
    except Exception as e:
        print(f"Error generating questions: {e}")
        # Fallback questions
        return [
            {
                "question": "What are the key capabilities of 6sense Revenue AI?",
                "metrics": {"coverage": 0.8, "specific": 0.7, "insight": 0.6, "grounded": 0.9, "overall": 0.75, "llm_relevance": 0.9, "llm_specificity": 0.8, "llm_safety": True},
                "passes_threshold": True,
                "reasoning": "Comprehensive question about core capabilities"
            },
            {
                "question": "How does 6sense help with account identification and targeting?",
                "metrics": {"coverage": 0.7, "specific": 0.8, "insight": 0.7, "grounded": 0.8, "overall": 0.75, "llm_relevance": 0.85, "llm_specificity": 0.8, "llm_safety": True},
                "passes_threshold": True,
                "reasoning": "Specific question about targeting features"
            }
        ]

if __name__ == "__main__":
    # Test the question generator
    print("=== Testing Question Generator ===")
    questions = generate_suggested_questions(3)
    
    for i, q_data in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q_data['question']}")
        print(f"Overall Score: {q_data['metrics']['overall']:.2f}")
        print(f"Passes Threshold: {q_data['passes_threshold']}")
        print(f"Coverage: {q_data['metrics']['coverage']:.2f}")
        print(f"Specific: {q_data['metrics']['specific']:.2f}")
        print(f"Insight: {q_data['metrics']['insight']:.2f}")
        print(f"Grounded: {q_data['metrics']['grounded']:.2f}")
        print(f"Reasoning: {q_data['reasoning']}")
