"""
Working Chat Interface for Enhanced Cuspera
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Enhanced Cuspera - AI Agent",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Header
st.title("🚀 Enhanced Cuspera - AI Agent")
st.markdown("Your Intelligent Revenue Intelligence Assistant")

# Quick actions
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Analytics Report"):
        st.session_state.query = "Generate analytics report"
with col2:
    if st.button("💰 Calculate ROI"):
        st.session_state.query = "Calculate ROI for 6sense"
with col3:
    if st.button("📈 Create Dashboard"):
        st.session_state.query = "Create dashboard showing 6sense metrics"
with col4:
    if st.button("🎨 Generate Infographic"):
        st.session_state.query = "Generate infographic showing 6sense impact"

# Chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Agent:** {message['content']}")
        
        # Always show sources
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                for i, source in enumerate(message["sources"][:3]):
                    st.write(f"**Source {i+1}:**")
                    if isinstance(source, dict):
                        content = source.get("content", "")
                        metadata = source.get("metadata", {})
                        if content:
                            st.write(f"Content: {content[:200]}...")
                        if metadata:
                            st.write(f"Metadata: {metadata}")
                    else:
                        st.write(f"Content: {str(source)[:200]}...")
        
        # Always show metrics
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
    "Ask me anything about 6sense, analytics, ROI, or visualizations...",
    value=st.session_state.get("query", ""),
    key="input"
)

if "query" in st.session_state:
    del st.session_state.query

col1, col2 = st.columns([4, 1])
with col1:
    if st.button("🚀 Send", type="primary"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            try:
                response = requests.post(
                    "http://localhost:8001/advanced-chat",
                    json={"message": user_input, "session_id": st.session_state.session_id},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result.get("response", ""),
                        "sources": result.get("sources", []),
                        "metrics": result.get("metrics", {})
                    })
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: Backend unavailable"
                    })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Connection error: {str(e)}"
                })
            
            st.rerun()

with col2:
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*🚀 Powered by 6sense Revenue AI*")
