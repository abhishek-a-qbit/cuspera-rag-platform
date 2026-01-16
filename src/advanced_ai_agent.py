"""
Advanced AI Agent with LangGraph
State management, chat memory, and dynamic capabilities
Enhanced with analytics, ROI calculator, and report generation
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional, TypedDict
from datetime import datetime, timedelta
import io
import base64

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from langgraph.graph import StateGraph, END
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_core.prompts import ChatPromptTemplate
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    print("Warning: LangGraph not available: " + str(e))
    LANGGRAPH_AVAILABLE = False

# Import existing RAG components
try:
    from rag_graph import create_persistent_rag_graph, run_rag_query
    RAG_AVAILABLE = True
except ImportError as e:
    print("Warning: RAG system not available: " + str(e))
    RAG_AVAILABLE = False

class AgentState(TypedDict):
    """State for the AI Agent with LangGraph"""
    messages: List[Any]  # Conversation history
    user_query: str
    retrieved_docs: List[Dict]
    generated_response: str
    metrics: Dict[str, Any]
    tools_used: List[str]
    navigation_intent: Optional[str]
    code_execution: Optional[Dict]
    context_data: Dict[str, Any]
    analytics_data: Optional[Dict]  # Analytics results
    roi_calculation: Optional[Dict]  # ROI calculation results
    report_data: Optional[Dict]  # Report generation data
    chart_data: Optional[Dict]  # Chart/visualization data

class AdvancedAIAgent:
    """Advanced AI Agent with LangGraph state management"""
    
    def __init__(self):
        """Initialize the advanced AI agent"""
        self.rag_graph = None
        self.state_graph = None
        self.chat_memory = {}  # Simple in-memory chat history
        
        if not LANGGRAPH_AVAILABLE:
            print("[Agent] LangGraph not available, falling back to basic mode")
            return
        
        # Initialize RAG graph
        if RAG_AVAILABLE:
            try:
                self.rag_graph = create_persistent_rag_graph(use_persistent=True, force_reprocess=False)
                print("[Agent] Initialized RAG graph")
            except Exception as e:
                print("[Agent] Error initializing RAG graph: " + str(e))
        
        # Build LangGraph
        self._build_state_graph()
    
    def _build_state_graph(self):
        """Build the LangGraph with state management"""
        if not LANGGRAPH_AVAILABLE:
            return
        
        # Create state graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("intent_detection", self._detect_intent)
        workflow.add_node("rag_retrieval", self._rag_retrieval)
        workflow.add_node("response_generation", self._generate_response)
        workflow.add_node("code_execution", self._execute_code)
        workflow.add_node("metrics_calculation", self._calculate_metrics)
        
        # Add edges
        workflow.set_entry_point("intent_detection")
        workflow.add_conditional_edges(
            "intent_detection",
            self._route_by_intent,
            {
                "rag": "rag_retrieval",
                "code": "code_execution",
                "navigation": END,
                "chat": "response_generation"
            }
        )
        workflow.add_edge("rag_retrieval", "response_generation")
        workflow.add_edge("response_generation", "metrics_calculation")
        workflow.add_edge("code_execution", "metrics_calculation")
        workflow.add_edge("metrics_calculation", END)
        
        # Compile without memory for now
        self.state_graph = workflow.compile()
        print("[Agent] Built state graph")
    
    def _detect_intent(self, state: AgentState) -> AgentState:
        """Detect user intent and route appropriately"""
        user_query = state["user_query"]
        
        # Intent detection logic
        query_lower = user_query.lower()
        
        # Navigation intents
        if any(word in query_lower for word in ["analytics", "report", "question generator", "status"]):
            if "analytics" in query_lower:
                state["navigation_intent"] = "analytics"
            elif "report" in query_lower:
                state["navigation_intent"] = "report"
            elif "question generator" in query_lower:
                state["navigation_intent"] = "question_generator"
            elif "status" in query_lower:
                state["navigation_intent"] = "status"
            return state
        
        # Code execution intents
        if any(word in query_lower for word in ["generate", "create", "build", "code", "python", "dashboard", "chart", "visualization"]):
            state["code_execution"] = {"type": "dynamic", "query": user_query}
            return state
        
        # Default to RAG chat
        state["navigation_intent"] = None
        return state
    
    def _route_by_intent(self, state: AgentState) -> str:
        """Route to appropriate node based on intent"""
        if state.get("navigation_intent"):
            return "navigation"
        elif state.get("code_execution"):
            return "code"
        else:
            return "rag"
    
    def _rag_retrieval(self, state: AgentState) -> AgentState:
        """Retrieve documents using RAG"""
        if not self.rag_graph:
            state["retrieved_docs"] = []
            return state
        
        try:
            result = run_rag_query(self.rag_graph, state["user_query"])
            state["retrieved_docs"] = result.get("retrieved_docs", [])
            state["context_data"] = result
        except Exception as e:
            print("[Agent] RAG retrieval error: " + str(e))
            state["retrieved_docs"] = []
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """Generate response using LLM with context"""
        if not self.rag_graph or not self.rag_graph.llm:
            state["generated_response"] = "I'm sorry, I'm not available right now."
            return state
        
        try:
            # Build context from retrieved docs
            context = "\n".join([doc.get("content", "")[:500] for doc in state["retrieved_docs"]])
            
            # Enhanced prompt with context
            prompt = f"""You are a helpful AI assistant. Answer the user's question based on the provided context.

Context:
{context}

User Question: {state["user_query"]}

Provide a comprehensive answer with:
1. Clear explanation
2. Supporting details from context
3. Relevant insights

