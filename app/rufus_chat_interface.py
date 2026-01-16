"""
Amazon Rufus-style Chat Interface
Interactive question cards with rich context and metrics
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

# Import the advanced agent
try:
    import requests
    AGENT_AVAILABLE = True
    API_URL = "http://localhost:8001"
except ImportError as e:
    st.error(f"Requests not available: {e}")
    AGENT_AVAILABLE = False

def display_question_card(question_data: Dict, index: int) -> bool:
    """Display a simple question card using basic Streamlit components"""
    
    # Extract question data - handle both direct string and JSON structure
    question_raw = question_data.get("question", "")
    
    # If question is a JSON string, extract the actual question
    if isinstance(question_raw, str) and question_raw.startswith('{"questions":'):
        try:
            import json
            parsed = json.loads(question_raw)
            if "questions" in parsed and len(parsed["questions"]) > 0:
                question = parsed["questions"][0]
            else:
                question = question_raw
        except:
            question = question_raw
    else:
        question = question_raw
    
    # Clean up the question text
    question = str(question).strip().strip('"\'')
    
    metrics = question_data.get("metrics", {})
    answer_metrics = question_data.get("answer_metrics", {})
    sources = question_data.get("retrieved_sources", 0)
    
    # Calculate overall scores
    q_score = metrics.get("overall_score", 0) * 100
    a_score = answer_metrics.get("overall_score", 0) * 100
    
    # Simple Streamlit card
    with st.container():
        # Header with scores
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"🤔 Question {index}")
        with col2:
            st.markdown(f"🟢 Q: {q_score:.0f}% | 🔵 A: {a_score:.0f}%")
        
        # Question text
        st.write(question)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Sources", sources)
        with col2:
            st.metric("🎯 Coverage", f"{metrics.get('coverage_final', 0)*100:.0f}%")
        with col3:
            st.metric("📊 Specificity", f"{metrics.get('specificity_final', 0)*100:.0f}%")
        
        # Chat button
        if st.button(f"💬 Chat About This Question", key=f"chat_btn_{index}"):
            st.session_state.selected_question = index
            st.rerun()
        
        st.divider()
    
    return True

def display_agent_response(response_data: Dict, question_data: Dict):
    """Display simple agent response using basic Streamlit components"""
    
    response = response_data.get("response", "")
    sources = response_data.get("sources", [])
    metrics = response_data.get("metrics", {})
    
    # Response container
    st.subheader("🤖 AI Agent Response")
    
    # Response content
    st.write(response)
    
    # Sources section
    if sources:
        st.subheader("📚 Source Documents")
        for i, source in enumerate(sources[:5], 1):  # Show top 5 sources
            # Get actual content and metadata
            content = source.get("content", "")
            metadata = source.get("metadata", {})
            similarity_score = source.get("score", 0)
            
            # Extract key metadata fields
            doc_id = metadata.get("id", f"doc_{i}")
            content_type = metadata.get("content_type", "unknown")
            dataset = metadata.get("dataset", "unknown")
            source_file = metadata.get("source", "unknown")
            
            with st.expander(f"📄 Source {i} ({similarity_score:.1%} match)"):
                # Document metadata
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**📋 Document Info**")
                    st.write(f"**ID:** {doc_id}")
                    st.write(f"**Type:** {content_type}")
                    st.write(f"**Dataset:** {dataset}")
                    if source_file != "unknown":
                        st.write(f"**Source:** {source_file}")
                
                with col2:
                    st.write("**📊 Match Score**")
                    st.metric("Similarity", f"{similarity_score:.1%}")
                
                st.write("**📄 Content Preview:**")
                # Show first 300 characters of content
                preview = content[:300] + "..." if len(content) > 300 else content
                st.text_area("Content", value=preview, height=150, disabled=True, label_visibility="collapsed")
                
                # Show additional metadata if available
                if metadata:
                    with st.expander("🔍 Full Metadata"):
                        st.json(metadata)
    
    # Metrics section
    if metrics:
        st.subheader("📊 Response Quality Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Coverage", f"{metrics.get('coverage_final', 0)*100:.0f}%")
        with col2:
            st.metric("📊 Specificity", f"{metrics.get('specificity_final', 0)*100:.0f}%")
        with col3:
            st.metric("💡 Insightfulness", f"{metrics.get('insightfulness_final', 0)*100:.0f}%")
        with col4:
            st.metric("🔗 Groundedness", f"{metrics.get('groundedness_final', 0)*100:.0f}%")
    
    # Follow-up suggestions
    st.subheader("🔄 Follow-up Questions")
    follow_ups = [
        "Can you provide more details about this?",
        "What are the practical implications?",
        "How does this compare to alternatives?",
        "What evidence supports this conclusion?"
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(follow_ups[0], key=f"followup_1"):
            st.session_state.chat_input = follow_ups[0]
            st.rerun()
    with col2:
        if st.button(follow_ups[1], key=f"followup_2"):
            st.session_state.chat_input = follow_ups[1]
            st.rerun()
    
    st.divider()

def rufus_chat_interface():
    """Main Amazon Rufus-style chat interface"""
    
    st.markdown("## 🤖 AI Assistant - Amazon Rufus Style")
    
    # Initialize chat state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = None
    if "agent_responses" not in st.session_state:
        st.session_state.agent_responses = {}
    
    # Check if we have generated questions from question generator
    if st.session_state.get("question_gen_results"):
        questions = st.session_state.question_gen_results.get("questions", [])
        
        if questions:
            st.markdown("### 📋 Generated Questions - Click to Chat")
            
            # Display question cards
            for i, question_data in enumerate(questions, 1):
                if display_question_card(question_data, i):
                    # Check if this question was clicked
                    if st.session_state.get("selected_question") == i:
                        # Generate agent response for this question
                        if i not in st.session_state.agent_responses:
                            with st.spinner("🤖 Thinking..."):
                                question_text = question_data.get("question", "")
                                
                                if AGENT_AVAILABLE:
                                    try:
                                        response = requests.post(
                                            f"{API_URL}/advanced-chat",
                                            json={"message": question_text, "session_id": f"question_{i}"},
                                            timeout=60
                                        )
                                        
                                        if response.status_code == 200:
                                            response_data = response.json()
                                            st.session_state.agent_responses[i] = response_data
                                        else:
                                            st.session_state.agent_responses[i] = {
                                                "response": f"API Error: {response.status_code}",
                                                "sources": [],
                                                "metrics": {}
                                            }
                                    except Exception as e:
                                        st.session_state.agent_responses[i] = {
                                            "response": f"Error: {str(e)}",
                                            "sources": [],
                                            "metrics": {}
                                        }
                                else:
                                    st.session_state.agent_responses[i] = {
                                        "response": "Agent not available",
                                        "sources": [],
                                        "metrics": {}
                                    }
                        
                        # Display agent response
                        response_data = st.session_state.agent_responses[i]
                        display_agent_response(response_data, question_data)
    
    # Chat input area
    st.markdown("### 💬 Direct Chat")
    
    chat_input = st.text_input(
        "Ask me anything about the data, analytics, or request visualizations...",
        key="chat_input",
        placeholder="Try: 'Show me revenue trends' or 'Create a dashboard for customer analytics'"
    )
    
    if st.button("Send 💬") or chat_input:
        if chat_input.strip():
            with st.spinner("🤖 Processing..."):
                if AGENT_AVAILABLE:
                    try:
                        response = requests.post(
                            f"{API_URL}/advanced-chat",
                            json={"message": chat_input, "session_id": "direct_chat"},
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            response_data = response.json()
                            
                            # Add to chat history
                            st.session_state.chat_messages.append({
                                "type": "user",
                                "message": chat_input,
                                "timestamp": datetime.now()
                            })
                            
                            st.session_state.chat_messages.append({
                                "type": "agent", 
                                "message": response_data["response"],
                                "sources": response_data.get("sources", []),
                                "metrics": response_data.get("metrics", {}),
                                "timestamp": datetime.now()
                            })
                            
                            # Check for navigation intent
                            nav_intent = response_data.get("navigation_intent")
                            if nav_intent:
                                st.info(f"🧭 I can help you navigate to the {nav_intent.replace('_', ' ').title()} page.")
                                if st.button(f"Go to {nav_intent.replace('_', ' ').title()}"):
                                    st.session_state.current_page = nav_intent.title()
                                    st.rerun()
                        else:
                            st.error(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Agent not available. Please check your setup.")
    
    # Display chat history
    if st.session_state.chat_messages:
        st.subheader("📜 Chat History")
        
        for msg_index, msg in enumerate(st.session_state.chat_messages[-5:]):  # Show last 5 messages
            if msg["type"] == "user":
                st.write(f"**You:** {msg['message']}")
            else:
                st.write(f"**🤖 Agent:** {msg['message']}")
                
                # Show sources if available
                if msg.get("sources") and len(msg["sources"]) > 0:
                    with st.expander("📚 Sources for this response"):
                        for i, source in enumerate(msg["sources"][:3], 1):  # Show top 3 sources
                            content = source.get("content", "")
                            metadata = source.get("metadata", {})
                            similarity_score = source.get("score", 0)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**📄 Source {i}**")
                                st.write(f"**Score:** {similarity_score:.1%}")
                                doc_id = metadata.get("id", f"doc_{i}")
                                content_type = metadata.get("content_type", "unknown")
                                st.write(f"**ID:** {doc_id}")
                                st.write(f"**Type:** {content_type}")
                            
                            with col2:
                                st.write("**📋 Content Preview:**")
                                preview = content[:200] + "..." if len(content) > 200 else content
                                st.text_area("", value=preview, height=100, disabled=True, label_visibility="collapsed", key=f"preview_msg_{msg_index}_{i}_{doc_id[:8]}")
                
                # Show metrics if available
                if msg.get("metrics") and msg["metrics"]:
                    with st.expander("📊 Quality Metrics"):
                        metrics = msg["metrics"]
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("🎯 Coverage", f"{metrics.get('coverage_final', 0)*100:.0f}%")
                        with col2:
                            st.metric("📊 Specificity", f"{metrics.get('specificity_final', 0)*100:.0f}%")
                        with col3:
                            st.metric("💡 Insight", f"{metrics.get('insightfulness_final', 0)*100:.0f}%")
                        with col4:
                            st.metric("🔗 Grounded", f"{metrics.get('groundedness_final', 0)*100:.0f}%")
            
            st.divider()

# No JavaScript needed - using Streamlit buttons instead
