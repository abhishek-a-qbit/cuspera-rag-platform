"""
Data-Driven Question Generation System with REAL Metrics
Uses RAG graph to generate questions from actual data with proper evaluation
"""

import os
import sys
import json
import re
import numpy as np
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rag_graph import create_persistent_rag_graph, run_rag_query
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"Warning: RAG system not available: {e}")
    RAG_AVAILABLE = False

class DataDrivenQuestionGenerator:
    """Generates questions using RAG graph with REAL evaluation metrics."""
    
    def __init__(self):
        """Initialize with persistent RAG graph."""
        self.rag_graph = None
        self.embedding_model = None
        self.nlp_model = None
        
        if RAG_AVAILABLE:
            try:
                self.rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
                print("[QGen] Initialized with persistent RAG graph")
            except Exception as e:
                print(f"[QGen] Error initializing RAG graph: {e}")
                self.rag_graph = None
        else:
            print("[QGen] RAG system not available")
        
        # Initialize embedding model for semantic similarity
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("[QGen] Embedding model loaded")
        except Exception as e:
            print(f"[QGen] Could not load embedding model: {e}")
            self.embedding_model = None
        
        # Initialize spaCy for NLP metrics
        try:
            import spacy
            self.nlp_model = spacy.load("en_core_web_sm")
            print("[QGen] spaCy NLP model loaded")
        except Exception as e:
            print(f"[QGen] Could not load spaCy: {e}")
            self.nlp_model = None
    
    def generate_question_from_data(self, topic: str = None, num_questions: int = 1) -> List[Dict[str, Any]]:
        """Generate questions using RAG graph invoke function."""
        if not self.rag_graph:
            return self._fallback_questions(topic, num_questions)
        
        questions = []
        
        for i in range(num_questions):
            try:
                # Generate question using RAG graph
                question_prompt = self._create_question_prompt(topic, i)
                
                # Use RAG graph to generate question
                result = run_rag_query(
                    self.rag_graph,
                    question_prompt,
                    mode="question_generation",
                    style="default",
                    target_count=1
                )
                
                # Extract question from RAG response
                question = self._extract_question_from_response(result, topic, i)
                
                # Calculate question metrics with REAL LLM grading
                question_metrics = self._calculate_question_metrics(question)
                
                # Generate answer for this question
                answer_result = run_rag_query(self.rag_graph, question)
                answer = answer_result.get("answer", "")
                retrieved_docs = answer_result.get("retrieved_docs", [])
                context = "\n".join([doc.get("content", "")[:500] for doc in retrieved_docs])
                
                # Calculate answer metrics
                answer_metrics = self._calculate_answer_metrics(question, answer, context)
                
                questions.append({
                    "question": question,
                    "answer": answer,
                    "context_source": "RAG Graph Invoke",
                    "chunk_id": f"rag_generated_{i}",
                    "reasoning": f"Generated using RAG graph with topic: {topic or '6sense'}",
                    "metrics": question_metrics,
                    "answer_metrics": answer_metrics,
                    "retrieved_sources": len(retrieved_docs)
                })
                
            except Exception as e:
                print(f"[QGen] Error generating question {i}: {e}")
                # Fallback question
                fallback = self._create_fallback_question(topic, i)
                questions.append(fallback)
        
        return questions
    
    def _llm_grade_metric(self, text: str, metric_name: str, metric_type: str = "question") -> int:
        """Real LLM grading using actual API calls with few-shot examples."""
        from langchain_core.prompts import ChatPromptTemplate
        
        # Few-shot examples for each metric
        examples = {
            "coverage": {
                "question": [
                    {"text": "What is 6sense?", "score": 2, "reason": "Too basic, doesn't cover key aspects"},
                    {"text": "How does 6sense's predictive AI identify in-market accounts across multiple buying stages?", "score": 5, "reason": "Covers specific features and use cases"}
                ],
                "answer": [
                    {"text": "6sense is a platform.", "score": 2, "reason": "Incomplete, missing key details"},
                    {"text": "6sense Revenue AI helps identify in-market buyers using predictive analytics, intent data, and account-based marketing across awareness, consideration, and decision stages.", "score": 5, "reason": "Comprehensive coverage of features and stages"}
                ]
            },
            "specificity": {
                "question": [
                    {"text": "How does the platform work?", "score": 1, "reason": "Extremely vague"},
                    {"text": "How do I configure OAuth 2.0 with PKCE for 6sense API integration?", "score": 5, "reason": "Very specific with concrete technical details"}
                ],
                "answer": [
                    {"text": "You can configure it in settings.", "score": 1, "reason": "Vague, no specific steps"},
                    {"text": "To configure OAuth 2.0 with PKCE: 1) Generate code_verifier (43-128 char random string), 2) Create code_challenge using SHA256(code_verifier), 3) Request authorization with code_challenge, 4) Exchange code for token with code_verifier.", "score": 5, "reason": "Step-by-step with specific technical parameters"}
                ]
            },
            "insightfulness": {
                "question": [
                    {"text": "What features does 6sense have?", "score": 2, "reason": "Surface-level question"},
                    {"text": "Why does 6sense's account-based approach outperform lead-based marketing for enterprise B2B, and when should you combine both strategies?", "score": 5, "reason": "Explores why, trade-offs, and strategic decisions"}
                ],
                "answer": [
                    {"text": "6sense uses AI for targeting.", "score": 2, "reason": "Superficial, no depth"},
                    {"text": "6sense's AI analyzes intent signals across 1000+ sources. This matters because traditional lead scoring misses 70% of buyer committee members. However, for SMB sales (<$50k deals), lead-based may be more cost-effective due to shorter sales cycles.", "score": 5, "reason": "Explains why, provides context, discusses trade-offs"}
                ]
            },
            "groundedness": {
                "question": [
                    {"text": "Does 6sense cure cancer?", "score": 1, "reason": "Not answerable from product data"},
                    {"text": "What pricing tiers does 6sense offer?", "score": 5, "reason": "Factual question answerable from documentation"}
                ],
                "answer": [
                    {"text": "6sense is the best platform ever and everyone should use it.", "score": 1, "reason": "Opinion-based, not grounded in facts"},
                    {"text": "According to the documentation, 6sense offers three tiers: Team ($X/mo), Business ($Y/mo), and Enterprise (custom pricing).", "score": 5, "reason": "Factual claims with clear attribution"}
                ]
            }
        }
        
        # Build prompt with few-shot examples
        prompt_template = f"""You are evaluating {metric_type} quality on the metric: {metric_name}.

Rate on a scale of 1-5:
1 = Very poor
2 = Below average  
3 = Average
4 = Good
5 = Excellent

Examples:
"""
        
        for ex in examples.get(metric_name, {}).get(metric_type, []):
            prompt_template += f"\n{metric_type.capitalize()}: {ex['text']}\nScore: {ex['score']}\nReason: {ex['reason']}\n"
        
        prompt_template += f"\n\nNow evaluate this {metric_type}:\n{text}\n\nProvide ONLY a number from 1 to 5:"
        
        try:
            if not self.rag_graph or not self.rag_graph.llm:
                print(f"[LLM Grader] No LLM available, using fallback score")
                return 3
            
            prompt = ChatPromptTemplate.from_template(prompt_template)
            messages = prompt.format_messages()
            response = self.rag_graph.llm.invoke(messages)
            
            # Extract score from response
            score_text = response.content.strip()
            # Try to find a number 1-5
            match = re.search(r'[1-5]', score_text)
            if match:
                score = int(match.group())
                print(f"[LLM Grader] {metric_name} ({metric_type}): {score}/5")
                return score
            else:
                print(f"[LLM Grader] Could not parse score from: {score_text}")
                return 3  # Default to middle score if parsing fails
                
        except Exception as e:
            print(f"[LLM Grader] Error: {e}")
            return 3  # Fallback score
    
    def _calculate_groundedness_math(self, question: str) -> float:
        """Calculate if question can be answered from available data."""
        if not self.rag_graph or not self.rag_graph.vector_store:
            return 0.40  # Low confidence if no data source
        
        try:
            # Retrieve relevant documents for this question
            retrieved_docs = self.rag_graph.vector_store.retrieve(question, top_k=3)
            
            if not retrieved_docs:
                return 0.40  # Question can't be answered from data
            
            # Calculate relevance scores using embeddings
            if self.embedding_model:
                q_embedding = self.embedding_model.encode(question)
                
                max_similarity = 0.0
                for doc in retrieved_docs:
                    doc_text = doc.get('content', '')
                    if doc_text:
                        doc_embedding = self.embedding_model.encode(doc_text[:500])  # Limit length
                        
                        # Cosine similarity
                        similarity = np.dot(q_embedding, doc_embedding) / (
                            np.linalg.norm(q_embedding) * np.linalg.norm(doc_embedding) + 1e-10
                        )
                        max_similarity = max(max_similarity, similarity)
                
                # Convert similarity to groundedness score
                return float(min(1.0, max_similarity * 1.2))  # Boost slightly
            else:
                # Fallback: just check if we got documents
                return 0.70 if len(retrieved_docs) > 0 else 0.40
                
        except Exception as e:
            print(f"[Groundedness] Error: {e}")
            return 0.40
    
    def _calculate_specificity_math_improved(self, text: str) -> float:
        """Improved specificity using NLP."""
        if self.nlp_model:
            try:
                doc = self.nlp_model(text)
                
                # Named Entity Density
                entities = [ent for ent in doc.ents]
                ned = len(entities) / len(doc) if len(doc) > 0 else 0
                
                # Lexical Density  
                content_words = [token for token in doc if not token.is_stop and token.is_alpha]
                ld = len(content_words) / len(doc) if len(doc) > 0 else 0
                
                # Hedge word penalty
                hedge_words = {"might", "possibly", "usually", "perhaps", "generally", "sometimes"}
                hedge_count = sum(1 for token in doc if token.text.lower() in hedge_words)
                hwp = 1 - (hedge_count / len(doc)) if len(doc) > 0 else 1
                
                # Composite score
                return min(1.0, 0.4 * ned + 0.3 * ld + 0.3 * hwp)
                
            except Exception as e:
                print(f"[Specificity NLP] Error: {e}")
                # Fallback to simple method
                pass
        
        # Simple fallback method
        vague_terms = ["thing", "stuff", "something", "various", "multiple", "some", "many"]
        vague_count = sum(1 for term in vague_terms if term in text.lower())
        return max(0.0, min(1.0, 1.0 - (vague_count * 0.15)))
    
    def _calculate_question_metrics(self, question: str) -> Dict[str, Any]:
        """Calculate quality metrics for generated question with REAL LLM grading."""

        def _clamp01(x: float) -> float:
            return max(0.0, min(1.0, float(x)))

        def _llm_norm_0_1(llm_score_1_5: float) -> float:
            # (sLLM - 1) / 4
            return _clamp01((float(llm_score_1_5) - 1.0) / 4.0)

        def _fuse(stat_0_1: float, llm_1_5: float, lam: float = 0.5) -> float:
            return _clamp01(lam * _clamp01(stat_0_1) + (1.0 - lam) * _llm_norm_0_1(llm_1_5))

        q_lower = (question or "").lower()

        # Statistical (math) scores - IMPROVED
        
        # Coverage: Check topic relevance
        key_terms = ["6sense", "revenue", "ai", "platform", "features", "capabilities", "predictive", "analytics"]
        coverage_math = sum(1 for term in key_terms if term in q_lower) / float(len(key_terms))

        # Specificity: Use improved NLP-based calculation
        specificity_math = self._calculate_specificity_math_improved(question)

        # Insightfulness: Look for depth indicators
        insight_indicators = ["how", "why", "compare", "versus", "implement", "strategy", "best practices", "trade-off", "pitfall"]
        insight_count = sum(1 for indicator in insight_indicators if indicator in q_lower)
        insightfulness_math = _clamp01(0.35 + (insight_count * 0.15))

        # Groundedness: REAL calculation using document retrieval
        groundedness_math = self._calculate_groundedness_math(question)

        # LLM scores - REAL grading with actual API calls
        coverage_llm = self._llm_grade_metric(question, "coverage", "question")
        specificity_llm = self._llm_grade_metric(question, "specificity", "question")
        insightfulness_llm = self._llm_grade_metric(question, "insightfulness", "question")
        groundedness_llm = self._llm_grade_metric(question, "groundedness", "question")

        # Fused finals
        coverage_final = _fuse(coverage_math, coverage_llm)
        specificity_final = _fuse(specificity_math, specificity_llm)
        insightfulness_final = _fuse(insightfulness_math, insightfulness_llm)
        groundedness_final = _fuse(groundedness_math, groundedness_llm)

        overall_score = _clamp01(
            0.25 * coverage_final
            + 0.25 * specificity_final
            + 0.25 * insightfulness_final
            + 0.25 * groundedness_final
        )

        # Recommended thresholds (Marketing FAQs)
        thresholds = {
            "groundedness_min": 0.85,
            "specificity_min": 0.65,
            "insightfulness_min": 0.75,
            "overall_min": 0.80,
        }
        overall_pass = (
            groundedness_final >= thresholds["groundedness_min"]
            and specificity_final >= thresholds["specificity_min"]
            and insightfulness_final >= thresholds["insightfulness_min"]
            and overall_score >= thresholds["overall_min"]
        )

        return {
            "coverage_math": coverage_math,
            "coverage_llm": coverage_llm,
            "coverage_final": coverage_final,
            "specificity_math": specificity_math,
            "specificity_llm": specificity_llm,
            "specificity_final": specificity_final,
            "insightfulness_math": insightfulness_math,
            "insightfulness_llm": insightfulness_llm,
            "insightfulness_final": insightfulness_final,
            "groundedness_math": groundedness_math,
            "groundedness_llm": groundedness_llm,
            "groundedness_final": groundedness_final,
            "overall_score": overall_score,
            "overall_pass": overall_pass,
            "thresholds": thresholds,
            "fusion_lambda": 0.5,
        }
    
    def _calculate_answer_metrics(self, question: str, answer: str, context: str) -> Dict[str, Any]:
        """Calculate quality metrics for generated answer."""
        
        def _clamp01(x: float) -> float:
            return max(0.0, min(1.0, float(x)))
        
        def _llm_norm_0_1(llm_score_1_5: float) -> float:
            return _clamp01((float(llm_score_1_5) - 1.0) / 4.0)
        
        def _fuse(stat_0_1: float, llm_1_5: float, lam: float = 0.5) -> float:
            return _clamp01(lam * _clamp01(stat_0_1) + (1.0 - lam) * _llm_norm_0_1(llm_1_5))
        
        # Statistical metrics for ANSWERS
        
        # Coverage: Does answer address all aspects of question?
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        word_overlap = len(question_words & answer_words) / len(question_words) if question_words else 0
        coverage_math = _clamp01(word_overlap + 0.3)  # Boost base score
        
        # Specificity: Numbers, entities, concrete details
        has_numbers = any(char.isdigit() for char in answer)
        has_bullets = '\n' in answer or '•' in answer or '-' in answer
        answer_length = len(answer.split())
        specificity_math = _clamp01(
            0.4 + 
            (0.2 if has_numbers else 0) +
            (0.2 if has_bullets else 0) +
            (0.2 if answer_length > 50 else 0)
        )
        
        # Insightfulness: Causal language, depth indicators
        insight_markers = ["because", "therefore", "however", "trade-off", "best practice", "recommended", "pitfall"]
        insight_count = sum(1 for marker in insight_markers if marker in answer.lower())
        insightfulness_math = _clamp01(0.35 + (insight_count * 0.15))
        
        # Groundedness: How well does answer match context?
        if context:
            context_words = set(context.lower().split())
            answer_context_overlap = len(answer_words & context_words) / len(answer_words) if answer_words else 0
            groundedness_math = _clamp01(answer_context_overlap * 1.3)
        else:
            groundedness_math = 0.40
        
        # LLM grading for answers - REAL API calls
        coverage_llm = self._llm_grade_metric(answer, "coverage", "answer")
        specificity_llm = self._llm_grade_metric(answer, "specificity", "answer")
        insightfulness_llm = self._llm_grade_metric(answer, "insightfulness", "answer")
        groundedness_llm = self._llm_grade_metric(answer, "groundedness", "answer")
        
        # Fusion
        coverage_final = _fuse(coverage_math, coverage_llm)
        specificity_final = _fuse(specificity_math, specificity_llm)
        insightfulness_final = _fuse(insightfulness_math, insightfulness_llm)
        groundedness_final = _fuse(groundedness_math, groundedness_llm)
        
        overall_score = _clamp01(
            0.25 * coverage_final +
            0.25 * specificity_final +
            0.25 * insightfulness_final +
            0.25 * groundedness_final
        )
        
        # Thresholds for answers (stricter for groundedness)
        thresholds = {
            "groundedness_min": 0.90,  # Stricter for answers
            "specificity_min": 0.65,
            "insightfulness_min": 0.70,
            "overall_min": 0.75
        }
        
        overall_pass = (
            groundedness_final >= thresholds["groundedness_min"] and
            specificity_final >= thresholds["specificity_min"] and
            insightfulness_final >= thresholds["insightfulness_min"] and
            overall_score >= thresholds["overall_min"]
        )
        
        return {
            "coverage_math": coverage_math,
            "coverage_llm": coverage_llm,
            "coverage_final": coverage_final,
            "specificity_math": specificity_math,
            "specificity_llm": specificity_llm,
            "specificity_final": specificity_final,
            "insightfulness_math": insightfulness_math,
            "insightfulness_llm": insightfulness_llm,
            "insightfulness_final": insightfulness_final,
            "groundedness_math": groundedness_math,
            "groundedness_llm": groundedness_llm,
            "groundedness_final": groundedness_final,
            "overall_score": overall_score,
            "overall_pass": overall_pass,
            "thresholds": thresholds,
            "fusion_lambda": 0.5
        }
    
    def _create_question_prompt(self, topic: str, index: int) -> str:
        """Create prompt for question generation."""
        if topic:
            prompts = [
                f"Generate a specific, insightful question about {topic} features and capabilities for 6sense Revenue AI platform.",
                f"Create a question about how {topic} helps companies improve their sales and marketing using 6sense.",
                f"Generate a question about {topic} implementation strategies and best practices for 6sense users.",
                f"Create a comparative question about {topic} versus other solutions in the B2B revenue intelligence space."
            ]
        else:
            prompts = [
                "Generate a specific question about 6sense Revenue AI platform's key features and capabilities.",
                "Create a question about how 6sense helps companies identify and target in-market buyers.",
                "Generate a question about 6sense's predictive analytics and AI-powered targeting capabilities.",
                "Create a question about implementing 6sense effectively for B2B sales and marketing teams."
            ]
        
        return prompts[index % len(prompts)]
    
    def _extract_question_from_response(self, result: Dict, topic: str, index: int) -> str:
        """Extract clean question from RAG response."""
        if isinstance(result, dict) and "answer" in result:
            answer = result["answer"]
            # Extract question-like part from answer
            if "?" in answer:
                # Find the question part
                parts = answer.split("?")
                if len(parts) > 1:
                    question = parts[0] + "?"
                    return question.strip()
            
            # If no clear question, create one based on the content
            if topic:
                return f"What are the key {topic} features of 6sense that help with revenue intelligence?"
            else:
                return f"What are the main capabilities of 6sense Revenue AI platform?"
        
        # Fallback
        return self._create_fallback_question(topic, index)["question"]
    
    def _create_fallback_question(self, topic: str, index: int) -> Dict[str, Any]:
        """Create fallback question when RAG fails."""
        fallback_questions = [
            "What are the key features of 6sense Revenue AI platform?",
            "How does 6sense help companies identify in-market buyers?",
            "What predictive analytics capabilities does 6sense offer?",
            "How can companies implement 6sense effectively for B2B sales?",
            "What industries benefit most from 6sense's revenue intelligence?"
        ]
        
        if topic:
            fallback_questions = [
                f"What are the key {topic} features of 6sense?",
                f"How does {topic} help improve B2B sales and marketing?",
                f"What are the best practices for implementing {topic} with 6sense?",
                f"How does {topic} compare to other revenue intelligence solutions?"
            ]
        
        question = fallback_questions[index % len(fallback_questions)]
        
        return {
            "question": question,
            "answer": "",
            "context_source": "Fallback Template",
            "chunk_id": f"fallback_{index}",
            "reasoning": f"Generated using fallback template for topic: {topic or '6sense'}",
            "metrics": self._calculate_question_metrics(question),
            "answer_metrics": {},
            "retrieved_sources": 0
        }
    
    def _fallback_questions(self, topic: str, num_questions: int) -> List[Dict[str, Any]]:
        """Generate fallback questions when RAG is not available."""
        questions = []
        for i in range(num_questions):
            questions.append(self._create_fallback_question(topic, i))
        return questions

def generate_data_driven_questions(topic: str = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Main function to generate questions using RAG graph."""
    generator = DataDrivenQuestionGenerator()
    return generator.generate_question_from_data(topic, num_questions)

# Export for use in other modules
__all__ = ['generate_data_driven_questions', 'DataDrivenQuestionGenerator']