Answer:"""
            
            response = self.rag_graph.llm.invoke(prompt)
            state["generated_response"] = response.content
            state["tools_used"] = ["rag_retrieval", "llm_generation"]
            
        except Exception as e:
            print("[Agent] Response generation error: " + str(e))
            state["generated_response"] = "I encountered an error generating a response."
        
        return state
    
    def _execute_code(self, state: AgentState) -> AgentState:
        """Execute dynamic code for visualizations"""
        code_query = state["code_execution"]["query"]
        
        # This is a placeholder for code execution
        # In production, you'd want a secure sandbox
        state["generated_response"] = f"I would generate code for: {code_query}"
        state["tools_used"] = ["code_execution"]
        
        return state
    
    def _calculate_metrics(self, state: AgentState) -> AgentState:
        """Calculate response metrics"""
        # Import metrics calculation from existing system
        try:
            from data_driven_question_generator import DataDrivenQuestionGenerator
            generator = DataDrivenQuestionGenerator()
            
            # Calculate metrics for the response
            response_metrics = generator._calculate_answer_metrics(
                state["user_query"], 
                state["generated_response"], 
                "\n".join([doc.get("content", "") for doc in state["retrieved_docs"]])
            )
            
            state["metrics"] = response_metrics
            
        except Exception as e:
            print("[Agent] Metrics calculation error: " + str(e))
            state["metrics"] = {}
        
        return state
    
    def chat(self, user_query: str, session_id: str = "default") -> Dict[str, Any]:
        """Main chat interface using existing RAG system"""
        try:
            # Initialize variables
            sources = []
            response = ""
            metrics = {}
            navigation_intent = None
            code_execution = None
            tools_used = []
            
            # Store in simple memory with context
            if session_id not in self.chat_memory:
                self.chat_memory[session_id] = []
            
            # Add user message to memory
            self.chat_memory[session_id].append({
                "type": "user",
                "message": user_query,
                "timestamp": datetime.now()
            })
            
            # Get recent conversation context
            recent_messages = self.chat_memory[session_id][-5:]  # Last 5 messages
            conversation_context = "\n".join([
                f"{'User' if msg['type'] == 'user' else 'Agent'}: {msg['message']}" 
                for msg in recent_messages
            ])
            
            # Detect intent for navigation and code generation
            query_lower = user_query.lower()
            navigation_intent = None
            code_execution = None
            tools_used = []
            
            # Code generation and visualization intents - CHECK FIRST
            # Check for specific command patterns first
            if (query_lower.startswith(("calculate roi", "roi calculation", "return on investment", "investment returns")) or
                "calculate roi" in query_lower or "roi calculation" in query_lower):
                # Calculate ROI
                roi_data = self._calculate_roi(user_query)
                response = f"""💰 **ROI Analysis Complete**

**Investment:**
- Platform Cost: ${roi_data['investment']['platform_cost']:,}
- Implementation Cost: ${roi_data['investment']['implementation_cost']:,}
- Training Cost: ${roi_data['investment']['training_cost']:,}
- **Total Investment: ${roi_data['investment']['total_investment']:,}**

**Returns (12 months):**
- Revenue Increase: ${roi_data['returns']['revenue_increase']:,}
- Cost Savings: ${roi_data['returns']['cost_savings']:,}
- Productivity Gain: ${roi_data['returns']['productivity_gain']:,}
- **Total Returns: ${roi_data['returns']['total_returns']:,}**

**ROI Metrics:**
- **ROI: {roi_data['roi_metrics']['roi_percentage']:.1f}%**
- Payback Period: {roi_data['roi_metrics']['payback_period_months']} months
- Net Present Value: ${roi_data['roi_metrics']['npv']:,}
- Internal Rate of Return: {roi_data['roi_metrics']['irr']:.1f}%

**Breakdown by Function:**
- Marketing ROI: {roi_data['breakdown']['marketing_roi']:.1f}%
- Sales ROI: {roi_data['breakdown']['sales_roi']:.1f}%
- Overall ROI: {roi_data['breakdown']['overall_roi']:.1f}%"""
                
                tools_used = ["roi_calculation"]
                metrics = {"overall_score": 0.9}
                sources = []
                
            elif (query_lower.startswith(("generate analytics", "analytics report", "create analytics")) or
                  "generate analytics" in query_lower or "analytics report" in query_lower):
                # Generate analytics report
                analytics_data = self._generate_analytics_report(user_query)
                response = f"""📊 **Analytics Report Generated**

**Key Metrics:**
- Total Revenue: ${analytics_data['metrics']['total_revenue']:,.0f}
- Conversion Rate: {analytics_data['metrics']['conversion_rate']:.1%}
- Lead Quality Score: {analytics_data['metrics']['lead_quality_score']:.1f}/10
- Pipeline Velocity: {analytics_data['metrics']['pipeline_velocity']:.0f} days
- Win Rate: {analytics_data['metrics']['win_rate']:.1%}

**Trends:**
- Revenue Growth: {analytics_data['trends']['revenue_growth']:.1%}
- Lead Volume: {analytics_data['trends']['lead_volume_trend']}
- Engagement Rate: {analytics_data['trends']['engagement_rate']:.1%}

**Key Insights:**
{chr(10).join(f"• {insight}" for insight in analytics_data['insights'])}

**Recommendations:**
{chr(10).join(f"• {rec}" for rec in analytics_data['recommendations'])}"""
                
                tools_used = ["analytics_generation"]
                metrics = {"overall_score": 0.9}
                sources = []
                
            elif any(word in query_lower for word in ["generate", "create", "make", "build", "code", "visualization", "infographic", "dashboard", "chart", "graph", "plot"]):
                if "analytics" in query_lower or "report" in query_lower:
                    # Generate analytics report
                    analytics_data = self._generate_analytics_report(user_query)
                    response = f"""📊 **Analytics Report Generated**

**Key Metrics:**
- Total Revenue: ${analytics_data['metrics']['total_revenue']:,.0f}
- Conversion Rate: {analytics_data['metrics']['conversion_rate']:.1%}
- Lead Quality Score: {analytics_data['metrics']['lead_quality_score']:.1f}/10
- Pipeline Velocity: {analytics_data['metrics']['pipeline_velocity']:.0f} days
- Win Rate: {analytics_data['metrics']['win_rate']:.1%}

