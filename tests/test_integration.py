#!/usr/bin/env python3
"""
Integration Tests for Cuspera RAG System
Tests all components work together correctly
"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, Any
import sys

class RAGSystemTest:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test(self, name: str, func):
        """Run a single test."""
        try:
            print(f"\n🧪 {name}...")
            result = func()
            self.passed += 1
            self.results.append({"name": name, "status": "✓ PASS", "result": result})
            print(f"   ✓ PASS")
            return result
        except Exception as e:
            self.failed += 1
            self.results.append({"name": name, "status": "✗ FAIL", "error": str(e)})
            print(f"   ✗ FAIL: {str(e)[:100]}")
            return None
    
    def run_all(self):
        """Run all tests."""
        print("\n" + "="*70)
        print("CUSPERA RAG SYSTEM - INTEGRATION TESTS")
        print("="*70)
        
        # Health checks
        print("\n" + "-"*70)
        print("PHASE 1: System Health")
        print("-"*70)
        
        self.test("API is running", self._test_health)
        self.test("Products endpoint", self._test_products)
        self.test("System stats", self._test_stats)
        
        # RAG Core
        print("\n" + "-"*70)
        print("PHASE 2: RAG Core Functionality")
        print("-"*70)
        
        self.test("Direct query (answer + context)", self._test_query)
        self.test("Document retrieval only", self._test_retrieve)
        self.test("Query with top-k filtering", self._test_retrieve_topk)
        
        # Interfaces
        print("\n" + "-"*70)
        print("PHASE 3: User Interfaces")
        print("-"*70)
        
        self.test("Chat interface", self._test_chat)
        self.test("Chat with history", self._test_chat_history)
        self.test("Analytics scenario", self._test_analytics)
        self.test("Strategic report", self._test_report)
        
        # Data Quality
        print("\n" + "-"*70)
        print("PHASE 4: Data Quality")
        print("-"*70)
        
        self.test("Retrieved docs have metadata", self._test_doc_metadata)
        self.test("Answer is not empty", self._test_answer_quality)
        self.test("Sources are relevant", self._test_source_relevance)
        
        # Report
        print("\n" + "="*70)
        print("TEST RESULTS")
        print("="*70)
        print(f"\n✓ Passed: {self.passed}")
        print(f"✗ Failed: {self.failed}")
        print(f"📊 Total:  {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Your RAG system is ready to go!")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. See details above.")
        
        return self.failed == 0
    
    # ==================== TESTS ====================
    
    def _test_health(self):
        """Test health endpoint."""
        resp = requests.get(f"{self.api_url}/health")
        assert resp.status_code == 200, f"HTTP {resp.status_code}"
        data = resp.json()
        assert data.get("status") == "healthy", "Not healthy"
        return data
    
    def _test_products(self):
        """Test products endpoint."""
        resp = requests.get(f"{self.api_url}/products")
        assert resp.status_code == 200
        data = resp.json()
        assert "products" in data, "No products key"
        assert len(data["products"]) > 0, "No products returned"
        return f"Found {len(data['products'])} product(s)"
    
    def _test_stats(self):
        """Test stats endpoint."""
        resp = requests.get(f"{self.api_url}/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "vector_store" in data, "No vector store stats"
        return f"Vector store has {data['vector_store'].get('count', 0)} documents"
    
    def _test_query(self):
        """Test direct RAG query."""
        resp = requests.post(
            f"{self.api_url}/query",
            json={"question": "What are the main capabilities?", "top_k": 5}
        )
        assert resp.status_code == 200, f"HTTP {resp.status_code}"
        data = resp.json()
        assert data.get("success"), "Not successful"
        assert data.get("answer"), "No answer"
        assert data.get("context"), "No context"
        assert len(data["context"]["top_sources"]) > 0, "No sources"
        return f"Retrieved {data['context'].get('documents_retrieved', 0)} documents"
    
    def _test_retrieve(self):
        """Test retrieval only."""
        resp = requests.post(
            f"{self.api_url}/retrieve",
            json={"question": "pricing strategy", "top_k": 3}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success"), "Not successful"
        assert data.get("documents"), "No documents"
        assert len(data["documents"]) > 0, "Empty results"
        return f"Retrieved {len(data['documents'])} documents"
    
    def _test_retrieve_topk(self):
        """Test top-k filtering."""
        resp = requests.post(
            f"{self.api_url}/retrieve",
            json={"question": "capabilities", "top_k": 3}
        )
        data = resp.json()
        assert len(data["documents"]) <= 3, "Returned more than top_k"
        return f"Correctly limited to {len(data['documents'])} results"
    
    def _test_chat(self):
        """Test chat interface."""
        resp = requests.post(
            f"{self.api_url}/chat",
            json={"question": "What is this product about?"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success"), "Not successful"
        assert data.get("answer"), "No answer"
        assert "follow_up" in data, "No follow-up suggestions"
        return "Chat interface working"
    
    def _test_chat_history(self):
        """Test chat with history."""
        resp = requests.post(
            f"{self.api_url}/chat",
            json={
                "question": "Tell me more",
                "chat_context": [
                    "User: What are the capabilities?",
                    "Assistant: ..."
                ]
            }
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success"), "Not successful"
        return "Chat history context working"
    
    def _test_analytics(self):
        """Test analytics endpoint."""
        resp = requests.post(
            f"{self.api_url}/analytics",
            json={"scenario": "50-person startup with 10000 budget"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success"), "Not successful"
        assert data.get("analytics"), "No analytics"
        return "Analytics endpoint working"
    
    def _test_report(self):
        """Test report generation."""
        resp = requests.post(
            f"{self.api_url}/report",
            json={
                "topic": "Growth strategy for B2B SaaS",
                "constraints": {"team_size": 50, "budget": 10000}
            }
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("success"), "Not successful"
        assert data.get("report"), "No report"
        return "Report generation working"
    
    def _test_doc_metadata(self):
        """Test that documents have proper metadata."""
        resp = requests.post(
            f"{self.api_url}/retrieve",
            json={"question": "features", "top_k": 1}
        )
        data = resp.json()
        docs = data.get("documents", [])
        assert len(docs) > 0, "No documents"
        doc = docs[0]
        assert "metadata" in doc, "No metadata"
        assert "id" in doc, "No id"
        assert "content" in doc, "No content"
        return "All documents have proper structure"
    
    def _test_answer_quality(self):
        """Test answer quality."""
        resp = requests.post(
            f"{self.api_url}/query",
            json={"question": "What is this product?"}
        )
        data = resp.json()
        answer = data.get("answer", "")
        assert len(answer) > 50, "Answer too short"
        assert answer.lower() != "i don't know", "Empty answer"
        return f"Answer quality good ({len(answer)} chars)"
    
    def _test_source_relevance(self):
        """Test that sources are relevant."""
        resp = requests.post(
            f"{self.api_url}/query",
            json={"question": "capabilities and features"}
        )
        data = resp.json()
        sources = data.get("context", {}).get("top_sources", [])
        assert len(sources) > 0, "No sources"
        for source in sources:
            assert "relevance_score" in source, "No relevance score"
            score = source["relevance_score"]
            assert 0 <= score <= 1, f"Invalid relevance score: {score}"
        return f"All {len(sources)} sources have valid relevance scores"


def main():
    """Run all tests."""
    print("\n⏳ Waiting for API to be ready (checking for 30 seconds)...")
    
    for i in range(30):
        try:
            resp = requests.get("http://localhost:8000/health", timeout=2)
            if resp.status_code == 200:
                print("✓ API is responding!\n")
                break
        except:
            if i < 29:
                print(".", end="", flush=True)
                time.sleep(1)
    else:
        print("\n❌ API is not responding. Start it with: python api_backend.py")
        return False
    
    # Run tests
    tester = RAGSystemTest()
    success = tester.run_all()
    
    # Save results
    results_file = Path(__file__).parent / "test_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": str(time.time()),
            "passed": tester.passed,
            "failed": tester.failed,
            "results": tester.results
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: test_results.json")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
