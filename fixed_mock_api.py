"""
Fixed Mock API with proper JSON responses
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    response = jsonify({
        "status": "healthy",
        "product": {
            "canonical_name": "6sense Revenue AI",
            "domain": "6sense.com",
            "total_documents": 261,
            "datasets": 23
        },
        "rag_ready": True,
        "vector_store_ready": True
    })
    response.headers.add('Content-Type', 'application/json')
    return response

@app.route('/query')
def query():
    question = request.args.get('question', 'Default question')
    response_data = {
        "question": question,
        "answer": f"Based on the 6sense platform data, here's an intelligent response to: {question}. The 6sense Revenue AI platform provides predictive analytics and AI-powered insights to help B2B companies identify in-market buyers and accelerate revenue growth.",
        "retrieved_docs": [
            {"content": "6sense helps companies identify anonymous buyers", "metadata": {"source": "capabilities"}},
            {"content": "AI-powered predictive analytics drive better conversions", "metadata": {"source": "analytics"}}
        ],
        "metadata": {
            "retrieval_count": 2,
            "documents_used": 2,
            "response_time": "0.8s"
        }
    }
    return Response(json.dumps(response_data), mimetype='application/json')

@app.route('/analytics')
def analytics():
    team_size = request.args.get('team_size', '50')
    budget = request.args.get('budget', '10000')
    timeline = request.args.get('timeline', '6 months')
    industry = request.args.get('industry', 'Technology')
    
    response_data = {
        "scenario": {
            "team_size": team_size,
            "budget": budget,
            "timeline": timeline,
            "industry": industry
        },
        "pricing": {
            "pricingModels": ["Custom Enterprise", "Tiered Pricing", "Usage-Based"],
            "timeToValue": "3-6 months",
            "data": "6sense offers flexible pricing plans based on your specific needs and company size. Contact their sales team for a customized quote tailored to your requirements."
        },
        "metrics": [
            {"label": "Lead Generation Improvement", "value": "85%", "category": "Performance"},
            {"label": "Conversion Rate Increase", "value": "92%", "category": "Performance"},
            {"label": "ROI Achievement", "value": "280%", "category": "Financial"},
            {"label": "Sales Cycle Reduction", "value": "45%", "category": "Efficiency"}
        ],
        "features": [
            "AI-Powered Predictive Analytics",
            "Real-Time Buyer Intent Data",
            "Account-Based Marketing",
            "Sales Intelligence Platform",
            "CRM Integration",
            "Custom Dashboards",
            "Lead Scoring",
            "Opportunity Insights",
            "Competitive Intelligence",
            "Marketing Attribution",
            "Revenue Forecasting",
            "Customer Journey Mapping"
        ],
        "integrations": [
            "Salesforce",
            "HubSpot",
            "Marketo",
            "Microsoft Dynamics",
            "Google Analytics",
            "LinkedIn",
            "Adobe Analytics",
            "Oracle Eloqua",
            "Pardot",
            "Mailchimp",
            "Slack",
            "Teams"
        ]
    }
    return Response(json.dumps(response_data), mimetype='application/json')

@app.route('/report')
def report():
    topic = request.args.get('topic', '6sense Platform Analysis')
    team_size = request.args.get('team_size', '50')
    budget = request.args.get('budget', '10000')
    
    response_data = {
        "success": True,
        "report": {
            "title": f"Strategic Analysis: {topic}",
            "summary": f"This comprehensive analysis of {topic} provides key insights for organizations with {team_size} team members and budget of ${budget}. The 6sense Revenue AI platform offers significant opportunities for B2B revenue growth through predictive analytics and AI-powered insights.",
            "insights": [
                "AI-powered predictive analytics can increase lead conversion rates by up to 85%",
                "Real-time buyer intent data helps identify in-market prospects 3-6 months earlier",
                "Account-based marketing strategies show 280% ROI improvement",
                "Sales cycle reduction of 45% through intelligent lead scoring",
                "Marketing attribution accuracy improves by 70% with 6sense analytics"
            ],
            "kpis": [
                {"name": "Analysis Confidence", "value": "85%"},
                {"name": "Data Sources", "value": "261"},
                {"name": "Relevance Score", "value": "High"},
                {"name": "Market Coverage", "value": "92%"},
                {"name": "Accuracy Rate", "value": "88%"},
                {"name": "Growth Potential", "value": "High"}
            ],
            "recommendation": f"Based on the analysis, organizations should implement 6sense's AI-powered platform to accelerate revenue growth. With a budget of ${budget} and team size of {team_size}, the expected ROI is 280% within 6-12 months.",
            "metadata": {
                "analysis_date": "2025-12-31",
                "data_points": 261,
                "confidence_level": "85%"
            }
        },
        "sources_used": 15,
        "metadata": {
            "generation_time": "2.3s",
            "model": "Advanced Analytics Engine"
        }
    }
    return Response(json.dumps(response_data), mimetype='application/json')

# Add a root route to prevent 404 errors
@app.route('/')
def root():
    return jsonify({
        "message": "Cuspera RAG Mock API",
        "status": "running",
        "endpoints": ["/health", "/query", "/analytics", "/report"]
    })

if __name__ == "__main__":
    print("🚀 Fixed Mock API Server for Cuspera RAG")
    print("=" * 50)
    print("📡 Proper JSON responses")
    print("🌐 Ready for Streamlit Cloud")
    print("🔄 Server starting on port 5000...")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