**Trends:**
- Revenue Growth: {analytics_data['trends']['revenue_growth']:.1%}
- Lead Volume: {analytics_data['trends']['lead_volume_trend']}
- Engagement Rate: {analytics_data['trends']['engagement_rate']:.1%}

**Key Insights:**
{chr(10).join(f"• {insight}" for insight in analytics_data['insights'])}

**Recommendations:**
{chr(10).join(f"• {rec}" for rec in analytics_data['recommendations'])}"""
                    
                    tools_used = ["analytics_generation"]
                    metrics = {"overall_score": 0.9}
                    sources = []
                    
                elif "roi" in query_lower or "return on investment" in query_lower or "investment" in query_lower or "returns" in query_lower:
                    # Calculate ROI
                    roi_data = self._calculate_roi(user_query)
                    response = f"""💰 **ROI Analysis Complete**

**Investment:**
- Platform Cost: ${roi_data['investment']['platform_cost']:,}
- Implementation Cost: ${roi_data['investment']['implementation_cost']:,}
- Training Cost: ${roi_data['investment']['training_cost']:,}
- **Total Investment: ${roi_data['investment']['total_investment']:,}**

**Returns (12 months):**
- Revenue Increase: ${roi_data['returns']['revenue_increase']:,}
- Cost Savings: ${roi_data['returns']['cost_savings']:,}
- Productivity Gain: ${roi_data['returns']['productivity_gain']:,}
- **Total Returns: ${roi_data['returns']['total_returns']:,}**

**ROI Metrics:**
- **ROI: {roi_data['roi_metrics']['roi_percentage']:.1f}%**
- Payback Period: {roi_data['roi_metrics']['payback_period_months']} months
- Net Present Value: ${roi_data['roi_metrics']['npv']:,}
- Internal Rate of Return: {roi_data['roi_metrics']['irr']:.1f}%

**Breakdown by Function:**
- Marketing ROI: {roi_data['breakdown']['marketing_roi']:.1f}%
- Sales ROI: {roi_data['breakdown']['sales_roi']:.1f}%
- Overall ROI: {roi_data['breakdown']['overall_roi']:.1f}%"""
                    
                    tools_used = ["roi_calculation"]
                    metrics = {"overall_score": 0.9}
                    sources = []
                    
                elif "infographic" in query_lower or "visualization" in query_lower:
                    # Generate infographic data
                    infographic_data = self._generate_infographic_data(user_query)
                    response = f"""🎨 **Infographic Data Generated**

**Title: {infographic_data['title']}**

**Key Statistics:**
{chr(10).join(f"{stat['icon']} {stat['label']}: {stat['value']}" for stat in infographic_data['key_statistics'])}

**Visual Elements:**
- Progress bars for target achievement, pipeline health, and team adoption
- Pie chart showing revenue sources breakdown
- Modern business infographic design with professional color scheme

**Design Specifications:**
- Color Scheme: {', '.join(infographic_data['design_elements']['color_scheme'])}
- Layout: {infographic_data['design_elements']['layout']}
- Style: {infographic_data['design_elements']['style']}

Ready to create stunning visual content for your presentations!"""
                    
                    tools_used = ["infographic_generation"]
                    metrics = {"overall_score": 0.85}
                    sources = []
                    
                elif "dashboard" in query_lower:
                    code_execution = {
                        "type": "dashboard", 
                        "query": user_query,
                        "description": "Create interactive dashboard"
                    }
                    response = self._generate_dashboard_code(user_query)
                    tools_used = ["dashboard_generation"]
                    metrics = {"overall_score": 0.8}
                    sources = []
                    
                elif "chart" in query_lower or "graph" in query_lower or "plot" in query_lower:
                    code_execution = {
                        "type": "chart",
                        "query": user_query, 
                        "description": "Generate chart or graph"
                    }
                    response = self._generate_code_visualization(code_execution, [])
                    tools_used = ["chart_generation"]
                    metrics = {"overall_score": 0.8}
                    sources = []
                    
                else:
                    code_execution = {
                        "type": "general",
                        "query": user_query,
                        "description": "Generate code or analysis"
                    }
                    response = self._generate_code_visualization(code_execution, [])
                    tools_used = ["code_generation"]
                    metrics = {"overall_score": 0.75}
                    sources = []
            
            # Check if user is asking about previous context
            elif any(word in query_lower for word in ["previous", "what was", "my last", "earlier", "before", "context", "dont"]):
                # Provide context from recent messages
                if len(recent_messages) > 1:
                    # Find the last actual user question
                    last_user_questions = [
                        msg["message"] for msg in reversed(recent_messages) 
                        if msg["type"] == "user" and msg["message"] != user_query
                    ]
                    
                    if last_user_questions:
                        last_question = last_user_questions[0]
                        response = f"Your previous question was: \"{last_question}\"\n\nBased on our conversation history, we've been discussing:\n"
                        
                        # Add context from recent conversation
                        topics_discussed = []
                        for msg in recent_messages[-5:]:
                            if msg["type"] == "user":
                                topics_discussed.append(f"• {msg['message']}")
                        
                        if topics_discussed:
                            response += "\n".join(topics_discussed[-3:])  # Last 3 topics
                            response += f"\n\nHow can I help you continue this analysis or explore a different aspect?"
                        else:
                            response += f"\n\nWe've been discussing 6sense's capabilities. What would you like to explore next?"
                        
                        tools_used = ["context_retrieval"]
                        metrics = {
                            "coverage_final": 0.9,
                            "specificity_final": 0.8,
                            "insightfulness_final": 0.7,
                            "groundedness_final": 0.8,
                            "overall_score": 0.8
                        }
                        sources = []  # Initialize sources for context response
                    else:
                        response = "This appears to be the start of our conversation. We've been discussing 6sense's Revenue AI platform and its capabilities. What specific aspect would you like to explore?"
                        tools_used = ["context_init"]
                        metrics = {
                            "coverage_final": 0.7,
                            "specificity_final": 0.6,
                            "insightfulness_final": 0.5,
                            "groundedness_final": 0.7,
                            "overall_score": 0.6
                        }
                        sources = []  # Initialize sources for context init response
            
            # Code generation and visualization intents
            elif any(word in query_lower for word in ["generate", "create", "make", "build", "code", "visualization", "infographic", "dashboard", "chart", "graph", "plot"]):
                if "analytics" in query_lower or "report" in query_lower:
                    # Generate analytics report
                    analytics_data = self._generate_analytics_report(user_query)
                    response = f"""📊 **Analytics Report Generated**

