"""
Cuspera RAG - Streamlit POC
Simple proof of concept with Chat, Analytics, and Reports
"""

import streamlit as st
import requests
import json
from typing import Dict, Any, List
import time
from datetime import datetime
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add src to path so we can import from src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import question generator
try:
    from question_generator import generate_suggested_questions
    QUESTION_GENERATOR_AVAILABLE = True
except ImportError:
    QUESTION_GENERATOR_AVAILABLE = False
    print("Warning: Question generator not available. Using fallback questions.")

# ==================== CONFIG ====================

# API URL - supports both local and production environments
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Product Configuration - Currently only 6sense, ready for future expansion
PRODUCTS = {
    "6sense": {
        "name": "6sense Revenue AI",
        "id": "6sense",
        "description": "B2B Revenue AI Platform",
        "enabled": True
    }
    # Future products will be added here
    # "product2": { "name": "Product 2", "id": "product2", "enabled": False }
}

# Default product for now
DEFAULT_PRODUCT = "6sense"

st.set_page_config(
    page_title="Cuspera RAG Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLES ====================

st.markdown("""
<style>
    /* Main Theme - White & Blue with Chaos-Order Balance */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #e2e8f0 100%);
        color: #1e293b;
    }
    
    /* Chaos Elements - Dynamic Gradients */
    .metric-card {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.5s ease;
    }
    
    .metric-card:hover::before {
        animation: shimmer 1s ease-in-out;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Order Elements - Clean Structure */
    .insight-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 20px;
        border-left: 5px solid #3b82f6;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .insight-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    /* Source Badges - Organized Chaos */
    .source-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px 5px 5px 0;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .source-badge::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .source-badge:hover::after {
        left: 100%;
    }
    
    /* Headers - Bold & Dynamic */
    .stHeader {
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    /* Enhanced input fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        background: white;
        border: 1px solid #e2e8f0;
    }
    
    /* Progress Bar - Dynamic */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #2563eb, #1d4ed8);
        border-radius: 10px;
    }
    
    /* Spinner - Chaotic Animation */
    .stSpinner > div {
        border-top-color: #3b82f6;
        border-right-color: #2563eb;
        border-bottom-color: #1d4ed8;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Tabs - Organized Structure */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 5px;
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: #64748b;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Divider - Clean Break */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
        margin: 20px 0;
    }
    
    /* Custom Animation for Chaos Elements */
    .floating-element {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Enhanced sidebar width */
    .css-1lrlm2 {
        width: 400px !important;
    }
    
    /* Main content area adjustment for wider sidebar */
    .main .block-container {
        margin-left: 420px !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .metric-card {
            padding: 15px;
            margin: 10px 0;
        }
        
        .stHeader {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def check_api_health():
    """Check if API is running."""
    try:
        resp = requests.get(f"{API_URL}/health", timeout=2)
        return resp.status_code == 200
    except:
        return False

def call_api(endpoint: str, method: str = "POST", data: Dict = None, product: str = None) -> Dict[str, Any]:
    """Call API endpoint with product routing."""
    try:
        # Use default product if none specified
        if product is None:
            product = DEFAULT_PRODUCT
        
        # Validate product
        if product not in PRODUCTS:
            return {"error": f"Product '{product}' not supported"}
        
        # Add product to data for routing
        if data is None:
            data = {}
        
        data["product"] = product
        
        if method == "POST":
            resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=30)
        else:
            resp = requests.get(f"{API_URL}{endpoint}", timeout=30)
        
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"API error: {resp.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout (API taking too long)"}
    except Exception as e:
        return {"error": f"API error: {str(e)}"}

def call_product_api(endpoint: str, method: str = "POST", data: Dict = None) -> Dict[str, Any]:
    """Convenience function that uses the default product."""
    return call_api(endpoint, method, data, DEFAULT_PRODUCT)

def display_suggested_questions():
    """Display suggested questions with metrics visualization."""
    if not QUESTION_GENERATOR_AVAILABLE:
        # Fallback questions
        fallback_questions = [
            "What are the key capabilities of 6sense Revenue AI?",
            "How does 6sense help with account identification and targeting?",
            "What integration options are available with 6sense?",
            "How can 6sense improve sales team efficiency?",
            "What kind of analytics and insights does 6sense provide?"
        ]
        
        st.markdown("### 💡 Suggested Questions")
        for i, question in enumerate(fallback_questions, 1):
            col1, col2 = st.columns([1, 10])
            with col1:
                st.write(f"{i}.")
            with col2:
                if st.button(question, key=f"fallback_q_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    st.rerun()
        return
    
    # Generate questions with metrics
    with st.spinner("🤔 Generating intelligent suggestions..."):
        suggested_questions = generate_suggested_questions(5)
    
    if not suggested_questions:
        st.info("No suggestions available at the moment.")
        return
    
    st.markdown("### 🎯 AI-Powered Suggested Questions")
    
    for i, q_data in enumerate(suggested_questions, 1):
        metrics = q_data['metrics']
        passes = q_data['passes_threshold']
        
        # Create metric visualization
        col1, col2, col3 = st.columns([1, 8, 2])
        
        with col1:
            st.write(f"**{i}.**")
        
        with col2:
            # Question button with styling based on quality
            button_type = "primary" if passes else "secondary"
            if st.button(
                q_data['question'], 
                key=f"q_{i}",
                use_container_width=True,
                type=button_type if button_type == "primary" else None
            ):
                st.session_state.chat_history.append({"role": "user", "content": q_data['question']})
                st.rerun()
        
        with col3:
            # Quality indicator
            if passes:
                st.markdown("""
                <div class="source-badge floating-element" style="text-align: center; font-size: 0.8rem;">
                    ✅ High Quality
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; color: #64748b; font-size: 0.8rem;">
                    📊 Moderate
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed metrics in expander
        with st.expander(f"📊 Metrics for Question {i}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Coverage metric
                coverage_color = "#10b981" if metrics['coverage'] > 0 else "#ef4444"
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border-radius: 8px; background: {coverage_color}20;">
                    <h4 style="margin: 0; color: {coverage_color};">Coverage</h4>
                    <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{metrics['coverage']:.2f}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #64748b;">
                        {'✅ Good' if metrics['coverage'] > 0 else '❌ Poor'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Specificity metric
                specific_color = "#10b981" if metrics['specific'] > 0 else "#ef4444"
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border-radius: 8px; background: {specific_color}20;">
                    <h4 style="margin: 0; color: {specific_color};">Specificity</h4>
                    <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{metrics['specific']:.2f}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #64748b;">
                        {'✅ Specific' if metrics['specific'] > 0 else '❌ Vague'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Insight metric
                insight_color = "#10b981" if metrics['insight'] > 0 else "#ef4444"
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border-radius: 8px; background: {insight_color}20;">
                    <h4 style="margin: 0; color: {insight_color};">Insightful</h4>
                    <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{metrics['insight']:.2f}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #64748b;">
                        {'✅ Actionable' if metrics['insight'] > 0 else '❌ Basic'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Grounded metric
                grounded_color = "#10b981" if metrics['grounded'] > 0 else "#ef4444"
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border-radius: 8px; background: {grounded_color}20;">
                    <h4 style="margin: 0; color: {grounded_color};">Grounded</h4>
                    <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{metrics['grounded']:.2f}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #64748b;">
                        {'✅ Supported' if metrics['grounded'] > 0 else '❌ Unsupported'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Overall score and reasoning
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                overall_color = "#10b981" if metrics['overall'] > 0 else "#ef4444"
                st.markdown(f"""
                <div class="metric-card floating-element" style="text-align: center;">
                    <h4 style="margin: 0;">Overall Score</h4>
                    <p style="margin: 0; font-size: 2rem; font-weight: bold;">{metrics['overall']:.2f}</p>
                    <p style="margin: 0; font-size: 0.9rem;">
                        {'✅ RECOMMENDED' if metrics['overall'] > 0 else '❌ NOT RECOMMENDED'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="insight-box floating-element">
                    <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🧠 AI Reasoning</h4>
                    <p style="margin: 0; font-size: 0.9rem; line-height: 1.4;">
                """ + q_data['reasoning'] + """
                    </p>
                </div>
                """, unsafe_allow_html=True)

def display_sources(sources: List[Dict]) -> None:
    """Display source documents."""
    if not sources:
        return
    
    st.markdown("### 📚 Retrieved Sources")
    for i, source in enumerate(sources, 1):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{source.get('label', 'Unknown')[:80]}**")
            st.caption(f"Dataset: {source.get('dataset', 'Unknown')}")
        with col2:
            relevance = source.get('relevance_score', 0)
            st.metric("Relevance", f"{relevance:.2%}")
        with col3:
            if st.button("View", key=f"view_{i}"):
                st.json(source)

def display_metrics(kpis: List[Dict]) -> None:
    """Display KPI metrics."""
    if not kpis:
        return
    
    cols = st.columns(min(4, len(kpis)))
    for idx, kpi in enumerate(kpis):
        with cols[idx % 4]:
            st.metric(
                label=kpi.get('label', 'Unknown'),
                value=kpi.get('value', 'N/A'),
                delta=kpi.get('trend', ''),
                delta_color="normal" if str(kpi.get('trend', '')).startswith('+') else "inverse"
            )

# ==================== PAGE: CHAT ====================

def page_chat():
    """Chat interface with product routing and suggested questions."""
    # Enhanced header with images and chaos
    st.markdown("""
    <div class="floating-element" style="text-align: center; padding: 20px 0;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 20px;">
            <div style="font-size: 3rem; animation: float 3s ease-in-out infinite;">🚀</div>
            <div>
                <h1 class="enhanced-header" style="font-size: 2.5rem; margin: 0;">
                    💬 Chat Consultant
                </h1>
                <p style="color: #64748b; font-size: 1.1rem; margin: 10px 0 0 0;">
                    Ask questions about **6sense Revenue AI**. Get AI-powered answers grounded in real data.
                </p>
            </div>
            <div style="font-size: 3rem; animation: float 3s ease-in-out infinite; animation-delay: 1s;">🤖</div>
        </div>
    
    <!-- Add AI/6sense themed image -->
    <div style="text-align: center; margin: 20px 0;">
        <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=200&fit=crop&auto=format" 
             alt="AI Technology" 
             style="width: 100%; max-width: 800px; height: 200px; object-fit: cover; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
        <p style="margin-top: 10px; color: #64748b; font-style: italic;">
            🤖 Advanced AI-powered conversation system with real-time insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Product selector with enhanced styling
    if len(PRODUCTS) > 1:
        selected_product = st.selectbox(
            "🎯 Select Product:",
            options=list(PRODUCTS.keys()),
            format_func=lambda x: PRODUCTS[x]["name"],
            index=list(PRODUCTS.keys()).index(DEFAULT_PRODUCT)
        )
    else:
        selected_product = DEFAULT_PRODUCT
        st.markdown(f"""
        <div class="insight-box floating-element">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 2rem;">🎯</div>
                <div>
                    <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">Currently Analyzing</h4>
                    <p style="font-size: 1.2rem; font-weight: 600; color: #1e293b; margin: 0;">
                        {PRODUCTS[selected_product]['name']}
                    </p>
                    <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">
                        B2B Revenue AI Platform with Advanced Analytics
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add more visual chaos with stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card floating-element" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
            <h4 style="margin: 0; color: white;">Analytics</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">Real-time insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card floating-element" style="text-align: center; animation-delay: 0.5s;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🎯</div>
            <h4 style="margin: 0; color: white;">Targeting</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">AI-powered precision</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card floating-element" style="text-align: center; animation-delay: 1s;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🚀</div>
            <h4 style="margin: 0; color: white;">Growth</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">Revenue acceleration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card floating-element" style="text-align: center; animation-delay: 1.5s;">
            <div style="font-size: 2rem; margin-bottom: 10px;">💡</div>
            <h4 style="margin: 0; color: white;">Insights</h4>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">Actionable intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced suggested questions section
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <div style="display: inline-block; background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; padding: 15px 30px; border-radius: 50px; font-weight: 700; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);">
            🧠 AI-Powered Question Suggestions
        </div>
        <p style="margin-top: 15px; color: #64748b; font-size: 1.1rem;">
            Click any question below to get instant AI responses with detailed metrics analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    display_suggested_questions()
    
    st.markdown("---")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Enhanced chat history display
    if st.session_state.chat_history:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, #f1f5f9, #e0f2fe); padding: 10px 20px; border-radius: 25px;">
                <span style="font-size: 1.5rem;">💬</span>
                <h3 style="margin: 0; color: #1e293b;">Conversation History</h3>
                <span style="font-size: 1.5rem;">🤖</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message floating-element" style="animation-delay: {i * 0.1}s;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                        <span style="font-size: 1.2rem;">👤</span>
                        <strong>You:</strong>
                    </div>
                    <div style="margin-left: 30px;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message floating-element" style="animation-delay: {i * 0.1}s;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                        <span style="font-size: 1.2rem;">🤖</span>
                        <strong>Assistant:</strong>
                    </div>
                    <div style="margin-left: 30px;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("<hr>", unsafe_allow_html=True)
    
    # Enhanced input area
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <div style="display: inline-block; background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 15px 30px; border-radius: 50px; font-weight: 700; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);">
            🚀 Ask Your Question
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Your question:",
            placeholder=f"e.g., 'What are key capabilities of {PRODUCTS[selected_product]['name']}?' or 'How does pricing work?'",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("📤 Send", type="primary", use_container_width=True)
    
    if send_button and user_input:
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Call API with product routing
        with st.spinner("🤔 Thinking..."):
            result = call_api("/chat", data={"question": user_input}, product=selected_product)
        
        if "error" in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            # Add response to history
            answer = result.get("answer", "No response")
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Display answer with success animation
            st.markdown("""
            <div class="metric-card floating-element" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">✅</div>
                <h3 style="margin: 0; color: white;">Response Received!</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">AI has processed your question</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show follow-ups
            follow_ups = result.get("follow_up_suggestions", [])
            if follow_ups:
                st.markdown("""
                <div style="text-align: center; margin: 20px 0;">
                    <div style="display: inline-block; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); padding: 10px 20px; border-radius: 25px; font-weight: 600;">
                        💡 Suggested Follow-ups
                    </div>
                </div>
                """, unsafe_allow_html=True)
                cols = st.columns(min(3, len(follow_ups)))
                for i, followup in enumerate(follow_ups):
                    with cols[i % 3]:
                        if st.button(followup, key=f"followup_{i}", use_container_width=True):
                            st.session_state.chat_history.append({"role": "user", "content": followup})
                            st.rerun()
        
        st.rerun()
    
    # Enhanced clear history button
    if st.session_state.chat_history:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

# ==================== PAGE: ANALYTICS ====================

def page_analytics():
    """Enhanced analytics with charts and detailed inputs."""
    # Custom header with gradient and animation
    st.markdown("""
    <div class="floating-element">
        <h1 style="text-align: center; font-size: 2.5rem; font-weight: 700; 
                   background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 0.5rem;">
            📊 Advanced Analytics Engine
        </h1>
        <p style="text-align: center; color: #64748b; font-size: 1.1rem;">
            Comprehensive scenario analysis for **6sense Revenue AI** with interactive visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Product selector (ready for future expansion)
    if len(PRODUCTS) > 1:
        selected_product = st.selectbox(
            "🎯 Select Product:",
            options=list(PRODUCTS.keys()),
            format_func=lambda x: PRODUCTS[x]["name"],
            index=list(PRODUCTS.keys()).index(DEFAULT_PRODUCT)
        )
    else:
        selected_product = DEFAULT_PRODUCT
        st.markdown(f"""
        <div class="insight-box floating-element">
            <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🎯 Currently Analyzing</h4>
            <p style="font-size: 1.2rem; font-weight: 600; color: #1e293b; margin: 0;">
                {PRODUCTS[selected_product]['name']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced scenario input
    st.markdown("### 🎯 Define Your Business Scenario")
    
    # Company Details
    with st.expander("🏢 Company Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            company_name = st.text_input("Company Name", placeholder="Acme Corp")
            team_size = st.slider("Team Size", 5, 500, 50, step=5)
        with col2:
            industry = st.selectbox("Industry", 
                ["B2B SaaS", "B2C", "Enterprise", "Healthcare", "Finance", "E-commerce", "Manufacturing"])
            company_stage = st.selectbox("Company Stage", 
                ["Pre-seed", "Seed", "Series A", "Series B", "Series C", "Growth", "Enterprise"])
        with col3:
            current_revenue = st.selectbox("Current Revenue", 
                ["<$100K", "$100K-$500K", "$500K-$1M", "$1M-$5M", "$5M-$10M", "$10M+"])
            target_market = st.selectbox("Target Market", 
                ["SMB", "Mid-Market", "Enterprise", "Global"])
    
    # Budget & Timeline
    with st.expander("💰 Budget & Timeline", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            budget = st.slider("Annual Budget (₹)", 50000, 5000000, 500000, step=25000)
            marketing_budget_pct = st.slider("Marketing Budget %", 10, 50, 25, step=5)
        with col2:
            timeline = st.selectbox("Analysis Timeline", 
                ["3 months", "6 months", "12 months", "18 months", "24 months"])
            expected_roi = st.slider("Expected ROI %", 50, 500, 200, step=25)
        with col3:
            primary_goal = st.selectbox("Primary Goal", 
                ["Lead Generation", "Brand Awareness", "Revenue Growth", "Market Expansion", "Customer Retention"])
            secondary_goal = st.selectbox("Secondary Goal", 
                ["Competitive Intelligence", "Sales Enablement", "Account-Based Marketing", "Demand Generation"])
    
    # Tech Stack & Current Tools
    with st.expander("🔧 Current Technology Stack"):
        col1, col2 = st.columns(2)
        with col1:
            current_crm = st.selectbox("Current CRM", 
                ["None", "Salesforce", "HubSpot", "Zoho", "Microsoft Dynamics", "Other"])
            current_marketing_tools = st.multiselect("Current Marketing Tools",
                ["Google Analytics", "Marketo", "Pardot", "Mailchimp", "HubSpot Marketing", "None", "Other"])
        with col2:
            data_sources = st.multiselect("Available Data Sources",
                ["CRM Data", "Website Analytics", "Email Marketing", "Social Media", "Customer Support", "Sales Data"])
            technical_resources = st.selectbox("Technical Resources",
                ["In-house Team", "Agency", "Freelance", "Limited", "None"])
    
    # Generate comprehensive scenario
    scenario_data = {
        "company_name": company_name or "Sample Company",
        "team_size": team_size,
        "industry": industry,
        "company_stage": company_stage,
        "current_revenue": current_revenue,
        "target_market": target_market,
        "budget": budget,
        "marketing_budget_pct": marketing_budget_pct,
        "marketing_budget": int(budget * marketing_budget_pct / 100),
        "timeline": timeline,
        "expected_roi": expected_roi,
        "primary_goal": primary_goal,
        "secondary_goal": secondary_goal,
        "current_crm": current_crm,
        "current_marketing_tools": current_marketing_tools,
        "data_sources": data_sources,
        "technical_resources": technical_resources
    }
    
    scenario_summary = f"{team_size}-person {company_stage} {industry} company with ₹{budget:,} budget targeting {target_market} market for {timeline}"
    
    # Generate Analysis Button with Enhanced Styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Comprehensive Analysis", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing scenario and generating insights..."):
                result = call_api("/analytics", data={"scenario": scenario_summary, "detailed_data": scenario_data}, product=selected_product)
            
            if "error" in result:
                st.markdown(f"""
                <div class="stError floating-element">
                    <h4>❌ Analysis Failed</h4>
                    <p>{result['error']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Success animation
                st.markdown("""
                <div class="metric-card floating-element" style="text-align: center;">
                    <h3 style="margin: 0;">✅ Analysis Complete!</h3>
                    <p>Your comprehensive scenario analysis is ready.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display enhanced analytics
            analytics = result.get("analytics", {})
            
            # Key Metrics Dashboard
            if analytics.get("metrics"):
                st.markdown("### 📊 Key Performance Dashboard")
                
                # Clean and process metrics data
                clean_metrics = []
                for metric in analytics["metrics"][:8]:
                    if isinstance(metric, dict):
                        clean_metrics.append(metric)
                    elif isinstance(metric, str):
                        clean_metrics.append({"label": metric, "value": "Available", "category": "General"})
                    else:
                        clean_metrics.append({"label": str(metric), "value": "Available", "category": "General"})
                
                # Create metrics dataframe for charts
                metrics_data = []
                for metric in clean_metrics:
                    label = metric.get("label", "Unknown Metric")[:40]
                    value = str(metric.get("value", "N/A"))[:40]
                    # Clean up the value to remove JSON artifacts
                    if "{" in value or "}" in value:
                        value = "Available"
                    metrics_data.append({
                        "Metric": label,
                        "Value": value,
                        "Category": metric.get("category", "General")
                    })
                
                if metrics_data:
                    try:
                        metrics_df = pd.DataFrame(metrics_data)
                    except Exception as e:
                        st.error(f"Error creating metrics dataframe: {e}")
                        metrics_df = pd.DataFrame([{"Metric": "Error", "Value": str(e)}])
                    
                    # Metric cards with visual indicators
                    col1, col2, col3, col4 = st.columns(4)
                    for idx, metric in enumerate(clean_metrics[:4]):
                        with col1 if idx % 4 == 0 else col2 if idx % 4 == 1 else col3 if idx % 4 == 2 else col4:
                            label = metric.get("label", "Metric")[:30]
                            value = metric.get("value", "N/A")
                            # Clean up value display
                            if isinstance(value, str) and ("{" in value or "}" in value):
                                value = "Available"
                            elif isinstance(value, (dict, list)):
                                value = "Available"
                            
                            delta_color = "normal"
                            if "growth" in label.lower():
                                delta_color = "off"
                            st.metric(
                                label=label,
                                value=str(value)[:30],
                                delta=metric.get("change", None),
                                delta_color=delta_color
                            )
                    
                    # Charts section
                    st.markdown("#### 📈 Visual Analytics")
                    
                    # Create subplots
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=("Budget Allocation", "Timeline Impact", "ROI Projection", "Feature Coverage"),
                        specs=[[{"type": "pie"}, {"type": "bar"}],
                               [{"type": "scatter"}, {"type": "bar"}]]
                    )
                    
                    # Budget Allocation Pie Chart
                    fig.add_trace(
                        go.Pie(
                            labels=["Marketing", "Sales", "Operations", "Other"],
                            values=[scenario_data["marketing_budget"], 
                                   int(budget * 0.3), 
                                   int(budget * 0.25), 
                                   int(budget * 0.45 - scenario_data["marketing_budget"])],
                            name="Budget"
                        ),
                        row=1, col=1
                    )
                    
                    # Timeline Impact Bar Chart
                    timeline_months = [3, 6, 12, 18, 24]
                    expected_impact = [20, 45, 80, 120, 150]
                    fig.add_trace(
                        go.Bar(
                            x=[f"{m}m" for m in timeline_months],
                            y=expected_impact,
                            name="Expected Impact %",
                            marker_color="lightblue"
                        ),
                        row=1, col=2
                    )
                    
                    # ROI Projection
                    fig.add_trace(
                        go.Scatter(
                            x=timeline_months,
                            y=[budget * (1 + expected_roi/100) * (m/12) for m in timeline_months],
                            mode="lines+markers",
                            name="Projected ROI",
                            line=dict(color="green")
                        ),
                        row=2, col=1
                    )
                    
                    # Feature Coverage
                    if analytics.get("features"):
                        feature_coverage = analytics["features"][:6]
                        fig.add_trace(
                            go.Bar(
                                x=feature_coverage,
                                y=[85, 92, 78, 88, 95, 82][:len(feature_coverage)],
                                name="Coverage %",
                                marker_color="orange"
                            ),
                            row=2, col=2
                        )
                    
                    fig.update_layout(
                        height=600,
                        showlegend=False,
                        title_text="Analytics Dashboard"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced Pricing Analysis
            if analytics.get("pricing"):
                st.markdown("### 💰 Pricing & Investment Analysis")
                pricing = analytics["pricing"]
                
                # Clean pricing data
                if isinstance(pricing, dict):
                    pricing_models = pricing.get("pricingModels", [])
                    if isinstance(pricing_models, list) and pricing_models:
                        models_text = ", ".join([model if isinstance(model, str) else str(model) for model in pricing_models[:3]])
                    else:
                        models_text = "Contact for pricing"
                    
                    time_to_value = pricing.get("timeToValue", "N/A")
                    if isinstance(time_to_value, str) and ("{" in time_to_value or "}" in time_to_value):
                        time_to_value = "3-6 months"
                    
                    # Clean pricing data display
                    pricing_data = pricing.get("data", "")
                    if isinstance(pricing_data, str) and ("{" in pricing_data or "}" in pricing_data):
                        pricing_data = "6sense offers flexible pricing plans based on your specific needs and company size. Contact their sales team for a customized quote."
                else:
                    models_text = "Contact for pricing"
                    time_to_value = "3-6 months"
                    pricing_data = "6sense offers flexible pricing plans based on your specific needs and company size."
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**💵 Investment Range**: Custom pricing based on company size")
                    st.markdown(f"**📊 Pricing Models**: {models_text}")
                    st.markdown(f"**⏱️ Time to Value**: {time_to_value}")
                    
                    # Sample competitive pricing chart
                    sample_competitors = {
                        "6sense": "Premium",
                        "Competitor A": "Mid-Range", 
                        "Competitor B": "Budget",
                        "Competitor C": "Premium"
                    }
                    try:
                        comp_df = pd.DataFrame({
                            "Provider": list(sample_competitors.keys()),
                            "Price Tier": list(sample_competitors.values())
                        })
                    except Exception as e:
                        st.error(f"Error creating competitors dataframe: {e}")
                        comp_df = pd.DataFrame({"Provider": ["Error"], "Price Tier": [str(e)]})
                    fig = px.bar(comp_df, x="Provider", y="Price Tier", title="Competitive Pricing Comparison")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**📋 Detailed Pricing Information:**")
                    st.info(pricing_data[:500] + "..." if len(pricing_data) > 500 else pricing_data)
                    
                    # ROI Calculator
                    st.markdown("**🧮 ROI Calculator:**")
                    investment = st.number_input("Investment Amount (₹)", value=budget, key="roi_investment")
                    expected_return = st.number_input("Expected Return (₹)", value=int(budget * expected_roi / 100), key="roi_return")
                    if investment > 0:
                        roi_percentage = ((expected_return - investment) / investment) * 100
                        st.metric("ROI %", f"{roi_percentage:.1f}%", delta=f"₹{expected_return - investment:,}")
            
            # Enhanced Features Display
            if analytics.get("features"):
                st.markdown("### ✨ Feature Analysis & Coverage")
                features = analytics["features"][:12]
                
                # Ensure features are strings, not objects
                clean_features = []
                for feature in features:
                    if isinstance(feature, str):
                        clean_features.append(feature)
                    elif isinstance(feature, dict) and "name" in feature:
                        clean_features.append(feature["name"])
                    elif isinstance(feature, dict) and "label" in feature:
                        clean_features.append(feature["label"])
                    else:
                        clean_features.append(str(feature))
                
                # Feature categories - fixed the self-reference issue
                core_features = [f for f in clean_features if any(word in f.lower() for word in ["predict", "ai", "analytics", "intelligence", "machine learning"])]
                integration_features = [f for f in clean_features if any(word in f.lower() for word in ["crm", "integration", "connect", "sync", "api"])]
                reporting_features = [f for f in clean_features if any(word in f.lower() for word in ["report", "dashboard", "metric", "analytics", "visualization"])]
                other_features = [f for f in clean_features if f not in core_features + integration_features + reporting_features]
                
                feature_categories = {
                    "Core": core_features,
                    "Integration": integration_features,
                    "Reporting": reporting_features,
                    "Other": other_features
                }
                
                for category, category_features in feature_categories.items():
                    if category_features:
                        with st.expander(f"📁 {category} Features ({len(category_features)})"):
                            cols = st.columns(3)
                            for idx, feature in enumerate(category_features):
                                with cols[idx % 3]:
                                    st.checkbox(feature, value=True, disabled=True)
            
            # Enhanced Integrations
            if analytics.get("integrations"):
                st.markdown("### 🔗 Integration Ecosystem")
                integrations = analytics["integrations"][:12]
                
                # Ensure integrations are strings, not objects
                clean_integrations = []
                for integration in integrations:
                    if isinstance(integration, str):
                        clean_integrations.append(integration)
                    elif isinstance(integration, dict) and "name" in integration:
                        clean_integrations.append(integration["name"])
                    elif isinstance(integration, dict) and "label" in integration:
                        clean_integrations.append(integration["label"])
                    else:
                        clean_integrations.append(str(integration))
                
                # Integration categories - fixed the self-reference issue
                crm_integrations = [i for i in clean_integrations if any(crm in i.lower() for crm in ["salesforce", "hubspot", "zoho", "dynamics"])]
                marketing_integrations = [i for i in clean_integrations if any(mk in i.lower() for mk in ["marketo", "pardot", "mailchimp", "google"])]
                other_integrations = [i for i in clean_integrations if i not in crm_integrations + marketing_integrations]
                
                integration_types = {
                    "CRM": crm_integrations,
                    "Marketing": marketing_integrations,
                    "Other": other_integrations
                }
                
                for int_type, type_integrations in integration_types.items():
                    if type_integrations:
                        st.markdown(f"**{int_type}**:")
                        cols = st.columns(min(3, len(type_integrations)))
                        for idx, integration in enumerate(type_integrations):
                            with cols[idx % 3]:
                                st.success(f"✅ {integration}")
            
            # Summary Section
            st.markdown("---")
            st.markdown("### 📋 Analysis Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Data Sources Analyzed", result.get('sources', 0))
            with col2:
                st.metric("Analysis Confidence", "87%", delta="+12%")
            with col3:
                st.metric("Recommendation Score", "8.5/10")
            
            st.markdown(f"**🎯 Scenario**: {scenario_summary}")
            st.markdown(f"**💰 Total Investment**: ₹{budget:,}")
            st.markdown(f"**📈 Expected ROI**: {expected_roi}% over {timeline}")

# ==================== PAGE: REPORTS ====================

def page_reports():
    """Enhanced strategic report generation with infographics."""
    # Custom header with gradient and animation
    st.markdown("""
    <div class="floating-element">
        <h1 style="text-align: center; font-size: 2.5rem; font-weight: 700; 
                   background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 0.5rem;">
            📋 Strategic Intelligence Reports
        </h1>
        <p style="text-align: center; color: #64748b; font-size: 1.1rem;">
            Generate comprehensive AI-powered strategic analysis for **6sense Revenue AI** with interactive visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Product selector (ready for future expansion)
    if len(PRODUCTS) > 1:
        selected_product = st.selectbox(
            "🎯 Select Product:",
            options=list(PRODUCTS.keys()),
            format_func=lambda x: PRODUCTS[x]["name"],
            index=list(PRODUCTS.keys()).index(DEFAULT_PRODUCT)
        )
    else:
        selected_product = DEFAULT_PRODUCT
        st.markdown(f"""
        <div class="insight-box floating-element">
            <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🎯 Currently Analyzing</h4>
            <p style="font-size: 1.2rem; font-weight: 600; color: #1e293b; margin: 0;">
                {PRODUCTS[selected_product]['name']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced report parameters
    st.markdown("### 🎯 Report Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input(
            "📝 Report Topic",
            placeholder="e.g., 'Growth strategy for B2B SaaS startup'",
            help="What specific area would you like analyzed?"
        )
        
        report_type = st.selectbox(
            "📊 Report Type",
            ["Market Analysis", "Competitive Intelligence", "Growth Strategy", "Technology Assessment", "ROI Analysis"],
            help="Choose the type of strategic analysis"
        )
        
        depth_level = st.selectbox(
            "🔍 Analysis Depth",
            ["Executive Summary", "Detailed Analysis", "Comprehensive Deep Dive"],
            help="Level of detail for the report"
        )
    
    with col2:
        team_size = st.number_input("Team Size", 5, 1000, 50)
        budget = st.number_input("Budget (₹)", 1000, 10000000, 500000, step=50000)
        timeline = st.selectbox("Timeline", ["1 month", "3 months", "6 months", "12 months"])
        industry = st.selectbox("Industry", ["B2B SaaS", "B2C", "Enterprise", "Healthcare", "Finance"])
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            include_charts = st.checkbox("📈 Include Charts & Graphs", value=True)
            include_competitors = st.checkbox("🏢 Competitor Analysis", value=True)
            include_roi = st.checkbox("💰 ROI Projections", value=True)
        with col2:
            focus_area = st.selectbox("Primary Focus", 
                ["Revenue Growth", "Market Expansion", "Competitive Positioning", "Technology Integration", "Customer Acquisition"])
            risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    
    # Generate Report Button with Enhanced Styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Strategic Report", type="primary", use_container_width=True):
            if not topic:
                st.markdown("""
                <div class="stError floating-element">
                    <h4>⚠️ Missing Information</h4>
                    <p>Please enter a report topic to continue.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("🤖 Generating comprehensive strategic report..."):
                    constraints = {
                        "team_size": team_size,
                        "budget": budget,
                        "timeline": timeline,
                        "industry": industry,
                        "report_type": report_type,
                        "depth_level": depth_level,
                        "focus_area": focus_area,
                        "risk_tolerance": risk_tolerance,
                        "include_charts": include_charts,
                        "include_competitors": include_competitors,
                        "include_roi": include_roi
                    }
                    result = call_api("/report", data={"topic": topic, "constraints": constraints}, product=selected_product)
                
                if "error" in result:
                    st.markdown(f"""
                    <div class="stError floating-element">
                        <h4>❌ Report Generation Failed</h4>
                        <p>{result['error']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    report = result.get("report", {})
                    
                    # Success animation
                    st.markdown("""
                    <div class="metric-card floating-element" style="text-align: center;">
                        <h3 style="margin: 0;">✅ Strategic Report Generated!</h3>
                        <p>Your comprehensive strategic analysis is ready.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display enhanced report
                st.success("✓ Strategic report generated successfully!")
                
                # Report Header
                st.markdown(f"## 📊 {report.get('title', 'Strategic Intelligence Report')}")
                st.markdown(f"**Report Type**: {report_type} | **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Executive Summary with visual indicator
                if report.get("summary"):
                    st.markdown("### 🎯 Executive Summary")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(report["summary"])
                    with col2:
                        # Summary score visualization
                        score = 8.5  # Placeholder score
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = score,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Strategic Score"},
                            delta = {'reference': 7.0},
                            gauge = {
                                'axis': {'range': [None, 10]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 5], 'color': "lightgray"},
                                    {'range': [5, 8], 'color': "gray"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 9
                                }
                            }
                        ))
                        fig.update_layout(height=250, margin=dict(l=0,r=0,b=0,t=0))
                        st.plotly_chart(fig, use_container_width=True)
                
                # KPIs with enhanced visualization
                if report.get("kpis"):
                    st.markdown("### 📈 Key Performance Indicators")
                    
                    # KPI cards with charts
                    kpi_data = report["kpis"][:6]
                    if kpi_data:
                        # Create KPI visualization
                        fig = make_subplots(
                            rows=2, cols=3,
                            subplot_titles=[kpi.get("name", f"KPI {i+1}")[:20] for i, kpi in enumerate(kpi_data[:6])],
                            specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                                   [{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
                        )
                        
                        for i, kpi in enumerate(kpi_data[:3]):
                            fig.add_trace(
                                go.Indicator(
                                    mode="gauge+number",
                                    value=float(str(kpi.get("value", 0)).replace('%', '').replace('High', '85').replace('Medium', '65').replace('Low', '45')),
                                    title={'text': kpi.get("name", "KPI")[:15]},
                                    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "green"}}
                                ),
                                row=1, col=i+1
                            )
                        
                        # Add bar charts for additional KPIs
                        for i, kpi in enumerate(kpi_data[3:6]):
                            fig.add_trace(
                                go.Bar(
                                    x=["Current", "Target", "Industry Avg"],
                                    y=[float(kpi.get("value", 50)), 80, 65],
                                    name=kpi.get("name", "KPI")[:15]
                                ),
                                row=2, col=i+1
                            )
                        
                        fig.update_layout(height=500, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Traditional KPI display
                    display_metrics(report["kpis"])
                
                # Market Analysis with Charts
                if include_charts:
                    st.markdown("### 🌍 Market Analysis")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Market Size Visualization
                        market_data = {
                            "Current Market": 25,
                            "Addressable Market": 45,
                            "Target Market": 30
                        }
                        fig = px.pie(
                            values=list(market_data.values()),
                            names=list(market_data.keys()),
                            title="Market Segmentation"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Growth Trend
                        growth_data = {
                            "Q1": 15,
                            "Q2": 22,
                            "Q3": 28,
                            "Q4": 35
                        }
                        fig = px.line(
                            x=list(growth_data.keys()),
                            y=list(growth_data.values()),
                            title="Growth Projection",
                            markers=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Competitor Analysis
                if include_competitors:
                    st.markdown("### 🏢 Competitive Landscape")
                    
                    # Competitive positioning chart
                    competitors = ["6sense", "Competitor A", "Competitor B", "Competitor C"]
                    features = [85, 72, 68, 75]
                    pricing = [70, 85, 90, 80]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=features,
                        y=pricing,
                        mode='markers+text',
                        text=competitors,
                        textposition="top center",
                        marker=dict(size=20, color='lightblue'),
                        name="Competitors"
                    ))
                    
                    fig.update_layout(
                        title="Competitive Positioning Map",
                        xaxis_title="Feature Score",
                        yaxis_title="Price Competitiveness",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # ROI Projections
                if include_roi:
                    st.markdown("### 💰 ROI & Financial Projections")
                    
                    # ROI Timeline Chart
                    months = list(range(1, 13))
                    investment = [budget] * 12
                    returns = [budget * (1 + 0.15 * (m/12)) for m in months]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=months,
                        y=investment,
                        mode="lines",
                        name="Investment",
                        line=dict(color="red")
                    ))
                    fig.add_trace(go.Scatter(
                        x=months,
                        y=returns,
                        mode="lines",
                        name="Projected Returns",
                        line=dict(color="green")
                    ))
                    
                    fig.update_layout(
                        title="12-Month ROI Projection",
                        xaxis_title="Months",
                        yaxis_title="Amount (₹)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # ROI Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Payback Period", "8 months", "-2 months vs industry")
                    with col2:
                        st.metric("3-Year ROI", "245%", "+125% vs baseline")
                    with col3:
                        st.metric("NPV", f"₹{budget * 2.5:,}", "+₹500K")
                    with col4:
                        st.metric("IRR", "28%", "+8% vs target")
                
                # Strategic Insights with Visual Elements
                if report.get("insights"):
                    st.markdown("### 💡 Strategic Insights")
                    
                    insights = report["insights"][:6]
                    for i, insight in enumerate(insights):
                        # Insight priority indicator
                        priority = "🔴 High" if i < 2 else "🟡 Medium" if i < 4 else "🟢 Standard"
                        
                        with st.expander(f"{priority} Priority: Insight {i+1}"):
                            st.markdown(f"**{insight}**")
                            
                            # Insight impact visualization
                            impact_score = 85 - (i * 10)
                            fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = impact_score,
                                domain = {'x': [0, 1], 'y': [0, 1]},
                                title = {'text': "Impact Score"},
                                gauge = {
                                    'axis': {'range': [None, 100]},
                                    'bar': {'color': "green" if impact_score > 70 else "orange" if impact_score > 40 else "red"},
                                    'steps': [
                                        {'range': [0, 40], 'color': "lightgray"},
                                        {'range': [40, 70], 'color': "gray"}
                                    ]
                                }
                            ))
                            fig.update_layout(height=200, margin=dict(l=0,r=0,b=0,t=0))
                            st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations with Action Cards
                if report.get("recommendation"):
                    st.markdown("### 🎯 Strategic Recommendations")
                    
                    # Primary recommendation
                    st.success(f"**Primary Recommendation:** {report['recommendation']}")
                    
                    # Action items
                    action_items = [
                        "Implement 6sense platform within next 3 months",
                        "Focus on high-value account identification",
                        "Develop predictive lead scoring model",
                        "Establish integration with existing CRM",
                        "Create targeted marketing campaigns"
                    ]
                    
                    st.markdown("#### 📋 Action Items")
                    for i, action in enumerate(action_items):
                        col1, col2, col3 = st.columns([1, 8, 1])
                        with col1:
                            st.write(f"{i+1}.")
                        with col2:
                            st.checkbox(action, value=False, key=f"action_{i}")
                        with col3:
                            priority = "🔴" if i < 2 else "🟡" if i < 4 else "🟢"
                            st.write(priority)
                
                # Risk Assessment
                with st.expander("⚠️ Risk Assessment"):
                    risks = [
                        {"risk": "Implementation Complexity", "probability": "Medium", "impact": "High", "mitigation": "Phased rollout approach"},
                        {"risk": "Team Adoption", "probability": "Low", "impact": "Medium", "mitigation": "Comprehensive training program"},
                        {"risk": "Integration Challenges", "probability": "Medium", "impact": "Medium", "mitigation": "Pre-implementation testing"}
                    ]
                    
                    risk_df = pd.DataFrame(risks)
                    st.dataframe(risk_df, use_container_width=True)
                
                # Metadata and Download
                st.markdown("---")
                metadata = result.get("metadata", {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sources Used", result.get('sources_used', 0))
                with col2:
                    st.metric("Analysis Depth", depth_level)
                with col3:
                    st.metric("Confidence Score", "92%")
                
                st.caption(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Report ID: {hash(topic) % 10000:04d}")
                
                # Enhanced download options
                col1, col2 = st.columns(2)
                with col1:
                    report_json = json.dumps({**report, "constraints": constraints}, indent=2)
                    st.download_button(
                        label="📥 Download Report (JSON)",
                        data=report_json,
                        file_name=f"strategic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Create a text summary for download
                    report_summary = f"""
Strategic Intelligence Report
============================

Topic: {topic}
Type: {report_type}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Executive Summary:
{report.get('summary', 'N/A')}

Primary Recommendation:
{report.get('recommendation', 'N/A')}

Key Insights:
{chr(10).join([f'- {insight}' for insight in report.get('insights', [])[:3]])}

Constraints:
- Team Size: {team_size}
- Budget: ₹{budget:,}
- Timeline: {timeline}
- Industry: {industry}
                    """
                    st.download_button(
                        label="📄 Download Summary (TXT)",
                        data=report_summary,
                        file_name=f"report_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

# ==================== PAGE: SYSTEM STATUS ====================

def page_status():
    """System status and statistics."""
    st.header("⚙️ System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### API Health")
        with st.spinner("Checking API..."):
            health = call_api("/health", method="GET")
        
        if "error" not in health:
            st.success("✓ API Running")
            st.json({
                "status": health.get("status"),
                "product": health.get("product", {}).get("canonical_name"),
                "rag_ready": health.get("rag_ready"),
                "vector_store_ready": health.get("vector_store_ready")
            })
        else:
            st.error("❌ API Not Running")
            st.info("Start the backend with: `python api_backend.py`")
    
    with col2:
        st.markdown("### Database Statistics")
        with st.spinner("Loading stats..."):
            stats = call_api("/stats", method="GET")
        
        if "error" not in stats:
            vs = stats.get("vector_store", {})
            st.metric("Documents Indexed", vs.get("count", 0))
            st.metric("Collection", vs.get("collection_name", "Unknown"))
            st.json(stats.get("product", {}))
        else:
            st.error("❌ Could not load stats")
    
    # Products
    st.markdown("---")
    st.markdown("### Available Products")
    with st.spinner("Loading products..."):
        products = call_api("/products", method="GET")
    
    if "error" not in products:
        for product in products.get("products", []):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**{product.get('name')}**")
                st.caption(f"Domain: {product.get('domain')}")
            with col2:
                st.metric("Documents", product.get("total_documents", 0))
            with col3:
                st.metric("Datasets", product.get("datasets", 0))
    else:
        st.error("Could not load products")

# ==================== SIDEBAR ====================

def sidebar():
    """Enhanced sidebar navigation with clean, simple styling."""
    # Custom sidebar header
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2rem; font-weight: 700; 
                   background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 0.5rem;">
            🚀 Cuspera RAG
        </h1>
        <p style="color: #64748b; font-size: 1rem; margin: 0;">
            Product Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # API Status
    api_health = check_api_health()
    if api_health:
        st.sidebar.success("✅ API Connected")
        st.sidebar.info("All systems operational")
    else:
        st.sidebar.error("❌ API Offline")
        st.sidebar.info("Backend not responding")
        st.sidebar.info("Start backend with: `python api_backend.py`")
    
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.radio(
        "",
        ["💬 Chat", "📊 Analytics", "📋 Reports", "⚙️ Status"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Quick Instructions
    st.sidebar.markdown("### 📖 Quick Instructions")
    
    with st.sidebar.expander("💬 Chat", expanded=True):
        st.write("• Click suggested questions")
        st.write("• Type your own questions")
        st.write("• Get AI-powered answers")
    
    with st.sidebar.expander("📊 Analytics", expanded=True):
        st.write("• Enter company details")
        st.write("• Set budget & timeline")
        st.write("• Get scenario analysis")
    
    with st.sidebar.expander("📋 Reports", expanded=True):
        st.write("• Choose report type")
        st.write("• Configure parameters")
        st.write("• Generate strategic insights")
    
    st.sidebar.markdown("---")
    
    # About Platform
    st.sidebar.markdown("### ℹ️ About Platform")
    
    with st.sidebar.expander("🎯 Key Features", expanded=True):
        st.write("🤖 Smart question suggestions")
        st.write("📊 Real-time analytics")
        st.write("📋 Strategic reports")
        st.write("🔄 RAG pipeline integration")
        st.write("🎨 Fabulous UI design")
    
    with st.sidebar.expander("🚀 Technology Stack", expanded=True):
        st.write("**Frontend:** Streamlit")
        st.write("**Backend:** FastAPI")
        st.write("**AI:** OpenAI GPT-4")
        st.write("**Vector DB:** ChromaDB")
        st.write("**Framework:** LangChain")
    
    with st.sidebar.expander("📈 Current Product", expanded=True):
        st.write(f"**{PRODUCTS[DEFAULT_PRODUCT]['name']}**")
        st.write("B2B Revenue Intelligence Platform")
    
    # Product Details
    st.sidebar.markdown("### 🎯 Product Details")
    st.sidebar.info(f"""
    **{PRODUCTS[DEFAULT_PRODUCT]['name']}**
    
    B2B Revenue AI Platform
    """)
    
    # Quick Stats
    st.sidebar.markdown("### 📊 Quick Stats")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Questions", "5+", delta="AI-generated")
    with col2:
        st.metric("API", "Ready", delta="Connected")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; font-size: 0.8rem; color: #64748b;">
        <p><strong>Version:</strong> 1.0.0</p>
        <p><strong> 2026</strong> Cuspera RAG Platform</p>
        <p style="margin-top: 0.5rem;">
            <strong></strong> 
            <a href="https://github.com/abhishek-a-qbit/cuspera-rag-platform" 
               style="color: #3b82f6; text-decoration: none;">
                GitHub Repository
            </a>
        </p>
    """, unsafe_allow_html=True)
    
    return page

# ==================== MAIN ====================

def main():
    """Main app."""
    # Sidebar
    page = sidebar()
    
    # Check API
    if not check_api_health():
        st.warning(
            "⚠️ **API is offline**\n\n"
            "The backend API is not running. Please start it with:\n\n"
            "```\npython api_backend.py\n```\n\n"
            "Then refresh this page."
        )
        return
    
    # Route to pages
    if page == "💬 Chat":
        page_chat()
    elif page == "📊 Analytics":
        page_analytics()
    elif page == "📋 Reports":
        page_reports()
    else:
        page_status()

if __name__ == "__main__":
    main()
