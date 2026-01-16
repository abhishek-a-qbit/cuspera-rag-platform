"""
Advanced Agent Streamlit Interface
Single-page application with comprehensive AI agent capabilities
Maintains question generator from cuspera_working.py with Amazon Rufus style display
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import base64
from typing import Dict, List, Any

st.set_page_config(
    page_title="6sense AI Agent - Revenue Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI with background
def set_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Try to set background image
try:
    set_background("assets/background.png")
except:
    pass  # Continue without background image

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .chat-message {
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        max-width: 85%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        margin-left: auto;
        border-radius: 18px 18px 4px 18px;
    }
    
    .agent-message {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        border-radius: 18px 18px 18px 4px;
    }
    
    .source-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        backdrop-filter: blur(5px);
    }
    
    .metric-display {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        text-align: center;
        margin: 5px 0;
        font-weight: bold;
    }
    
    .quick-action-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .question-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-container img {
        max-width: 150px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if 'current_view' not in st.session_state:
    st.session_state.current_view = "Chat"
if 'question_gen_results' not in st.session_state:
    st.session_state.question_gen_results = None

# API URL
API_URL = "http://localhost:8001"

# Header with logo
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("assets/logo.png", width=150)
except:
    st.markdown("🚀", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚀 6sense AI Agent</h1>
    <h3>Your Intelligent Revenue Intelligence Assistant</h3>
    <p>✨ Analytics | 💰 ROI Calculator | 📈 Dashboard | 📋 Questions | 🎨 Infographics | 🤖 AI Chat</p>
</div>
""", unsafe_allow_html=True)

# Navigation - Simple tabs
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("💬 Chat with AI Agent", use_container_width=True, key="nav_chat"):
        st.session_state.current_view = "Chat"
    if st.button("📋 Question Generator", use_container_width=True, key="nav_questions"):
        st.session_state.current_view = "Questions"

