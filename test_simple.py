import requests
import json

# API endpoint
API_URL = "http://localhost:8001/advanced-chat"

# Test queries
test_queries = [
    "Create dashboard showing 6sense metrics",
    "Generate analytics report",
    "Calculate ROI for marketing",
    "Show revenue trends"
]

print("Testing 6sense AI Agent Dashboard Generation")
print("=" * 50)

for i, query in enumerate(test_queries, 1):
    print(f"\nTest {i}: {query}")
    print("-" * 40)
    
    try:
        response = requests.post(
            API_URL,
            json={"message": query, "session_id": f"test_{i}"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if dashboard was generated
            tools_used = result.get("tools_used", [])
            if "dashboard_generation" in tools_used:
                print("✅ Dashboard code generated successfully!")
                print(f"Response length: {len(result['response'])} characters")
                print(f"Metrics: {result.get('metrics', {})}")
            else:
                print("ℹ️ Regular response (not dashboard)")
                print(f"Response: {result['response'][:200]}...")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

print("\n" + "=" * 50)
print("Testing complete!")
