#!/usr/bin/env python3

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from rag_graph import create_persistent_rag_graph, run_rag_query

class NudgeEvalResult(BaseModel):
    """Schema for granular nudge evaluation."""
    coverage: Literal["yes", "no"] = Field(description="Does the question cover product capabilities?")
    specific: Literal["yes", "no"] = Field(description="Is the question specific rather than generic?")
    insightful: Literal["yes", "no"] = Field(description="Does the question provide a helpful insight to the user?")
    grounded: Literal["yes", "no"] = Field(description="Is the question grounded in the provided data context?")
    reasoning: str = Field(description="Brief explanation for these scores.")

class EvalResult(BaseModel):
    """Schema for LLM-as-a-judge grading."""
    relevance_score: float = Field(description="Score from 0-1 on how relevant question is to product capabilities.")
    safety_pass: bool = Field(description="Whether the question is safe and appropriate.")
    specificity_score: float = Field(description="Score from 0-1 on how specific question is.")
    reasoning: str = Field(description="Brief explanation of the grade.")

class QuestionSet(BaseModel):
    """Schema for bulk question generation."""
    questions: List[str] = Field(description="List of product questions.")

class GraphState(BaseModel):
    """The state of our LangGraph workflow."""
    context: str = Field(default="")
    target_count: int = Field(default=100)
    generated_questions: List[str] = Field(default_factory=list)
    final_evals: List[Dict] = Field(default_factory=list)
    iterations: int = Field(default=0)
    product: str = Field(default="6sense")