# Main Content
if st.session_state.current_view == "Chat":
    # Enhanced Chat Interface
    st.markdown("### 💬 Chat with Enhanced AI Agent")
    st.markdown("Ask me anything about 6sense, analytics, ROI, dashboards, or visualizations!")
    
    # Quick action buttons
    st.markdown("#### 🎯 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Analytics Report", use_container_width=True):
            st.session_state.quick_query = "Generate analytics report"
    with col2:
        if st.button("💰 Calculate ROI", use_container_width=True):
            st.session_state.quick_query = "Calculate ROI for 6sense"
    with col3:
        if st.button("📈 Create Dashboard", use_container_width=True):
            st.session_state.quick_query = "Create dashboard showing 6sense metrics"
    with col4:
        if st.button("🎨 Generate Infographic", use_container_width=True):
            st.session_state.quick_query = "Generate infographic showing 6sense impact"
    
    # Chat messages display
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message agent-message">{message["content"]}</div>', unsafe_allow_html=True)
                
                # ALWAYS show sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources & References", expanded=True):
                        for i, source in enumerate(message["sources"][:3]):
                            st.markdown(f'<div class="source-card">', unsafe_allow_html=True)
                            st.markdown(f"**Source {i+1}**")
                            if isinstance(source, dict):
                                content = source.get("content", "")
                                metadata = source.get("metadata", {})
                                similarity_score = source.get("score", 0)
                                
                                # Document metadata
                                doc_id = metadata.get("id", f"doc_{i}")
                                content_type = metadata.get("content_type", "unknown")
                                dataset = metadata.get("dataset", "unknown")
                                source_file = metadata.get("source", "unknown")
                                
                                st.write(f"**📋 Document ID:** {doc_id}")
                                st.write(f"**📄 Type:** {content_type}")
                                st.write(f"**📊 Dataset:** {dataset}")
                                if source_file != "unknown":
                                    st.write(f"**📁 Source:** {source_file}")
                                st.write(f"**🎯 Match Score:** {similarity_score:.1%}")
                                
                                if content:
                                    st.markdown(f"**📝 Content Preview:** {content[:200]}...")
                                
                                if metadata:
                                    with st.expander("🔍 Full Metadata"):
                                        st.json(metadata)
                            else:
                                st.markdown(f"**📝 Content:** {str(source)[:200]}...")
                            st.markdown('</div>', unsafe_allow_html=True)
                
                # ALWAYS show metrics if available
                if "metrics" in message and message["metrics"]:
                    with st.expander("📊 Response Quality Metrics", expanded=True):
                        metrics = message["metrics"]
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f'<div class="metric-display">🎯 Coverage<br>{metrics.get("coverage_final", 0):.1%}</div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown(f'<div class="metric-display">📊 Specificity<br>{metrics.get("specificity_final", 0):.1%}</div>', unsafe_allow_html=True)
                        with col3:
                            st.markdown(f'<div class="metric-display">💡 Insightfulness<br>{metrics.get("insightfulness_final", 0):.1%}</div>', unsafe_allow_html=True)
                        with col4:
                            st.markdown(f'<div class="metric-display">🔗 Groundedness<br>{metrics.get("groundedness_final", 0):.1%}</div>', unsafe_allow_html=True)
                        
                        # Additional metrics
                        if "tools_used" in message and message["tools_used"]:
                            st.write(f"**🔧 Tools Used:** {', '.join(message['tools_used'])}")
                        if "retrieved_sources" in message:
                            st.write(f"**📚 Sources Retrieved:** {message['retrieved_sources']}")
    
    # Input area
    user_input = st.text_input(
        "Ask me anything about 6sense, analytics, ROI, dashboards, or visualizations...",
        value=st.session_state.get("quick_query", ""),
        key="chat_input",
        placeholder="e.g., 'What are 6sense features?', 'Generate analytics report', 'Calculate ROI', 'Create dashboard'"
    )
    
    if "quick_query" in st.session_state:
        del st.session_state.quick_query
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("🚀 Send Message", type="primary", use_container_width=True):
            if user_input:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now()
                })
                
                # Get response from enhanced agent
                try:
                    response = requests.post(
                        f"{API_URL}/advanced-chat",
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
                            "tools_used": tools_used,
                            "timestamp": datetime.now()
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Error: Backend unavailable (Status: {response.status_code})",
                            "timestamp": datetime.now()
                        })
                
                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Connection error: Unable to reach backend service. Please ensure the backend is running on localhost:8001",
                        "timestamp": datetime.now()
                    })
                
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

