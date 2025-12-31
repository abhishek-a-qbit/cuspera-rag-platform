"""
Frontend Integration Module
Bridges the three UIs (chat, analytics, agent) with the RAG backend
"""

import requests
import json
from typing import Dict, Any, List
from enum import Enum


class InterfaceType(Enum):
    CHAT = "chat"
    ANALYTICS = "analytics"
    AGENT = "agent"


class CuspAPIClient:
    """Client for Cuspera RAG API - used by all three frontends."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    # ============ CHAT INTERFACE ============
    
    def chat(self, question: str, chat_history: List[str] = None) -> Dict[str, Any]:
        """
        Chat Interface - Conversational RAG
        Used by: cusp_consultant.html
        """
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "question": question,
                "chat_context": chat_history or []
            }
        )
        return response.json()
    
    # ============ ANALYTICS INTERFACE ============
    
    def get_analytics(self, scenario: str) -> Dict[str, Any]:
        """
        Analytics Interface - Scenario-based insights
        Used by: cuspera_analytics.txt (React component)
        
        Example: "50-person startup with 10k budget"
        """
        response = requests.post(
            f"{self.base_url}/analytics",
            json={"scenario": scenario}
        )
        return response.json()
    
    # ============ AGENT INTERFACE ============
    
    def generate_report(self, topic: str, constraints: Dict = None) -> Dict[str, Any]:
        """
        Agent Interface - Dynamic report generation
        Used by: cuspera_agent.txt (React component with Gemini)
        
        Example: topic="Growth strategy for B2B SaaS", 
                 constraints={"team_size": 50, "budget": 10000}
        """
        response = requests.post(
            f"{self.base_url}/report",
            json={
                "topic": topic,
                "constraints": constraints or {}
            }
        )
        return response.json()
    
    # ============ CORE RAG ============
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Direct RAG query - Answer + Retrieved context
        Used by: All interfaces as fallback
        """
        response = requests.post(
            f"{self.base_url}/query",
            json={"question": question, "top_k": top_k}
        )
        return response.json()
    
    def retrieve(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Retrieval only - No generation
        Used by: Analytics interface for data extraction
        """
        response = requests.post(
            f"{self.base_url}/retrieve",
            json={"question": question, "top_k": top_k}
        )
        return response.json()
    
    # ============ SYSTEM ============
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health and readiness."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_products(self) -> Dict[str, Any]:
        """List available products."""
        response = requests.get(f"{self.base_url}/products")
        return response.json()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        response = requests.get(f"{self.base_url}/stats")
        return response.json()


# ============ INTEGRATION EXAMPLES ============

class ChatInterfaceAdapter:
    """Adapter for cusp_consultant.html - Chat UI."""
    
    def __init__(self):
        self.client = CuspAPIClient()
        self.chat_history = []
    
    def handle_user_input(self, user_message: str) -> str:
        """
        Process user message and return AI response.
        Maps to chat interface logic.
        """
        self.chat_history.append(f"User: {user_message}")
        
        # Call RAG
        result = self.client.chat(user_message, self.chat_history)
        
        answer = result.get("answer", "")
        self.chat_history.append(f"Assistant: {answer}")
        
        return answer
    
    def get_follow_ups(self, last_query: str) -> List[str]:
        """Get suggested follow-up questions."""
        result = self.client.chat(last_query)
        return result.get("follow_up_suggestions", [])


class AnalyticsInterfaceAdapter:
    """Adapter for cuspera_analytics.txt - Analytics UI."""
    
    def __init__(self):
        self.client = CuspAPIClient()
    
    def analyze_scenario(self, scenario: str) -> Dict[str, Any]:
        """
        Analyze a startup scenario.
        
        Example scenario: "50-person startup with 10k budget"
        Returns: {"pricing": {...}, "metrics": [...], "features": [...]}
        """
        result = self.client.get_analytics(scenario)
        
        # Transform for React component
        return {
            "scenario": scenario,
            "pricing_data": result.get("analytics", {}).get("pricing"),
            "metrics": result.get("analytics", {}).get("metrics"),
            "features": result.get("analytics", {}).get("features"),
            "integrations": result.get("analytics", {}).get("integrations"),
            "chart_recommendations": result.get("charts", {}).get("recommended", [])
        }


class AgentInterfaceAdapter:
    """Adapter for cuspera_agent.txt - AI Agent UI."""
    
    def __init__(self):
        self.client = CuspAPIClient()
    
    def generate_strategic_report(self, topic: str, constraints: Dict = None) -> Dict[str, Any]:
        """
        Generate dynamic strategic report with Gemini.
        
        Example:
        - topic: "Growth strategy for B2B SaaS"
        - constraints: {"team_size": 50, "budget": 10000}
        
        Returns: JSON with title, kpis, insights, recommendation, data for charts
        """
        result = self.client.generate_report(topic, constraints)
        
        # Return structured report for React component
        return {
            "title": result.get("report", {}).get("title"),
            "summary": result.get("report", {}).get("summary"),
            "kpis": result.get("report", {}).get("kpis", []),
            "insights": result.get("report", {}).get("insights", []),
            "recommendation": result.get("report", {}).get("recommendation"),
            "chart_type": result.get("report", {}).get("chartType", "bar"),
            "chart_data": result.get("report", {}).get("data", []),
            "sources_used": result.get("sources_used", 0),
            "metadata": result.get("metadata", {})
        }


# ============ USAGE EXAMPLES ============

def example_chat_flow():
    """Example: Chat Interface Flow."""
    adapter = ChatInterfaceAdapter()
    
    # User asks a question
    response = adapter.handle_user_input("What are the key capabilities of 6sense?")
    print(f"Assistant: {response}\n")
    
    # Get follow-ups
    follow_ups = adapter.get_follow_ups("What are the key capabilities of 6sense?")
    print(f"Follow-up suggestions: {follow_ups}\n")


def example_analytics_flow():
    """Example: Analytics Interface Flow."""
    adapter = AnalyticsInterfaceAdapter()
    
    # Analyze scenario
    analysis = adapter.analyze_scenario("50-person startup with 10k budget for lead gen")
    print(json.dumps(analysis, indent=2))


def example_agent_flow():
    """Example: Agent Interface Flow."""
    adapter = AgentInterfaceAdapter()
    
    # Generate report
    report = adapter.generate_strategic_report(
        topic="Growth strategy for B2B SaaS startup",
        constraints={
            "team_size": 50,
            "budget": 10000,
            "timeline": "6 months",
            "industry": "B2B SaaS"
        }
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    print("="*60)
    print("Cuspera Frontend Integration Examples")
    print("="*60)
    
    print("\n[EXAMPLE 1] Chat Flow")
    print("-"*60)
    try:
        example_chat_flow()
    except Exception as e:
        print(f"Error (API might not be running): {e}")
    
    print("\n[EXAMPLE 2] Analytics Flow")
    print("-"*60)
    try:
        example_analytics_flow()
    except Exception as e:
        print(f"Error (API might not be running): {e}")
    
    print("\n[EXAMPLE 3] Agent Flow")
    print("-"*60)
    try:
        example_agent_flow()
    except Exception as e:
        print(f"Error (API might not be running): {e}")