**Key Metrics:**
- Total Revenue: ${analytics_data['metrics']['total_revenue']:,.0f}
- Conversion Rate: {analytics_data['metrics']['conversion_rate']:.1%}
- Lead Quality Score: {analytics_data['metrics']['lead_quality_score']:.1f}/10
- Pipeline Velocity: {analytics_data['metrics']['pipeline_velocity']:.0f} days
- Win Rate: {analytics_data['metrics']['win_rate']:.1%}

**Trends:**
- Revenue Growth: {analytics_data['trends']['revenue_growth']:.1%}
- Lead Volume: {analytics_data['trends']['lead_volume_trend']}
- Engagement Rate: {analytics_data['trends']['engagement_rate']:.1%}

**Key Insights:**
{chr(10).join(f"• {insight}" for insight in analytics_data['insights'])}

**Recommendations:**
{chr(10).join(f"• {rec}" for rec in analytics_data['recommendations'])}"""
                    
                    tools_used = ["analytics_generation"]
                    metrics = {"overall_score": 0.9}
                    sources = []
                    
                elif "roi" in query_lower or "return on investment" in query_lower or "investment" in query_lower or "returns" in query_lower:
                    # Calculate ROI
                    roi_data = self._calculate_roi(user_query)
                    response = f"""💰 **ROI Analysis Complete**

**Investment:**
- Platform Cost: ${roi_data['investment']['platform_cost']:,}
- Implementation Cost: ${roi_data['investment']['implementation_cost']:,}
- Training Cost: ${roi_data['investment']['training_cost']:,}
- **Total Investment: ${roi_data['investment']['total_investment']:,}**

**Returns (12 months):**
- Revenue Increase: ${roi_data['returns']['revenue_increase']:,}
- Cost Savings: ${roi_data['returns']['cost_savings']:,}
- Productivity Gain: ${roi_data['returns']['productivity_gain']:,}
- **Total Returns: ${roi_data['returns']['total_returns']:,}**

**ROI Metrics:**
- **ROI: {roi_data['roi_metrics']['roi_percentage']:.1f}%**
- Payback Period: {roi_data['roi_metrics']['payback_period_months']} months
- Net Present Value: ${roi_data['roi_metrics']['npv']:,}
- Internal Rate of Return: {roi_data['roi_metrics']['irr']:.1f}%

**Breakdown by Function:**
- Marketing ROI: {roi_data['breakdown']['marketing_roi']:.1f}%
- Sales ROI: {roi_data['breakdown']['sales_roi']:.1f}%
- Overall ROI: {roi_data['breakdown']['overall_roi']:.1f}%"""
                    
                    tools_used = ["roi_calculation"]
                    metrics = {"overall_score": 0.9}
                    sources = []
                    
                elif "infographic" in query_lower or "visualization" in query_lower:
                    # Generate infographic data
                    infographic_data = self._generate_infographic_data(user_query)
                    response = f"""🎨 **Infographic Data Generated**

**Title: {infographic_data['title']}**

**Key Statistics:**
{chr(10).join(f"{stat['icon']} {stat['label']}: {stat['value']}" for stat in infographic_data['key_statistics'])}

**Visual Elements:**
- Progress bars for target achievement, pipeline health, and team adoption
- Pie chart showing revenue sources breakdown
- Modern business infographic design with professional color scheme

**Design Specifications:**
- Color Scheme: {', '.join(infographic_data['design_elements']['color_scheme'])}
- Layout: {infographic_data['design_elements']['layout']}
- Style: {infographic_data['design_elements']['style']}

