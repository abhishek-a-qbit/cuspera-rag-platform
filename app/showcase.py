"""
6sense AI Agent Showcase
Beautiful single-page interface with comprehensive capabilities
"""

import streamlit as st
import requests
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="6sense AI Agent",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .header {
        text-align: center;
        color: white;
        padding: 2rem;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
    }
    .user-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        margin-left: auto;
    }
    .agent-message {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
    }
    .metric-display {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Header
st.markdown("""
<div class="header">
    <h1>🚀 6sense AI Agent</h1>
    <p>Your Intelligent Revenue Intelligence Assistant</p>
    <p>✨ Analytics | 💰 ROI Calculator | 📈 Dashboard | 🎨 Infographics | 🤖 AI Chat</p>
</div>
""", unsafe_allow_html=True)

# Feature showcase
st.markdown("### 🎯 Quick Actions", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Analytics Report", use_container_width=True):
        st.session_state.query = "Generate analytics report"

with col2:
    if st.button("💰 Calculate ROI", use_container_width=True):
        st.session_state.query = "Calculate ROI for 6sense"

with col3:
    if st.button("📈 Create Dashboard", use_container_width=True):
        st.session_state.query = "Create dashboard showing 6sense metrics"

with col4:
    if st.button("🎨 Generate Infographic", use_container_width=True):
        st.session_state.query = "Generate infographic showing 6sense impact"

# Chat interface
st.markdown("### 💬 Chat with AI Agent", unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message agent-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Display metrics if available
        if "metrics" in message and message["metrics"]:
            with st.expander("📊 Response Quality"):
                metrics = message["metrics"]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Quality Score", f"{metrics.get('overall_score', 0):.1%}")
                with col2:
                    st.metric("Tools Used", len(message.get("tools_used", [])))
                with col3:
                    st.metric("Sources", len(message.get("sources", [])))
                with col4:
                    st.metric("Session", st.session_state.session_id[:8])

# Input area
user_input = st.text_input(
    "Ask me anything about 6sense, analytics, ROI, or visualizations...",
    value=st.session_state.get("query", ""),
    key="input",
    placeholder="e.g., 'What are 6sense features?', 'Generate analytics', 'Calculate ROI'"
)

# Clear query after using
if "query" in st.session_state:
    del st.session_state.query

col1, col2 = st.columns([4, 1])
with col1:
    send_button = st.button("🚀 Send", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Handle message
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
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
            tools_used = result.get("tools_used", [])
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": agent_response,
                "sources": sources,
                "metrics": metrics,
                "tools_used": tools_used
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: Backend unavailable (Status: {response.status_code})"
            })
    
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Connection error: {str(e)}"
        })
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: white; opacity: 0.8;">
        <p>🚀 Powered by 6sense Revenue AI | Advanced Analytics & Intelligence Platform</p>
        <p>✨ Comprehensive AI Agent with Analytics, ROI Calculator, Dashboard Generation & More</p>
    </div>
    """,
    unsafe_allow_html=True
)
