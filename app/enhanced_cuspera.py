"""
Enhanced Cuspera Working Application
Maintains original question generator with enhanced AI agent integration
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

st.set_page_config(
    page_title="Cuspera Supreme - B2B Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for blue/black/rainbow theme
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .main-header {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,78,146,0.3);
        border: 2px solid #00d4ff;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,78,146,0.3);
        margin: 1rem 0;
        border-left: 4px solid #00d4ff;
        border: 1px solid rgba(0,212,255,0.3);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(0,212,255,0.2);
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
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# API URL
API_URL = "http://localhost:8001"

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Cuspera Supreme</h1>
    <p>B2B Intelligence Platform with Enhanced AI Agent</p>
    <p>✨ Analytics | 💰 ROI | 📈 Dashboard | 📋 Questions | 🤖 AI Chat | 📑 Reports</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    
    if st.button("💬 Enhanced AI Agent", use_container_width=True, key="nav_chat"):
        st.session_state.current_page = "Chat"
    
    if st.button("📊 Analytics Dashboard", use_container_width=True, key="nav_analytics"):
        st.session_state.current_page = "Analytics"
    
    if st.button("📈 ROI Calculator", use_container_width=True, key="nav_roi"):
        st.session_state.current_page = "ROI"
    
    if st.button("📋 Question Generator", use_container_width=True, key="nav_questions"):
        st.session_state.current_page = "Questions"
    
    if st.button("📑 Reports", use_container_width=True, key="nav_reports"):
        st.session_state.current_page = "Reports"
    
    if st.button("⚙️ Status", use_container_width=True, key="nav_status"):
        st.session_state.current_page = "Status"
    
    st.markdown("---")
    
    # Session info
    st.markdown("### 📊 Session Info")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Page", st.session_state.current_page)
    st.metric("Session Time", f"{time.time() - st.session_state.get('start_time', time.time()):.0f}s")

# Main Content based on navigation
if st.session_state.current_page == "Chat":
    # Enhanced Chat Interface
    st.markdown("### 💬 Enhanced AI Agent")
    st.markdown("Your intelligent revenue intelligence assistant with analytics, ROI, and visualization capabilities")
    
    # Quick action buttons
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
    
    # Chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message agent-message">{message["content"]}</div>', unsafe_allow_html=True)
            
            # Always show sources if available
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources & References", expanded=True):
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
            
            # Always show metrics if available
            if "metrics" in message and message["metrics"]:
                with st.expander("📊 Response Quality Metrics", expanded=True):
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
    
    # Input area
    user_input = st.text_input(
        "Ask me anything about 6sense, analytics, ROI, or visualizations...",
        value=st.session_state.get("quick_query", ""),
        key="chat_input",
        placeholder="e.g., 'What are 6sense features?', 'Generate analytics', 'Calculate ROI'"
    )
    
    if "quick_query" in st.session_state:
        del st.session_state.quick_query
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("🚀 Send", type="primary", use_container_width=True):
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
                            "session_id": "enhanced_chat"
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
                        "content": f"Connection error: {str(e)}",
                        "timestamp": datetime.now()
                    })
                
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

elif st.session_state.current_page == "Questions":
    # EXACT question generator section from cuspera_working.py
    st.markdown("## 🎲 Enhanced Question Generator")
    st.markdown("Generate questions with REAL RAGAS-style evaluation metrics for both questions AND answers")
    
    # Initialize session state for question generator
    if 'question_gen_results' not in st.session_state:
        st.session_state.question_gen_results = None
    
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
    
    # Display Results - EXACT from cuspera_working.py
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
        
        # Detailed Q&A table with redirect to chat
        st.markdown("### 📋 Detailed Question & Answer Metrics")
        
        # Display Q&A pairs with chat redirect
        for i, q in enumerate(results.get("questions", []), 1):
            q_metrics = q.get("metrics", {})
            a_metrics = q.get("answer_metrics", {})
            
            with st.expander(f"**Q{i}:** {q.get('question', '')[:80]}{'...' if len(q.get('question', '')) > 80 else ''}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### 📝 Question")
                    st.info(q.get("question", ""))
                    
                    st.markdown("##### 📊 Question Metrics")
                    q_metrics_df = pd.DataFrame({
                        "Metric": ["Coverage", "Specificity", "Insightfulness", "Groundedness", "Overall"],
                        "Score": [
                            f"{q_metrics.get('coverage_final', 0)*100:.1f}%",
                            f"{q_metrics.get('specificity_final', 0)*100:.1f}%",
                            f"{q_metrics.get('insightfulness_final', 0)*100:.1f}%",
                            f"{q_metrics.get('groundedness_final', 0)*100:.1f}%",
                            f"{q_metrics.get('overall_score', 0)*100:.1f}%"
                        ],
                        "Pass": ["—", "—", "—", "—", "✅" if q_metrics.get("overall_pass") else "❌"]
                    })
                    st.dataframe(q_metrics_df, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("##### 💬 Answer")
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%); 
                                border: 1px solid #00d4ff; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                        <p style="color: white; font-size: 1rem; line-height: 1.5;">
                            {q.get("answer", "")}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("##### 📊 Answer Metrics")
                    a_metrics_df = pd.DataFrame({
                        "Metric": ["Coverage", "Specificity", "Insightfulness", "Groundedness", "Overall"],
                        "Score": [
                            f"{a_metrics.get('coverage_final', 0)*100:.1f}%",
                            f"{a_metrics.get('specificity_final', 0)*100:.1f}%",
                            f"{a_metrics.get('insightfulness_final', 0)*100:.1f}%",
                            f"{a_metrics.get('groundedness_final', 0)*100:.1f}%",
                            f"{a_metrics.get('overall_score', 0)*100:.1f}%"
                        ],
                        "Pass": ["—", "—", "---", "—", "✅" if a_metrics.get("overall_pass") else "❌"]
                    })
                    st.dataframe(a_metrics_df, use_container_width=True, hide_index=True)
                
                st.markdown(f"**📚 Sources Retrieved:** {q.get('retrieved_sources', 0)}")
                st.markdown(f"**🔗 Context Source:** {q.get('context_source', '')}")
                
                # Chat redirect button - Amazon Rufus style
                if st.button(f"💬 Chat About This Question (Amazon Rufus Style)", key=f"chat_redirect_{i}", use_container_width=True):
                    # Store question data for chat interface
                    st.session_state.redirect_question = q
                    st.session_state.current_page = "Chat"
                    st.rerun()
                
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
                    
                    # Question metrics (all)
                    "Q_Coverage_Math": q_m.get("coverage_math", 0),
                    "Q_Coverage_LLM": q_m.get("coverage_llm", 0),
                    "Q_Coverage_Final": q_m.get("coverage_final", 0),
                    "Q_Specificity_Math": q_m.get("specificity_math", 0),
                    "Q_Specificity_LLM": q_m.get("specificity_llm", 0),
                    "Q_Specificity_Final": q_m.get("specificity_final", 0),
                    "Q_Insight_Math": q_m.get("insightfulness_math", 0),
                    "Q_Insight_LLM": q_m.get("insightfulness_llm", 0),
                    "Q_Insight_Final": q_m.get("insightfulness_final", 0),
                    "Q_Grounded_Math": q_m.get("groundedness_math", 0),
                    "Q_Grounded_LLM": q_m.get("groundedness_llm", 0),
                    "Q_Grounded_Final": q_m.get("groundedness_final", 0),
                    "Q_Overall_Score": q_m.get("overall_score", 0),
                    "Q_Overall_Pass": q_m.get("overall_pass", False),
                    
                    # Answer metrics (all)
                    "A_Coverage_Math": a_m.get("coverage_math", 0),
                    "A_Coverage_LLM": a_m.get("coverage_llm", 0),
                    "A_Coverage_Final": a_m.get("coverage_final", 0),
                    "A_Specificity_Math": a_m.get("specificity_math", 0),
                    "A_Specificity_LLM": a_m.get("specificity_llm", 0),
                    "A_Specificity_Final": a_m.get("specificity_final", 0),
                    "A_Insight_Math": a_m.get("insightfulness_math", 0),
                    "A_Insight_LLM": a_m.get("insightfulness_llm", 0),
                    "A_Insight_Final": a_m.get("insightfulness_final", 0),
                    "A_Grounded_Math": a_m.get("groundedness_math", 0),
                    "A_Grounded_LLM": a_m.get("groundedness_llm", 0),
                    "A_Grounded_Final": a_m.get("groundedness_final", 0),
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
            # Passed only
            passed_data = [row for row in export_data if row["Q_Overall_Pass"] and row["A_Overall_Pass"]]
            passed_df = pd.DataFrame(passed_data)
            st.download_button(
                label="📥 Download Passed Only",
                data=passed_df.to_csv(index=False),
                file_name=f"qa_passed_{results['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col3:
            # FAQ Export
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
            
            if st.button("🔄 Generate New Questions"):
                st.session_state.question_gen_results = None
                st.rerun()

# Handle question redirect from question generator
if st.session_state.current_page == "Chat" and 'redirect_question' in st.session_state:
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

# Add other pages (Analytics, ROI, Reports, Status) from original cuspera_working.py
# [These would be added here - keeping them the same as original]

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: white; opacity: 0.8;">
        <p>🚀 Powered by 6sense Revenue AI | Enhanced Analytics & Intelligence Platform</p>
        <p>✨ Comprehensive AI Agent | 📊 Real-time Analytics | 💰 ROI Calculator | 📋 Question Generator</p>
    </div>
    """,
    unsafe_allow_html=True
)