Ready to create stunning visual content for your presentations!"""
                    
                    tools_used = ["infographic_generation"]
                    metrics = {"overall_score": 0.85}
                    sources = []
                    
                elif "dashboard" in query_lower:
                    code_execution = {
                        "type": "dashboard", 
                        "query": user_query,
                        "description": "Create interactive dashboard"
                    }
                    response = self._generate_dashboard_code(user_query)
                    tools_used = ["dashboard_generation"]
                    metrics = {"overall_score": 0.8}
                    sources = []
                    
                elif "chart" in query_lower or "graph" in query_lower or "plot" in query_lower:
                    code_execution = {
                        "type": "chart",
                        "query": user_query, 
                        "description": "Generate chart or graph"
                    }
                    response = self._generate_code_visualization(code_execution, [])
                    tools_used = ["chart_generation"]
                    metrics = {"overall_score": 0.8}
                    sources = []
                    
                else:
                    code_execution = {
                        "type": "general",
                        "query": user_query,
                        "description": "Generate code or analysis"
                    }
                    response = self._generate_code_visualization(code_execution, [])
                    tools_used = ["code_generation"]
                    metrics = {"overall_score": 0.75}
                    sources = []
            
            # Generate code/visualization if requested
            elif code_execution:
                response = self._generate_code_visualization(code_execution, [])
                tools_used.append("code_generation")
                metrics = {
                    "coverage_final": 0.8,
                    "specificity_final": 0.9,
                    "insightfulness_final": 0.8,
                    "groundedness_final": 0.7,
                    "overall_score": 0.8
                }
                sources = []  # Initialize sources for code generation
            else:
                # Navigation intents
                if "analytics" in query_lower or "dashboard" in query_lower:
                    navigation_intent = "analytics"
                elif "report" in query_lower:
                    navigation_intent = "reports"
                elif "question" in query_lower or "generate" in query_lower:
                    navigation_intent = "question_generator"
                
                # Use existing RAG system directly
                if RAG_AVAILABLE and self.rag_graph:
                    from rag_graph import run_rag_query
                    
                    # Run RAG query
                    result = run_rag_query(
                        self.rag_graph,
                        user_query,
                        mode="answer",
                        style="default"
                    )
                    
                    # Debug: Print what we got from RAG
                    print(f"[DEBUG] RAG result keys: {result.keys()}")
                    print(f"[DEBUG] Retrieved docs: {len(result.get('retrieved_docs', []))}")
                    
                    # Extract response and sources
                    response = result.get("answer", "I'm having trouble processing your question.")
                    sources = result.get("retrieved_docs", [])
                    print(f"[DEBUG] Sources extracted: {len(sources)}")
                    tools_used.append("rag_query")
                    
                    # Calculate basic metrics
                    metrics = {
                        "coverage_final": min(0.9, len(sources) / 5.0),  # More sources = better coverage
                        "specificity_final": 0.7,  # Default specificity
                        "insightfulness_final": 0.6,  # Default insightfulness  
                        "groundedness_final": 0.8,  # High groundedness since we use RAG
                        "overall_score": 0.7
                    }
                else:
                    # Fallback response
                    response = "I'm sorry, RAG system is not available right now. Please check if backend is running properly."
                    sources = []
                    metrics = {}
                    tools_used.append("fallback")
            
            # Add agent response to memory
            self.chat_memory[session_id].append({
                "type": "agent",
                "message": response,
                "timestamp": datetime.now()
            })
            
            return {
                "response": response,
                "sources": sources,
                "metrics": metrics,
                "navigation_intent": navigation_intent,
                "tools_used": tools_used,
                "session_id": session_id
            }
        
        except Exception as e:
            print("[Agent] Chat error: " + str(e))
            return {"response": f"Error: {str(e)}", "sources": [], "metrics": {}}
    
    def _generate_analytics_report(self, query: str) -> Dict[str, Any]:
        """Generate comprehensive analytics report based on query"""
        
        # Sample analytics data generation
        analytics_data = {
            "query_type": "analytics",
            "metrics": {
                "total_revenue": np.random.uniform(1000000, 5000000),
                "conversion_rate": np.random.uniform(0.15, 0.35),
                "lead_quality_score": np.random.uniform(7.5, 9.2),
                "pipeline_velocity": np.random.uniform(30, 90),  # days
                "win_rate": np.random.uniform(0.20, 0.40),
                "deal_size": np.random.uniform(25000, 150000)
            },
            "trends": {
                "revenue_growth": np.random.uniform(0.15, 0.45),
                "lead_volume_trend": "increasing",
                "engagement_rate": np.random.uniform(0.60, 0.85),
                "market_penetration": np.random.uniform(0.25, 0.65)
            },
            "insights": [
                "Revenue increased by 23% YoY due to improved targeting",
                "Lead quality improved by 15% with AI-powered scoring",
                "Sales cycle reduced by 12 days with better insights",
                "Marketing ROI increased by 180% with predictive analytics"
            ],
            "recommendations": [
                "Focus on high-value accounts showing strong intent signals",
                "Increase marketing spend in top-performing segments",
                "Implement lead nurturing for mid-funnel opportunities",
                "Expand into industries with highest conversion rates"
            ]
        }
        
        return analytics_data
    
    def _calculate_roi(self, query: str) -> Dict[str, Any]:
        """Calculate ROI based on query parameters"""
        
        # Sample ROI calculation
        roi_data = {
            "query_type": "roi_calculation",
            "investment": {
                "platform_cost": 120000,
                "implementation_cost": 45000,
                "training_cost": 15000,
                "total_investment": 180000
            },
            "returns": {
                "revenue_increase": 450000,
                "cost_savings": 85000,
                "productivity_gain": 120000,
                "total_returns": 655000
            },
            "roi_metrics": {
                "roi_percentage": 263.9,
                "payback_period_months": 8.5,
                "npv": 425000,
                "irr": 245.6
            },
            "breakdown": {
                "marketing_roi": 312.5,
                "sales_roi": 245.8,
                "overall_roi": 263.9
            },
            "timeframe": "12 months",
            "confidence_level": 0.85
        }
        
        return roi_data
    
    def _generate_report(self, query: str) -> Dict[str, Any]:
        """Generate comprehensive report with charts and insights"""
        
        # Generate sample data for visualization
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        revenue_data = np.random.uniform(200000, 500000, 12)
        lead_data = np.random.randint(100, 500, 12)
        conversion_data = np.random.uniform(0.15, 0.35, 12)
        
        # Create visualizations
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(x=months, y=revenue_data, mode='lines+markers', name='Revenue'))
        fig_revenue.update_layout(title='Monthly Revenue Trend', xaxis_title='Month', yaxis_title='Revenue ($)')
        
        fig_leads = go.Figure()
        fig_leads.add_trace(go.Bar(x=months, y=lead_data, name='Leads Generated'))
        fig_leads.update_layout(title='Monthly Lead Generation', xaxis_title='Month', yaxis_title='Number of Leads')
        
        fig_conversion = go.Figure()
        fig_conversion.add_trace(go.Scatter(x=months, y=conversion_data, mode='lines+markers', name='Conversion Rate'))
        fig_conversion.update_layout(title='Monthly Conversion Rate', xaxis_title='Month', yaxis_title='Conversion Rate (%)')
        
        # Generate report data
        report_data = {
            "query_type": "report_generation",
            "title": "6sense Performance Analytics Report",
            "period": f"{datetime.now().strftime('%B %Y')}",
            "executive_summary": {
                "total_revenue": f"${sum(revenue_data):,.0f}",
                "total_leads": f"{sum(lead_data):,}",
                "avg_conversion_rate": f"{np.mean(conversion_data):.1%}",
                "key_achievement": "Revenue increased by 28% YoY with improved targeting"
            },
            "visualizations": {
                "revenue_chart": fig_revenue.to_json(),
                "leads_chart": fig_leads.to_json(),
                "conversion_chart": fig_conversion.to_json()
            },
            "detailed_metrics": {
                "revenue_metrics": {
                    "monthly_avg": f"${np.mean(revenue_data):,.0f}",
                    "growth_rate": "+23.5%",
                    "best_month": months[np.argmax(revenue_data)],
                    "worst_month": months[np.argmin(revenue_data)]
                },
                "lead_metrics": {
                    "monthly_avg": f"{np.mean(lead_data):.0f}",
                    "quality_score": "8.4/10",
                    "conversion_to_opportunity": "32%",
                    "pipeline_value": f"${np.mean(lead_data) * 50000:,.0f}"
                },
                "performance_metrics": {
                    "marketing_qualified_leads": f"{int(sum(lead_data) * 0.6):,}",
                    "sales_accepted_leads": f"{int(sum(lead_data) * 0.4):,}",
                    "closed_won_deals": f"{int(sum(lead_data) * 0.25):,}",
                    "average_deal_size": f"${np.random.uniform(50000, 150000):,.0f}"
                }
            },
            "insights": [
                "Q3 showed strongest performance with 34% increase in qualified leads",
                "Marketing campaigns in technology sector yielded highest ROI",
                "Sales cycle reduced by 15% with AI-powered insights",
                "Customer acquisition cost decreased by 18%"
            ],
            "recommendations": [
                "Double investment in high-performing channels",
                "Expand AI-powered targeting to additional segments",
                "Implement advanced analytics for predictive modeling",
                "Focus on customer retention strategies"
            ]
        }
        
        return report_data
    
    def _generate_infographic_data(self, query: str) -> Dict[str, Any]:
        """Generate data for infographics and visual content"""
        
        infographic_data = {
            "query_type": "infographic_generation",
            "title": "6sense Revenue AI Impact",
            "key_statistics": [
                {"label": "Revenue Increase", "value": "+45%", "icon": "📈"},
                {"label": "Lead Quality", "value": "8.7/10", "icon": "⭐"},
                {"label": "Sales Cycle Reduction", "value": "-28%", "icon": "⏱️"},
                {"label": "Marketing ROI", "value": "312%", "icon": "💰"},
                {"label": "Customer Satisfaction", "value": "94%", "icon": "😊"},
                {"label": "Market Coverage", "value": "78%", "icon": "🎯"}
            ],
            "visual_elements": {
                "progress_bars": [
                    {"label": "Target Achievement", "value": 0.87, "color": "#4CAF50"},
                    {"label": "Pipeline Health", "value": 0.92, "color": "#2196F3"},
                    {"label": "Team Adoption", "value": 0.78, "color": "#FF9800"}
                ],
                "pie_chart": {
                    "title": "Revenue Sources",
                    "data": [
                        {"label": "New Business", "value": 45, "color": "#4CAF50"},
                        {"label": "Expansion", "value": 30, "color": "#2196F3"},
                        {"label": "Renewals", "value": 25, "color": "#FF9800"}
                    ]
                }
            },
            "design_elements": {
                "color_scheme": ["#4CAF50", "#2196F3", "#FF9800", "#F44336", "#9C27B0"],
                "font_family": "Arial, sans-serif",
                "layout": "modern",
                "style": "business_infographic"
            }
        }
        
        return infographic_data
    
    def _generate_dashboard_code(self, query: str) -> str:
        """Generate intelligent, context-aware dashboard code"""
        
        # Analyze user intent
        query_lower = query.lower()
        
        # Get context from RAG if available
        context_data = []
        if RAG_AVAILABLE:
            try:
                rag_result = run_rag_query(self.rag_graph, f"dashboard data for {query}")
                context_data = rag_result.get("retrieved_docs", [])
            except:
                pass
        
        # Generate dynamic dashboard based on intent
        if "revenue" in query_lower or "sales" in query_lower:
            return self._create_revenue_dashboard(context_data)
        elif "analytics" in query_lower or "performance" in query_lower:
            return self._create_analytics_dashboard(context_data)
        elif "infographic" in query_lower or "visual" in query_lower:
            return self._create_infographic_dashboard(context_data)
        elif "report" in query_lower:
            return self._create_report_dashboard(context_data)
        else:
            # Default comprehensive dashboard
            return self._create_comprehensive_dashboard(context_data)
    
    def _create_revenue_dashboard(self, context_data: List) -> str:
        """Create revenue-focused dashboard as clean Python code"""
        
        return f'''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="💰 Revenue Analytics Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .revenue-header {{
        background: linear-gradient(135deg, #2ECC71, #27AE60);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(46, 204, 113, 0.3);
    }}
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #2ECC71;
    }}
    .chart-container {{
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="revenue-header">
    <h1>💰 Revenue Analytics Dashboard</h1>
    <p>Real-time revenue insights and performance metrics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header("📊 Controls")
    time_range = st.selectbox("📅 Time Range", ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year"])
    product_filter = st.multiselect("🎯 Products", ["Revenue AI", "Account Intelligence", "Predictive Analytics"])
    region_filter = st.selectbox("🌍 Region", ["All", "North America", "Europe", "Asia Pacific"])

# Generate sample data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue_data = np.random.normal(450000, 50000, 6)
growth_rates = np.random.normal(0.15, 0.05, 6)

# Key Metrics
st.header("🎯 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("💰 Total Revenue", f"${sum(revenue_data):,.0f}", "+15% YoY")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📈 Growth Rate", f"{np.mean(growth_rates)*100:.1f}%", "+5.2%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🎯 Conversion Rate", "24.5%", "+2.1%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("⭐ Avg Deal Size", "$125,000", "+8%")
    st.markdown('</div>', unsafe_allow_html=True)

# Revenue Trend Chart
st.header("📈 Revenue Trends")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=months,
        y=revenue_data,
        mode='lines+markers',
        line=dict(color='#2ECC71', width=4),
        marker=dict(size=10, color='#2ECC71'),
        name='Revenue'
    ))
    fig_trend.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        yaxis_tickformat='$,.0f',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(
        x=months,
        y=growth_rates * 100,
        marker=dict(color='#27AE60', line=dict(color='white', width=2)),
        name='Growth Rate %'
    ))
    fig_growth.update_layout(
        title="Monthly Growth Rates",
        xaxis_title="Month",
        yaxis_title="Growth Rate (%)",
        yaxis_ticksuffix="%",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Context from RAG
if {len(context_data)} > 0:
    st.header("📚 Context from Knowledge Base")
    for i, doc in enumerate(context_data[:3], 1):
        with st.expander(f"📄 Context Document {i}"):
            st.write(f"**Content:** {doc.get('content', 'N/A')[:300]}...")
            st.write(f"**Score:** {doc.get('score', 0):.2f}")
            if doc.get('metadata'):
                st.write("**Metadata:**")
                st.json(doc['metadata'])

st.markdown("---")
st.markdown(f"*Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
'''
    
    def _create_analytics_dashboard(self, context_data: List) -> str:
        """Create analytics-focused dashboard as clean Python code"""
        return f'''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Analytics Dashboard
st.set_page_config(
    page_title="📊 Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("# 📊 Advanced Analytics Dashboard")
st.markdown("Comprehensive performance analytics and insights")

# Analytics metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 Data Points", "15,234", "+12%")
with col2:
    st.metric("🎯 Accuracy", "94.2%", "+2.1%")
with col3:
    st.metric("⚡ Processing Speed", "1.2s", "-0.3s")

# Analytics charts
fig = px.scatter(
    x=np.random.randn(100),
    y=np.random.randn(100),
    title="Performance Distribution"
)
st.plotly_chart(fig)

# Context display
if {len(context_data)} > 0:
    for doc in context_data[:2]:
        st.write(f"**Context:** {doc.get('content', 'N/A')[:200]}...")
'''
    
    def _create_infographic_dashboard(self, context_data: List) -> str:
        """Create visual infographic dashboard as clean Python code"""
        return f'''import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Infographic Dashboard
st.set_page_config(
    page_title="🎨 Visual Infographic",
    page_icon="🎨",
    layout="wide"
)

st.markdown("# 🎨 Dynamic Infographic Generator")

# Create visual elements
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Sample data
categories = ['Revenue', 'Leads', 'Conversion', 'Satisfaction']
values = [85, 92, 78, 94]
colors = ['#2ECC71', '#3498DB', '#9B59B6', '#F39C12']

# Create charts
bars = ax1.bar(categories, values, color=colors)
ax1.set_title('Performance Metrics')

# Pie chart
sizes = [45, 30, 15, 10]
labels = ['Product A', 'Product B', 'Product C', 'Product D']
ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
ax2.set_title('Product Distribution')

# Display in Streamlit
st.pyplot(fig)

# Context integration
if {len(context_data)} > 0:
    st.markdown("## 📚 Context-Driven Insights")
    for doc in context_data:
        st.info(f"**Insight:** {doc.get('content', 'N/A')[:150]}...")
'''

def _create_report_dashboard(self, context_data: List) -> str:
    """Create report-focused dashboard as clean Python code"""
    return f'''import streamlit as st
import pandas as pd
from datetime import datetime

# Report Dashboard
st.set_page_config(
    page_title="📋 Report Generator",
    page_icon="📋",
    layout="wide"
)

st.markdown("# 📋 Intelligent Report Generator")

# Report content
st.markdown("## Executive Summary")
st.markdown("Based on analysis, here are key findings and recommendations...")

# Context-driven report
if {len(context_data)} > 0:
    st.markdown("## 📚 Knowledge Base Insights")
    for i, doc in enumerate(context_data, 1):
        st.markdown(f"### Source {i}")
        st.write(doc.get('content', 'N/A'))
        
st.markdown(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
'''

def _create_comprehensive_dashboard(self, context_data: List) -> str:
    """Create comprehensive dashboard as clean Python code"""
    return f'''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Comprehensive Dashboard
st.set_page_config(
    page_title="🚀 Comprehensive Analytics",
    page_icon="🚀",
    layout="wide"
)

st.markdown("# 🚀 Comprehensive Analytics Dashboard")
st.markdown("Complete overview of all metrics and insights")

# Multi-section layout
tab1, tab2, tab3 = st.tabs(["📊 Metrics", "📈 Analytics", "📋 Reports"])

with tab1:
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Revenue", "$2.4M", "+15%")
    with col2:
        st.metric("🎯 Conversion", "18.5%", "+2.1%")
    with col3:
        st.metric("⭐ Quality", "8.9/10", "+0.3")
    with col4:
        st.metric("📈 Growth", "23%", "+5%")

with tab2:
    st.header("Analytics Visualizations")
    # Sample chart
    fig = px.line(
        x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        y=[100, 120, 115, 140, 160, 180],
        title="Performance Trend"
    )
    st.plotly_chart(fig)

with tab3:
    st.header("Context-Driven Insights")
    if {len(context_data)} > 0:
        for doc in context_data[:3]:
            st.info(f"**Insight:** {doc.get('content', 'N/A')[:200]}...")
    else:
        st.info("No additional context available for this analysis.")

st.markdown(f"*Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
'''
    
    def _fallback_chat(self, user_query: str) -> Dict[str, Any]:
        """Fallback chat using existing RAG system"""
        if not RAG_AVAILABLE:
            return {"response": "RAG system not available", "sources": [], "metrics": {}}
        
        try:
            result = run_rag_query(self.rag_graph, user_query)
            return {
                "response": result.get("answer", ""),
                "sources": result.get("retrieved_docs", []),
                "metrics": {},
                "navigation_intent": None,
                "tools_used": ["rag_fallback"],
                "session_id": "fallback"
            }
        except Exception as e:
            return {"response": f"Error: {str(e)}", "sources": [], "metrics": {}}
    
    def _generate_code_visualization(self, code_execution: Dict, sources: List) -> str:
        """Generate actual code for visualizations and infographics"""
        viz_type = code_execution.get("type", "general")
        query = code_execution.get("query", "")
        
        if viz_type == "visualization" or "infographic" in query.lower():
            # Generate Python code for infographic
            return """
