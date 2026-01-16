"""
Enhanced Chat Interface with Beautiful UI
Single-page application with comprehensive AI agent capabilities
"""

import streamlit as st
import requests
import json
from datetime import datetime
import base64
from typing import Dict, List, Any

# Set page configuration
st.set_page_config(
    page_title="6sense AI Agent - Revenue Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .agent-message {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0;
        max-width: 80%;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin: 20px 0;
    }
    
    .sub-header {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 5px;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .source-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Header
st.markdown('<h1 class="main-header">🚀 6sense AI Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Intelligent Revenue Intelligence Assistant</p>', unsafe_allow_html=True)

# Quick action buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Analytics", help="Generate analytics report", use_container_width=True):
        st.session_state.quick_action = "analytics"
with col2:
    if st.button("💰 ROI Calculator", help="Calculate ROI", use_container_width=True):
        st.session_state.quick_action = "roi"
with col3:
    if st.button("📈 Dashboard", help="Create dashboard", use_container_width=True):
        st.session_state.quick_action = "dashboard"
with col4:
    if st.button("🎨 Infographic", help="Generate infographic", use_container_width=True):
        st.session_state.quick_action = "infographic"

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.chat_messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Display sources if available
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources & References"):
                for i, source in enumerate(message["sources"][:3]):
                    st.markdown(f'<div class="source-card">', unsafe_allow_html=True)
                    st.markdown(f"**Source {i+1}**")
                    if isinstance(source, dict):
                        content = source.get("content", "")
                        metadata = source.get("metadata", {})
                        if content:
                            st.markdown(f"*Content Preview:* {content[:200]}...")
                        if metadata:
                            st.markdown(f"*Metadata:* {metadata}")
                    else:
                        st.markdown(f"*Content:* {str(source)[:200]}...")
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Display metrics if available
        if "metrics" in message and message["metrics"]:
            with st.expander("📊 Response Quality Metrics"):
                metrics = message["metrics"]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Coverage", f"{metrics.get('coverage_final', 0):.1%}")
                with col2:
                    st.metric("Specificity", f"{metrics.get('specificity_final', 0):.1%}")
                with col3:
                    st.metric("Insightfulness", f"{metrics.get('insightfulness_final', 0):.1%}")
                with col4:
                    st.metric("Groundedness", f"{metrics.get('groundedness_final', 0):.1%}")

st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Handle quick actions
user_input = ""
if hasattr(st.session_state, 'quick_action'):
    if st.session_state.quick_action == "analytics":
        user_input = "Generate a comprehensive analytics report for 6sense performance"
    elif st.session_state.quick_action == "roi":
        user_input = "Calculate the ROI for implementing 6sense Revenue AI platform"
    elif st.session_state.quick_action == "dashboard":
        user_input = "Create an interactive dashboard showing 6sense metrics and KPIs"
    elif st.session_state.quick_action == "infographic":
        user_input = "Generate an infographic showing 6sense impact and key statistics"
    
    del st.session_state.quick_action

# Text input
user_input = st.text_input(
    "Ask me anything about 6sense, analytics, ROI, or visualizations...",
    value=user_input,
    key="user_input",
    placeholder="e.g., 'Generate analytics report', 'Calculate ROI', 'Create dashboard', 'What are 6sense features?'"
)

col1, col2 = st.columns([4, 1])
with col1:
    send_button = st.button("🚀 Send", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Clear chat history
if clear_button:
    st.session_state.chat_messages = []
    st.rerun()

# Send message
if send_button and user_input:
    # Add user message
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Get response from agent
    try:
        response = requests.post(
            "http://localhost:8001/advanced-chat",
            json={
                "message": user_input,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            agent_response = result.get("response", "I'm having trouble processing your request.")
            sources = result.get("sources", [])
            metrics = result.get("metrics", {})
            
            # Add agent response
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": agent_response,
                "sources": sources,
                "metrics": metrics,
                "timestamp": datetime.now()
            })
        else:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"Error: Backend service unavailable (Status: {response.status_code})",
                "timestamp": datetime.now()
            })
    
    except requests.exceptions.RequestException as e:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"Connection error: Unable to reach the backend service. Please ensure the backend is running on localhost:8001",
            "timestamp": datetime.now()
        })
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: white; opacity: 0.7;">'
    '🚀 Powered by 6sense Revenue AI | Advanced Analytics & Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)