class EnhancedQuestionGenerator:
    def __init__(self):
        self.rag_graph = None
        self.initialize_rag()
    
    def initialize_rag(self):
        """Initialize the RAG graph for context generation."""
        try:
            self.rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
            print("✅ RAG graph initialized for question generation")
        except Exception as e:
            print(f"❌ Error initializing RAG: {e}")
    
    def generate_context(self, product: str) -> str:
        """Generate comprehensive context using RAG."""
        if not self.rag_graph:
            return "No RAG context available."
        
        try:
            context_query = f"""
            Provide comprehensive product information for {product} including:
            - Core features and capabilities
            - Target industries and use cases
            - Implementation requirements and timeline
            - Pricing models and ROI expectations
            - Competitive advantages and unique selling points
            - Customer success stories and case studies
            - Technical specifications and integrations
            - Common challenges and solutions
            """
            
            result = run_rag_query(self.rag_graph, context_query)
            return result.get("answer", "")
        except Exception as e:
            print(f"❌ Error generating context: {e}")
            return ""
    
    def generate_questions_node(self, state: GraphState) -> Dict[str, Any]:
        """Node to generate initial product questions."""
        if not self.rag_graph:
            return {"generated_questions": [], "iterations": 1}
        
        try:
            # Import LLM for question generation
            from langchain_openai import ChatOpenAI
            from langchain_core.output_parsers import JsonOutputParser
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)
            parser = JsonOutputParser(pydantic_object=QuestionSet)
            
            prompt = ChatPromptTemplate.from_template(
                "You are a helpful shopping assistant like Amazon Rufus.\n"
                "Product Context: {context}\n"
                "Generate {count} unique questions a customer might ask.\n"
                "Questions should be:\n"
                "- Specific and detailed\n"
                "- Insightful and helpful\n"
                "- Grounded in the provided context\n"
                "- Cover different aspects (features, pricing, implementation, ROI, etc.)\n"
                "- Varied in complexity and type\n\n"
                "{format_instructions}"
            )
            
            chain = prompt | llm | parser
            result = chain.invoke({
                "context": state.context,
                "count": state.target_count,
                "format_instructions": parser.get_format_instructions()
            })
            
            return {"generated_questions": result["questions"], "iterations": 1}
            
        except Exception as e:
            print(f"❌ Error generating questions: {e}")
            return {"generated_questions": [], "iterations": 1}
    
    def evaluate_questions_node(self, state: GraphState) -> Dict[str, Any]:
        """Grades questions using RAGAS-style evaluation logic."""
        if not self.rag_graph:
            return {"final_evals": []}
        
        try:
            # Import LLM for evaluation
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            
            # Identify the latest batch of questions
            new_questions = state.generated_questions[-state.target_count:]
            valid_evals = []
            
            # Multi-dimensional evaluation prompt
            eval_prompt = ChatPromptTemplate.from_template(
                "Evaluate the following question based on the provided data context.\n\n"
                "Data Context: {context}\n"
                "Question: {question}\n\n"
                "Scoring Criteria:\n"
                "1. Coverage: Does the question cover product capabilities?\n"
                "2. Specificity: Is it a detailed query rather than a 'tell me more' style?\n"
                "3. Insightfulness: Would the answer help a user make a decision?\n"
                "4. Groundedness: Is the question logic supported by data context?\n\n"
                "Provide scores for each criterion and brief reasoning."
            )
            
            for q in new_questions:
                try:
                    # Run evaluation
                    grade = llm.invoke(eval_prompt.format(context=state.context, question=q))
                    
                    # Parse the response (simplified parsing)
                    eval_text = str(grade.content) if hasattr(grade, 'content') else str(grade)
                    
                    # Create evaluation result
                    res_dict = {
                        "question": q,
                        "coverage": "yes" if "cover" in eval_text.lower() and "yes" in eval_text.lower() else "no",
                        "specific": "yes" if "specific" in eval_text.lower() and "yes" in eval_text.lower() else "no",
                        "insightful": "yes" if "insight" in eval_text.lower() and "yes" in eval_text.lower() else "no",
                        "grounded": "yes" if "ground" in eval_text.lower() and "yes" in eval_text.lower() else "no",
                        "reasoning": eval_text,
                        "overall_pass": False
                    }
                    
                    # A question 'passes' if it is 'yes' across key dimensions
                    res_dict["overall_pass"] = all(res_dict[k] == "yes" for k in ["coverage", "specific", "insightful", "grounded"])
                    
                    valid_evals.append(res_dict)
                    
                except Exception as e:
                    print(f"❌ Error evaluating question: {e}")
                    continue
            
            return {"final_evals": valid_evals}
            
        except Exception as e:
            print(f"❌ Error in evaluation node: {e}")
            return {"final_evals": []}
    
    def decide_to_continue(self, state: GraphState) -> str:
        """Checks if we have enough high-quality questions."""
        passed_count = sum(1 for e in state.final_evals if e.get("overall_pass", False))
        
        # Continue if we haven't met the target or iteration limit
        if passed_count >= state.target_count or state.iterations >= 3:
            return "end"
        return "generate"
    
    def generate_questions_with_metrics(self, product: str = "6sense", target_count: int = 100) -> Dict[str, Any]:
        """Generate questions with RAGAS-style evaluation metrics."""
        print(f"🚀 Generating {target_count} questions for {product} with RAGAS evaluation...")
        
        # Initialize state
        state = GraphState(
            context=self.generate_context(product),
            target_count=target_count,
            generated_questions=[],
            final_evals=[],
            iterations=0,
            product=product
        )
        
        # Run the workflow
        max_iterations = 3
        for iteration in range(max_iterations):
            print(f"📊 Iteration {iteration + 1}: Generating questions...")
            
            # Generate questions
            gen_result = self.generate_questions_node(state)
            state.generated_questions.extend(gen_result["generated_questions"])
            state.iterations += 1
            
            # Evaluate questions
            print(f"🔍 Evaluating {len(gen_result['generated_questions'])} questions...")
            eval_result = self.evaluate_questions_node(state)
            state.final_evals.extend(eval_result["final_evals"])
            
            # Check if we should continue
            passed_count = sum(1 for e in state.final_evals if e.get("overall_pass", False))
            print(f"✅ Passed: {passed_count}/{target_count} questions")
            
            if passed_count >= target_count:
                break
        
        print(f"🎉 Generated {len(state.final_evals)} evaluated questions")
        return {
            "questions": state.final_evals,
            "total_generated": len(state.generated_questions),
            "total_passed": len(state.final_evals),
            "iterations": state.iterations,
            "product": product
        }
    
    def create_analytics_dashboard(self, evaluation_results: List[Dict]) -> Dict[str, Any]:
        """Create analytics dashboard from evaluation results."""
        if not evaluation_results:
            return {}
        
        # Calculate metrics
        total_questions = len(evaluation_results)
        passed_questions = sum(1 for e in evaluation_results if e.get("overall_pass", False))
        
        # Dimension-specific metrics
        coverage_pass = sum(1 for e in evaluation_results if e.get("coverage", "no") == "yes")
        specific_pass = sum(1 for e in evaluation_results if e.get("specific", "no") == "yes")
        insightful_pass = sum(1 for e in evaluation_results if e.get("insightful", "no") == "yes")
        grounded_pass = sum(1 for e in evaluation_results if e.get("grounded", "no") == "yes")
        
        # Calculate percentages
        metrics = {
            "total_questions": total_questions,
            "passed_questions": passed_questions,
            "pass_rate": (passed_questions / total_questions * 100) if total_questions > 0 else 0,
            "coverage_rate": (coverage_pass / total_questions * 100) if total_questions > 0 else 0,
            "specificity_rate": (specific_pass / total_questions * 100) if total_questions > 0 else 0,
            "insightfulness_rate": (insightful_pass / total_questions * 100) if total_questions > 0 else 0,
            "groundedness_rate": (grounded_pass / total_questions * 100) if total_questions > 0 else 0,
        }
        
        return metrics
    
    def create_questions_dataframe(self, evaluation_results: List[Dict]) -> pd.DataFrame:
        """Create pandas DataFrame from evaluation results."""
        if not evaluation_results:
            return pd.DataFrame()
        
        # Prepare data for DataFrame
        data = []
        for i, result in enumerate(evaluation_results, 1):
            data.append({
                "ID": i,
                "Question": result.get("question", ""),
                "Coverage": result.get("coverage", "no"),
                "Specific": result.get("specific", "no"),
                "Insightful": result.get("insightful", "no"),
                "Grounded": result.get("grounded", "no"),
                "Overall Pass": "✅" if result.get("overall_pass", False) else "❌",
                "Reasoning": result.get("reasoning", "")
            })
        
        return pd.DataFrame(data)
    
    def create_visualizations(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualizations for question analytics."""
        visualizations = {}
        
        # RAGAS Metrics Radar Chart
        if metrics:
            radar_data = {
                "Metric": ["Coverage", "Specificity", "Insightfulness", "Groundedness"],
                "Score": [
                    metrics.get("coverage_rate", 0),
                    metrics.get("specificity_rate", 0),
                    metrics.get("insightfulness_rate", 0),
                    metrics.get("groundedness_rate", 0)
                ]
            }
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_data["Score"],
                theta=radar_data["Metric"],
                fill='toself',
                name='RAGAS Metrics'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title="RAGAS Evaluation Metrics"
            )
            visualizations["radar_chart"] = fig_radar
            
            # Pass/Fail Distribution
            pass_fail_data = {
                "Status": ["Passed", "Failed"],
                "Count": [
                    metrics.get("passed_questions", 0),
                    metrics.get("total_questions", 0) - metrics.get("passed_questions", 0)
                ]
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=pass_fail_data["Status"],
                values=pass_fail_data["Count"],
                hole=0.3
            )])
            fig_pie.update_layout(title="Question Quality Distribution")
            visualizations["pie_chart"] = fig_pie
        
        return visualizations

# Main function for testing
def main():
    """Test the enhanced question generator."""
    generator = EnhancedQuestionGenerator()
    
    # Generate questions for 6sense
    results = generator.generate_questions_with_metrics("6sense", 100)
    
    # Create analytics
    metrics = generator.create_analytics_dashboard(results["questions"])
    
    # Create DataFrame
    df = generator.create_questions_dataframe(results["questions"])
    
    # Create visualizations
    visualizations = generator.create_visualizations(metrics)
    
    print("🎉 Enhanced Question Generation Complete!")
    print(f"📊 Total Questions: {metrics.get('total_questions', 0)}")
    print(f"✅ Passed Questions: {metrics.get('passed_questions', 0)}")
    print(f"📈 Pass Rate: {metrics.get('pass_rate', 0):.1f}%")
    
    return {
        "results": results,
        "metrics": metrics,
        "dataframe": df,
        "visualizations": visualizations
    }

if __name__ == "__main__":
    main()