I'll create a visual infographic for you! Here's the Python code to generate an infographic based on the 6sense case studies:

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set style
plt.style.use('seaborn-v0_8')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('6sense Impact & Case Studies - Visual Infographic', fontsize=16, fontweight='bold')

# Chart 1: Company Success Metrics
companies = ['Clari', 'NanaWall', 'Khoros']
success_metrics = [85, 92, 78]  # Success scores
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

bars = ax1.bar(companies, success_metrics, color=colors)
ax1.set_title('Company Success Scores', fontweight='bold')
ax1.set_ylabel('Success Score (%)')
ax1.set_ylim(0, 100)

# Add value labels on bars
for bar, value in zip(bars, success_metrics):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{value}%', ha='center', va='bottom', fontweight='bold')

# Chart 2: ROI Timeline
months = [0, 3, 6, 9, 12]
roi_values = [0, 150, 200, 275, 350]  # Cumulative ROI %
ax2.plot(months, roi_values, marker='o', linewidth=3, markersize=8, color='#2ECC71')
ax2.fill_between(months, roi_values, alpha=0.3, color='#2ECC71')
ax2.set_title('ROI Timeline - 6sense Investment', fontweight='bold')
ax2.set_xlabel('Months')
ax2.set_ylabel('Cumulative ROI (%)')
ax2.grid(True, alpha=0.3)

