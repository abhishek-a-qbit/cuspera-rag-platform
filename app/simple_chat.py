"""
Simple Chat Interface for 6sense AI Agent
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
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
    }
    .user-message {
        background: #4CAF50;
        color: white;
        margin-left: auto;
    }
    .agent-message {
        background: #2196F3;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Header
st.title("🚀 6sense AI Agent")
st.markdown("Your Intelligent Revenue Intelligence Assistant")

# Quick actions
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Analytics"):
        st.session_state.query = "Generate a comprehensive analytics report for 6sense performance"
with col2:
    if st.button("💰 ROI Calculator"):
        st.session_state.query = "Calculate the ROI for implementing 6sense Revenue AI platform"
with col3:
    if st.button("📈 Dashboard"):
        st.session_state.query = "Create an interactive dashboard showing 6sense metrics"
with col4:
    if st.button("🎨 Infographic"):
        st.session_state.query = "Generate an infographic showing 6sense impact"

# Chat container
chat_container = st.container()

with chat_container:
    # Display messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message agent-message">{message["content"]}</div>', unsafe_allow_html=True)
            
            # Show sources if available
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message["sources"][:3]):
                        st.write(f"**Source {i+1}:**")
                        if isinstance(source, dict):
                            st.write(f"Content: {source.get('content', '')[:200]}...")
                        else:
                            st.write(f"Content: {str(source)[:200]}...")
            
            # Show metrics if available
            if "metrics" in message and message["metrics"]:
                with st.expander("📊 Metrics"):
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

# Input
user_input = st.text_input(
    "Ask me anything about 6sense...",
    value=st.session_state.get("query", ""),
    key="input"
)

# Clear query after using
if "query" in st.session_state:
    del st.session_state.query

col1, col2 = st.columns([4, 1])
with col1:
    send_button = st.button("🚀 Send", type="primary")
with col2:
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()

# Handle message
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response
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
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": agent_response,
                "sources": sources,
                "metrics": metrics
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
st.markdown("*🚀 Powered by 6sense Revenue AI*")
