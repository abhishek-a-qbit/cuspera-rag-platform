from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

app = FastAPI(
    title="Cuspera RAG API",
    description="Product Intelligence RAG System",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    product: str = "6sense"

class ChatResponse(BaseModel):
    answer: str
    sources: list = []
    context: str = "Fallback response"
    confidence: float = 0.5
    follow_up_suggestions: list = []

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Railway API", "backend": "simple"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        question = request.question
        product = request.product
        
        # Simple fallback responses for common 6sense questions
        if "pricing" in question.lower():
            answer = """6sense offers flexible pricing plans tailored to different business needs:

🏷 **Enterprise Plan**: Custom pricing for large organizations with advanced features, dedicated support, and full platform access.

📈 **Business Plan**: Mid-market pricing with core AI features, predictive analytics, and standard support.

🚀 **Startup Plan**: Entry-level pricing for small businesses getting started with AI-powered insights.

For specific pricing details, I recommend contacting 6sense directly for a customized quote based on your company size, industry, and specific requirements."""
        elif "features" in question.lower():
            answer = """6sense stands out with several key features that differentiate it in the B2B Revenue AI space:

🎯 **Predictive Analytics**: AI-powered identification of in-market buyers before they show intent.

📊 **Account Intelligence**: Comprehensive account-level insights and predictive scoring.

🎪 **Journey Tracking**: Complete buyer journey mapping and engagement tracking.

📧 **CRM Integration**: Seamless integration with existing CRM systems.

🔍 **Intent Data**: Real-time buyer intent detection and behavioral analysis.

⚡ **Real-Time Alerts**: Immediate notifications for high-value opportunities.

📈 **Multi-Touch Attribution**: Accurate attribution across all marketing channels.

🎛 **Audience Building**: Lookalike audience expansion and targeting.

These features work together to help B2B companies identify and engage with their most valuable prospects at the right time."""
        elif "roi" in question.lower() or "return on investment" in question.lower():
            answer = """6sense typically delivers strong ROI through several key mechanisms:

💰 **Reduced Waste**: Focuses marketing spend on accounts most likely to convert.

⚡ **Faster Sales Cycles**: Identifies in-market buyers, shortening sales cycles.

📈 **Higher Win Rates**: AI-powered targeting increases conversion rates.

🎯 **Better Lead Quality**: Predictive scoring improves lead qualification.

📊 **Improved Forecasting**: Data-driven sales forecasting and pipeline management.

🔄 **Account Expansion**: Identifies expansion opportunities within existing accounts.

⏭ **Competitive Advantage**: Early identification of market opportunities competitors miss.

📱 **Mobile Engagement**: Real-time mobile engagement tracking and insights.

Companies typically see 3-5x ROI within the first year, with significant improvements in conversion rates and sales efficiency."""
        else:
            answer = f"""I understand you're asking about: '{question}'. 

6sense is a powerful B2B Revenue AI platform that helps companies identify and target in-market buyers through predictive analytics and AI-powered insights. The platform combines advanced machine learning with comprehensive data integration to drive revenue growth and improve marketing effectiveness.

Key capabilities include predictive analytics, account intelligence, journey tracking, and seamless CRM integration to help B2B sales and marketing teams work more efficiently and close more deals.

For specific information about pricing, features, or implementation details, I recommend contacting 6sense directly or visiting their official website for the most current and detailed information."""
        
        return ChatResponse(
            answer=answer,
            sources=[],
            context="Fallback response - Railway API working",
            confidence=0.7,
            follow_up_suggestions=[
                "What are the pricing plans for 6sense?",
                "What are the key features of 6sense?",
                "What is the typical ROI with 6sense?",
                "How does 6sense integrate with existing systems?"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