elif st.session_state.current_view == "Questions":
    # EXACT question generator section from cuspera_working.py
    st.markdown("## 🎲 Enhanced Question Generator")
    st.markdown("Generate questions with REAL RAGAS-style evaluation metrics for both questions AND answers")
    
    # Question Generator Configuration
    with st.expander("⚙️ Generator Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            target_product = st.selectbox("Target Product", [
                "6sense Revenue AI", "Demandbase One", "Bombora", 
                "ZoomInfo SalesOS", "LinkedIn Sales Navigator"
            ])
            target_count = st.slider("Target Question Count", min_value=1, max_value=50, value=10, step=1)
            
            custom_prompt = st.text_area(
                "🔍 Custom Prompt (Optional)",
                value="",
                height=100,
                help="Enter a custom prompt for question generation. Leave empty to use default settings.",
                placeholder="Example: Generate questions about implementation challenges and ROI for enterprise clients..."
            )
        
        with col2:
            st.info("""
            **New in this version:**
            - ✅ Real LLM grading (not proxy scores)
            - ✅ Real groundedness calculation
            - ✅ Answer metrics included
            - ✅ NLP-based specificity
            - ✅ Semantic similarity scoring
            """)
    
    # Generate Questions Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Questions with REAL Metrics", type="primary", use_container_width=True):
            with st.spinner("🔄 Generating questions with real LLM evaluation..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate-questions",
                        json={"topic": target_product, "num_questions": target_count},
                        timeout=300  # Increased timeout for LLM grading
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("status") == "success":
                            # Store results
                            st.session_state.question_gen_results = {
                                "questions": result.get("questions", []),
                                "metrics": result.get("metrics", {}),
                                "product": target_product,
                                "target_count": target_count
                            }
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating questions: {str(e)}")
    
    # Display Results - AMAZON RUFUS STYLE
    if st.session_state.question_gen_results:
        results = st.session_state.question_gen_results
        metrics = results.get("metrics", {})
        
        st.markdown(f"### 🎯 Generation Results for {results['product']}")
        
        # Top-level metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📊 Total Generated",
                metrics.get("total_questions", 0),
                help="Total question-answer pairs generated"
            )
        
        with col2:
            st.metric(
                "✅ Questions Passed",
                f"{metrics.get('passed_questions', 0)} ({metrics.get('question_pass_rate', 0):.1f}%)",
                help="Questions meeting quality thresholds"
            )
        
        with col3:
            st.metric(
                "✅ Answers Passed",
                f"{metrics.get('passed_answers', 0)} ({metrics.get('answer_pass_rate', 0):.1f}%)",
                help="Answers meeting quality thresholds"
            )
        
        with col4:
            st.metric(
                "🎯 Combined Pass Rate",
                f"{metrics.get('combined_pass_rate', 0):.1f}%",
                help="Overall quality score"
            )
        
        # Detailed metrics comparison
        st.markdown("### 📊 Question vs Answer Metrics Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📝 Question Metrics**")
            q_metrics_df = pd.DataFrame({
                "Metric": ["Coverage", "Specificity", "Insightfulness", "Groundedness", "Overall"],
                "Score": [
                    f"{metrics.get('coverage_q_avg', 0)*100:.1f}%",
                    f"{metrics.get('specificity_q_avg', 0)*100:.1f}%",
                    f"{metrics.get('insightfulness_q_avg', 0)*100:.1f}%",
                    f"{metrics.get('groundedness_q_avg', 0)*100:.1f}%",
                    f"{metrics.get('overall_q_avg', 0)*100:.1f}%"
                ]
            })
            st.dataframe(q_metrics_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**💬 Answer Metrics**")
            a_metrics_df = pd.DataFrame({
                "Metric": ["Coverage", "Specificity", "Insightfulness", "Groundedness", "Overall"],
                "Score": [
                    f"{metrics.get('coverage_a_avg', 0)*100:.1f}%",
                    f"{metrics.get('specificity_a_avg', 0)*100:.1f}%",
                    f"{metrics.get('insightfulness_a_avg', 0)*100:.1f}%",
                    f"{metrics.get('groundedness_a_avg', 0)*100:.1f}%",
                    f"{metrics.get('overall_a_avg', 0)*100:.1f}%"
                ]
            })
            st.dataframe(a_metrics_df, use_container_width=True, hide_index=True)
        
        # Radar chart comparison
        try:
            fig = go.Figure()
            
            categories = ['Coverage', 'Specificity', 'Insightfulness', 'Groundedness']
            
            fig.add_trace(go.Scatterpolar(
                r=[
                    metrics.get('coverage_q_avg', 0),
                    metrics.get('specificity_q_avg', 0),
                    metrics.get('insightfulness_q_avg', 0),
                    metrics.get('groundedness_q_avg', 0)
                ],
                theta=categories,
                fill='toself',
                name='Questions',
                line_color='#00d4ff'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[
                    metrics.get('coverage_a_avg', 0),
                    metrics.get('specificity_a_avg', 0),
                    metrics.get('insightfulness_a_avg', 0),
                    metrics.get('groundedness_a_avg', 0)
                ],
                theta=categories,
                fill='toself',
                name='Answers',
                line_color='#ff8c00'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                showlegend=True,
                title="Question vs Answer Quality Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.warning(f"Could not create radar chart: {e}")
        
        # AMAZON RUFUS STYLE Question Display with redirect to chat
        st.markdown("### 📋 Amazon Rufus Style Question Cards")
        
        for i, q in enumerate(results.get("questions", []), 1):
            q_metrics = q.get("metrics", {})
            a_metrics = q.get("answer_metrics", {})
            
            # Amazon Rufus style card
            with st.container():
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                
                # Header with scores
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.subheader(f"🤔 Question {i}")
                with col2:
                    q_score = q_metrics.get("overall_score", 0) * 100
                    st.metric("Q", f"{q_score:.0f}%")
                with col3:
                    a_score = a_metrics.get("overall_score", 0) * 100
                    st.metric("A", f"{a_score:.0f}%")
                
                # Question text
                st.info(q.get("question", ""))
                
                # Answer with styling
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%); 
                            border: 1px solid #00d4ff; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                    <p style="color: white; font-size: 1rem; line-height: 1.5;">
                        {q.get("answer", "")}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # ALWAYS show metrics
                st.markdown("##### 📊 Quality Metrics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🎯 Coverage", f"{q_metrics.get('coverage_final', 0)*100:.0f}%")
                with col2:
                    st.metric("📊 Specificity", f"{q_metrics.get('specificity_final', 0)*100:.0f}%")
                with col3:
                    st.metric("💡 Insightfulness", f"{q_metrics.get('insightfulness_final', 0)*100:.0f}%")
                with col4:
                    st.metric("🔗 Groundedness", f"{q_metrics.get('groundedness_final', 0)*100:.0f}%")
                
                # ALWAYS show sources/metadata
                st.markdown(f"**📚 Sources Retrieved:** {q.get('retrieved_sources', 0)}")
                st.markdown(f"**🔗 Context Source:** {q.get('context_source', '')}")
                st.markdown(f"**🎯 Topic Name:** {q.get('topic_name', '6sense Analytics')}")
                
                # Enhanced evidence display
                if "enhanced_evidence" in q and q["enhanced_evidence"]:
                    st.markdown("##### 📚 Enhanced Evidence")
                    for j, evidence in enumerate(q["enhanced_evidence"][:2]):
                        st.write(f"**Evidence {j+1}:**")
                        if isinstance(evidence, dict):
                            st.write(f"**🔗 Link:** {evidence.get('link', 'N/A')}")
                            st.write(f"**📄 Type:** {evidence.get('type', 'N/A')}")
                            st.write(f"**📊 Score:** {evidence.get('score', 0):.2f}")
                            if "content_preview" in evidence:
                                st.write(f"**📝 Preview:** {evidence['content_preview']}")
                            if "metadata" in evidence:
                                with st.expander(f"🔍 Evidence {j+1} Metadata"):
                                    st.json(evidence["metadata"])
                
                # Amazon Rufus style chat redirect button
                if st.button(f"💬 Chat About This Question (Amazon Rufus Style)", key=f"rufus_chat_{i}", use_container_width=True):
                    # Store question data for chat interface
                    st.session_state.redirect_question = q
                    st.session_state.current_view = "Chat"
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Export options
        st.markdown("### 📤 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Full export with all metrics
            export_data = []
            for i, q in enumerate(results.get("questions", []), 1):
                q_m = q.get("metrics", {})
                a_m = q.get("answer_metrics", {})
                export_data.append({
                    "ID": i,
                    "Question": q.get("question", ""),
                    "Answer": q.get("answer", ""),
                    "Context_Source": q.get("context_source", ""),
                    "Retrieved_Sources": q.get("retrieved_sources", 0),
                    "Topic_Name": q.get("topic_name", ""),
                    
                    # Question metrics (all)
                    "Q_Coverage_Final": q_m.get("coverage_final", 0),
                    "Q_Specificity_Final": q_m.get("specificity_final", 0),
                    "Q_Insightfulness_Final": q_m.get("insightfulness_final", 0),
                    "Q_Groundedness_Final": q_m.get("groundedness_final", 0),
                    "Q_Overall_Score": q_m.get("overall_score", 0),
                    "Q_Overall_Pass": q_m.get("overall_pass", False),
                    
                    # Answer metrics (all)
                    "A_Coverage_Final": a_m.get("coverage_final", 0),
                    "A_Specificity_Final": a_m.get("specificity_final", 0),
                    "A_Insightfulness_Final": a_m.get("insightfulness_final", 0),
                    "A_Groundedness_Final": a_m.get("groundedness_final", 0),
                    "A_Overall_Score": a_m.get("overall_score", 0),
                    "A_Overall_Pass": a_m.get("overall_pass", False)
                })
            
            full_df = pd.DataFrame(export_data)
            st.download_button(
                label="📥 Download Full Metrics CSV",
                data=full_df.to_csv(index=False),
                file_name=f"qa_full_metrics_{results['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # FAQ Export with enhanced evidence
            if st.button("📋 Generate FAQ Format"):
                faq_data = []
                for i, q in enumerate(results.get("questions", []), 1):
                    q_m = q.get("metrics", {})
                    a_m = q.get("answer_metrics", {})
                    
                    # Create FAQ entry with enhanced evidence
                    faq_entry = {
                        "question": q.get("question", ""),
                        "answer": q.get("answer", ""),
                        "section": "General",
                        "context": [
                            {
                                "name": q.get("topic_name", "6sense Analytics"),  # Use generated topic
                                "code": f"Q_{i}",
                                "type": "capability",
                                "score": q_m.get("overall_score", 0)
                            }
                        ],
                        "evidence": q.get("enhanced_evidence", [  # Use enhanced evidence with document links
                                {
                                    "link": f"#question_{i}",
                                    "type": "generated",
                                    "score": q_m.get("groundedness_final", 0)
                                }
                            ])
                    }
                    faq_data.append(faq_entry)
                
                # Convert to JSON and provide download
                faq_json = json.dumps(faq_data, indent=2)
                st.download_button(
                    label="📋 Download FAQ JSON",
                    data=faq_json,
                    file_name=f"faq_{results['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("🔄 Generate New Questions"):
                st.session_state.question_gen_results = None
                st.rerun()

# Handle question redirect from question generator
if st.session_state.current_view == "Chat" and 'redirect_question' in st.session_state:
    question_data = st.session_state.redirect_question
    
    # Add the question as a user message
    st.session_state.messages.append({
        "role": "user",
        "content": question_data.get("question", ""),
        "timestamp": datetime.now()
    })
    
    # Get response from enhanced agent
    try:
        response = requests.post(
            f"{API_URL}/advanced-chat",
            json={
                "message": question_data.get("question", ""),
                "session_id": "question_redirect"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            agent_response = result.get("response", "I'm having trouble processing your question.")
            sources = result.get("sources", [])
            metrics = result.get("metrics", {})
            tools_used = result.get("tools_used", [])
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": agent_response,
                "sources": sources,
                "metrics": metrics,
                "tools_used": tools_used,
                "timestamp": datetime.now()
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: Backend unavailable (Status: {response.status_code})",
                "timestamp": datetime.now()
            })
    
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Connection error: {str(e)}",
            "timestamp": datetime.now()
        })
    
    # Clear redirect
    del st.session_state.redirect_question
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: white; opacity: 0.8;">
        <p>🚀 Powered by 6sense Revenue AI | Advanced Analytics & Intelligence Platform</p>
        <p>✨ Comprehensive AI Agent | 📊 Real-time Analytics | 💰 ROI Calculator | 📋 Question Generator</p>
        <p>🎨 Visual Content Generation | 📈 Dashboard Creation | 🤖 Seamless Chat Experience</p>
    </div>
    """,
    unsafe_allow_html=True
)