# Chart 3: Industry Distribution
industries = ['Software', 'Manufacturing', 'Technology']
company_counts = [2, 1, 1]
colors = ['#9B59B6', '#E74C3C', '#F39C12']

wedges, texts, autotexts = ax3.pie(company_counts, labels=industries, colors=colors, 
                                      autopct='%1.0f', startangle=90)
ax3.set_title('Industry Distribution', fontweight='bold')

# Chart 4: Key Benefits
benefits = ['Targeting', 'Efficiency', 'ROI', 'Engagement']
impact_scores = [90, 85, 95, 80]

bars = ax4.barh(benefits, impact_scores, color=['#3498DB', '#E67E22', '#27AE60', '#8E44AD'])
ax4.set_title('Key Impact Areas', fontweight='bold')
ax4.set_xlabel('Impact Score (%)')
ax4.set_xlim(0, 100)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, impact_scores)):
    ax4.text(value + 2, i, f'{value}%', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('6sense_infographic.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Infographic generated! Check '6sense_infographic.png'")
```

This code creates a comprehensive 4-panel infographic showing:
- **Company Success Scores** - Bar chart of Clari, NanaWall, Khoros performance
- **ROI Timeline** - Line chart showing 350% ROI over 12 months  
- **Industry Distribution** - Pie chart of industries served
- **Key Impact Areas** - Horizontal bar chart of targeting, efficiency, ROI, engagement

Run this code to generate a professional infographic visualization!
"""
        
        elif viz_type == "dashboard":
            # Generate dashboard code
            return """
I'll create an interactive dashboard for you! Here's the Python code:

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Dashboard Title
st.set_page_config(page_title="6sense Analytics Dashboard", layout="wide")
st.title("🚀 6sense Performance Dashboard")
st.markdown("---")

# Sample data based on case studies
data = {
    'Company': ['Clari', 'NanaWall', 'Khoros', 'Drata'],
    'Industry': ['Software', 'Manufacturing', 'Software', 'Technology'],
    'ROI_%': [150, 200, 180, 200],
    'Efficiency_Gain': [45, 60, 50, 55],
    'Implementation_Months': [6, 8, 7, 6]
}
df = pd.DataFrame(data)

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏢 Total Companies", len(df))
with col2:
    st.metric("📈 Avg ROI", f"{df['ROI_%'].mean():.0f}%")
with col3:
    st.metric("⚡ Avg Efficiency", f"{df['Efficiency_Gain'].mean():.0f}%")
with col4:
    st.metric("⏱️ Avg Implementation", f"{df['Implementation_Months'].mean():.1f} mo")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    fig_roi = px.bar(df, x='Company', y='ROI_%', 
                   title='ROI by Company',
                   color='Company',
                   color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    fig_roi.update_layout(showlegend=False)
    st.plotly_chart(fig_roi, use_container_width=True)

with col2:
    fig_efficiency = px.scatter(df, x='Implementation_Months', y='Efficiency_Gain',
                             size='ROI_%', color='Company',
                             title='Efficiency vs Implementation Time',
                             color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    st.plotly_chart(fig_efficiency, use_container_width=True)

# Charts Row 2  
col1, col2 = st.columns(2)

with col1:
    fig_industry = px.pie(df, names='Industry', values='ROI_%',
                         title='ROI by Industry')
    st.plotly_chart(fig_industry, use_container_width=True)

with col2:
    fig_timeline = px.line(df, x='Company', y='ROI_%',
                        title='ROI Comparison',
                        markers=True,
                        line_shape='spline')
    fig_timeline.update_traces(line=dict(width=4), marker=dict(size=12))
    st.plotly_chart(fig_timeline, use_container_width=True)

# Detailed Data Table
st.markdown("### 📊 Detailed Company Data")
st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard powered by 6sense AI Analytics*")
```

This creates an interactive Streamlit dashboard with:
- **Key Metrics** - Top KPI cards
- **ROI Charts** - Bar and scatter plots  
- **Industry Analysis** - Pie chart breakdown
- **Data Table** - Detailed company information

Run with: `streamlit run dashboard.py`
"""
        
        else:
            # General code generation
            return """
I'll generate Python code for your request! Here's a template:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Your custom analysis code here
print("Code generated successfully!")
```

Let me know what specific visualization or analysis you need!
"""

    def get_conversation_history(self, session_id: str = "default") -> List[Dict]:
        """Get conversation history from simple memory"""
        return self.chat_memory.get(session_id, [])

# Initialize global agent instance
agent = AdvancedAIAgent()
