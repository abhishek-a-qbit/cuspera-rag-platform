import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Set page configuration with beautiful theme
st.set_page_config(
    page_title=" Cuspera Supreme - Beautiful Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Beautiful custom CSS with animations and aesthetic images
st.markdown("""
<style>
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Animated background with aesthetic patterns */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%),
            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>'),
            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><radialGradient id="chaos1"><stop offset="0%" stop-color="%23667eea"/><stop offset="100%" stop-color="%23764ba2"/></radialGradient><circle cx="50" cy="50" r="40" fill="url(%23chaos1)" opacity="0.1"/></defs><rect width="200" height="200" fill="url(%23chaos1)"/></svg>');
        background-attachment: fixed;
        background-size: 400px 400px, 200px 200px;
        animation: aestheticFloat 20s ease-in-out infinite;
    }
    
    /* Chaotic decorative elements */
    .chaotic-decoration {
        position: fixed;
        pointer-events: none;
        z-index: -1;
        opacity: 0.05;
    }
    
    .decoration-1 {
        top: 10%;
        left: 5%;
        width: 150px;
        height: 150px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><linearGradient id="grad1"><stop offset="0%" stop-color="%23ff6b6b"/><stop offset="100%" stop-color="%234ecdc4"/></linearGradient><polygon points="50,10 90,90" fill="url(%23grad1)"/></defs><rect width="100" height="100" fill="none"/></svg>');
        transform: rotate(45deg);
        animation: spin 15s linear infinite;
    }
    
    .decoration-2 {
        bottom: 15%;
        right: 8%;
        width: 100px;
        height: 100px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><radialGradient id="grad2"><stop offset="0%" stop-color="%23f093fb"/><stop offset="100%" stop-color="%23f5576c"/></radialGradient><circle cx="50" cy="50" r="40" fill="url(%23grad2)"/></defs><rect width="100" height="100" fill="none"/></svg>');
        animation: pulse 3s ease-in-out infinite;
    }
    
    .decoration-3 {
        top: 60%;
        right: 3%;
        width: 80px;
        height: 80px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><linearGradient id="grad3"><stop offset="0%" stop-color="%239c27b0"/><stop offset="100%" stop-color="%2366eea"/></linearGradient><polygon points="20,80 80,20 50" fill="url(%23grad3)"/></defs><rect width="100" height="100" fill="none"/></svg>');
        animation: bounce 4s ease-in-out infinite;
    }
    
    /* Enhanced glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="noise" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23noise)"/></svg>');
        pointer-events: none;
    }
    
    /* Animated buttons */
    .aesthetic-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .aesthetic-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .aesthetic-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Chat message styling */
    .chat-message {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        position: relative;
        animation: messageSlide 0.5s ease-out;
    }
    
    @keyframes messageSlide {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Canvas container */
    .canvas-container {
        background: 
            linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(102,126,234,0.05) 100%),
            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><pattern id="canvas-pattern" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="none" stroke="rgba(255,255,255,0.02)"/></pattern></defs><rect width="200" height="200" fill="url(%23canvas-pattern)"/></svg>');
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .canvas-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><radialGradient id="canvas-glow"><stop offset="0%" stop-color="%23667eea" stop-opacity="0.1"/><stop offset="100%" stop-color="%23764ba2" stop-opacity="0.05"/></radialGradient><circle cx="50" cy="50" r="50" fill="url(%23canvas-glow)"/></defs><rect width="100" height="100" fill="none"/></svg>');
        pointer-events: none;
        animation: canvasGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes canvasGlow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.1; }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Input styling */
    .stTextInput > div > input {
        background: rgba(255,255,255,0.95);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1.5rem 2rem;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        color: #333;
        height: 60px;
    }
    
    .stTextInput > div > input::placeholder {
        color: #333;
        opacity: 0.7;
    }
    
    .stTextInput > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        color: #333;
    }
    
    /* Hide streamlit branding */
    .stDeployButton {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
</style>

<!-- Chaotic decorative elements -->
<div class="chaotic-decoration decoration-1"></div>
<div class="chaotic-decoration decoration-2"></div>
<div class="chaotic-decoration decoration-3"></div>
""", unsafe_allow_html=True)

# Create beautiful logo placeholder
def create_logo():
    """Create a beautiful logo for Cuspera Supreme"""
    try:
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Create gradient background
        gradient = np.linspace(0, 1, 256).reshape(256, 1)
        gradient = np.hstack((gradient, gradient))
        ax.imshow(gradient, extent=[0, 10, 0, 10], aspect='auto', cmap='viridis')
        
        # Add Cuspera Supreme text
        ax.text(5, 5, 'Cuspera', fontsize=20, fontweight='bold', 
                ha='center', va='center', color='white')
        ax.text(5, 3, 'Supreme', fontsize=8, 
                ha='center', va='center', color='white')
        
        # Save to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        return img_str
    except Exception as e:
        print(f"Logo creation failed: {e}")
        # Return a simple emoji-based logo fallback
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhf/kZQAAAAlwSFlzAAALEwAACxYAAADKAAAZIlgdAAALx0RB2AAAAAAAASUVORK5CYII="

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'page' not in st.session_state:
    st.session_state.page = 'chat'
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = []
if 'last_intent' not in st.session_state:
    st.session_state.last_intent = None

# Sidebar with beautiful design
with st.sidebar:
    # Logo and branding
    try:
        logo_img = create_logo()
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{logo_img}" 
                 style="width: 80px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
            <h3 style="margin: 1rem 0 0.5rem 0; color: white;">Cuspera Supreme</h3>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Advanced Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        print(f"Sidebar logo display failed: {e}")
        # Fallback to text-based logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; color: white;">
            <h1 style="margin: 0; font-size: 2rem;"></h1>
            <h3 style="margin: 0.5rem 0; color: white;">Cuspera Supreme</h3>
            <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">Advanced Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    
    if st.button("� Chat Assistant", use_container_width=True, key="nav_chat"):
        st.session_state.page_selector = "💬 Chat Assistant"
    
    if st.button("�📋 Question Generator", use_container_width=True, key="nav_questions"):
        st.session_state.page_selector = "📋 Question Generator"
    
    # Status section
    st.markdown("---")
    st.markdown("###  System Status")
    
    # Check backend status
    try:
        response = requests.get("http://localhost:8001/", timeout=2)
        status_color = "#4CAF50"
        status_text = "Online"
        status_icon = ""
    except:
        status_color = "#f44336"
        status_text = "Offline"
        status_icon = ""
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span>Backend Status</span>
            <span style="color: {status_color}; font-weight: bold;">{status_icon} {status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("###  Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Messages Today", "247", "+12%")
    with col2:
        st.metric("Dashboards Created", "18", "+5")
    with col3:
        st.metric("ROI Calculations", "32", "+8")
    with col4:
        st.metric("Reports Generated", "15", "+3")

# Main content area - Single page with chat and question generator
# Check backend status
try:
    backend_response = requests.get("http://localhost:8001/", timeout=3)
    if backend_response.status_code == 200:
        backend_status = "🟢 Online"
        backend_color = "#4CAF50"
    else:
        backend_status = "🔴 Error"
        backend_color = "#f44336"
except:
    backend_status = "🔴 Offline"
    backend_color = "#f44336"

# Display backend status
st.markdown(f"""
<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-weight: bold;">Backend Status:</span>
        <span style="color: {backend_color}; font-weight: bold;">{backend_status}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Page selector
page = st.selectbox(
    "Choose Functionality:",
    ["💬 Chat Assistant", "📋 Question Generator"],
    key="page_selector",
    index=0
)

if page == "📋 Question Generator":
    # Enhanced Question Generator (from cuspera_working.py)
    st.markdown("""
    <div class="glass-card">
        <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                Enhanced Question Generator
            </h1>
            <h2 style="font-size: 1.8rem; margin-bottom: 1rem; opacity: 0.9;">
                Generate Questions with REAL RAGAS-style Evaluation
            </h2>
            <p style="font-size: 1.2rem; opacity: 0.8; margin: 0;">
                Generate questions with real LLM grading and comprehensive metrics! 
            </p>
        </div>
    """, unsafe_allow_html=True)
    
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
            target_count = st.slider("Target Question Count", min_value=3, max_value=20, value=5, step=1)
            
            question_type = st.selectbox("Question Type:", [
                "General", "Technical", "Business", "ROI-focused", "Feature-specific"
            ])
            
            difficulty = st.selectbox("Difficulty Level:", [
                "Basic", "Intermediate", "Advanced"
            ])
            
            include_rag = st.checkbox("Include RAG context from database", value=True)
        
        with col2:
            st.info("""
            **Features Available:**
            - ✅ Real LLM grading (not proxy scores)
            - ✅ Real groundedness calculation
            - ✅ Answer metrics included
            - ✅ NLP-based specificity
            - ✅ Semantic similarity scoring
            - ✅ Amazon Rufus style display
            - ✅ Direct chat redirection
            """)
    
    # Generate Questions Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🚀 Generate Questions with REAL Metrics", type="primary", use_container_width=True)
        
        clear_button = st.button("🗑️ Clear Results", use_container_width=True)
        
        if clear_button:
            if 'question_gen_results' in st.session_state:
                del st.session_state.question_gen_results
            st.rerun()
        
        if generate_button:
            with st.spinner("🔄 Generating questions with real LLM evaluation..."):
                try:
                    response = requests.post(
                        "http://localhost:8001/generate-questions",
                        json={
                            "topic": target_product,
                            "num_questions": target_count,
                            "question_type": question_type,
                            "difficulty": difficulty,
                            "include_rag": include_rag
                        },
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Store results
                        st.session_state.question_gen_results = result
                        st.success(f"✅ Generated {len(result.get('questions', []))} questions successfully!")
                        
                        # Display questions with Amazon Rufus style
                        questions = result.get('questions', [])
                        
                        for i, question_data in enumerate(questions, 1):
                            # Extract question data
                            question_raw = question_data.get("question", "")
                            question = str(question_raw).strip().strip('"\'')
                            
                            metrics = question_data.get("metrics", {})
                            answer_metrics = question_data.get("answer_metrics", {})
                            sources = question_data.get("retrieved_sources", 0)
                            
                            # Calculate overall scores
                            q_score = metrics.get("overall_score", 0) * 100
                            a_score = answer_metrics.get("overall_score", 0) * 100
                            
                            # Generate topic name from source chunks
                            topic_name = "Generated Q&A"
                            if sources and len(sources) > 0:
                                first_source = sources[0]
                                if first_source.get('metadata'):
                                    topic_name = first_source['metadata'].get('dataset', 'Generated Q&A')
                            
                            # Beautiful question card with chat redirection
                            st.markdown(f"""
                            <div class="glass-card">
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                                    <h4 style="margin: 0;">Question {topic_name} - Question {i}</h4>
                                    <div style="display: flex; gap: 1rem;">
                                        <span style="background: #4CAF50; color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">Q: {q_score:.0f}%</span>
                                        <span style="background: #2196F3; color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">A: {a_score:.0f}%</span>
                                    </div>
                                </div>
                                
                                <p style="font-size: 1.1rem; margin-bottom: 1rem;">{question}</p>
                                
                                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                                    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);">
                                        <h5 style="margin: 0 0 0.5rem 0; color: #667eea;">Metrics</h5>
                                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                                            <div>
                                                <strong>Sources:</strong> {sources}
                                            </div>
                                            <div>
                                                <strong>Coverage:</strong> {metrics.get('coverage_final', 0)*100:.0f}%
                                            </div>
                                            <div>
                                                <strong>Specificity:</strong> {metrics.get('specificity_final', 0)*100:.0f}%
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);">
                                        <h5 style="margin: 0 0 0.5rem 0; color: #2196F3;">Answer Metrics</h5>
                                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                                            <div>
                                                <strong>Insightfulness:</strong> {answer_metrics.get('insightfulness_final', 0)*100:.0f}%
                                            </div>
                                            <div>
                                                <strong>Groundedness:</strong> {answer_metrics.get('groundedness_final', 0)*100:.0f}%
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div style="text-align: center; margin-top: 1rem;">
                                    <button class="aesthetic-btn" onclick="window.location.reload()">
                                        💬 Chat About This Question
                                    </button>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                            # Store question for chat redirection
                            st.session_state[f"selected_question_{i}"] = {
                                "question": question,
                                "answer": question_data.get("answer", ""),
                                "metrics": metrics,
                                "answer_metrics": answer_metrics,
                                "sources": sources,
                                "topic_name": topic_name
                            }
                    
                    st.divider()
                    
                    # Display chat redirection message
                    st.markdown("""
                    <div class="glass-card">
                        <h3>🎯 Questions Ready for Chat!</h3>
                        <p>Click on any question above to start a detailed conversation about it in the chat assistant.</p>
                        <p>The AI assistant will have access to all the metrics, sources, and context for that specific question.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add button to switch to chat
                    if st.button("💬 Go to Chat Assistant", type="primary", use_container_width=True):
                        st.session_state.page_selector = "💬 Chat Assistant"
                        st.rerun()
                    
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

else:  # Chat Assistant page
    # Check if we have selected questions from question generator
    selected_questions = {k: v for k, v in st.session_state.items() if k.startswith("selected_question_")}
    
    if selected_questions:
        st.markdown("### 📋 Selected Questions - Click to Chat")
        
        for key, question_data in selected_questions.items():
            question_num = key.split("_")[-1]
            question = question_data.get("question", "")
            answer = question_data.get("answer", "")
            metrics = question_data.get("metrics", {})
            answer_metrics = question_data.get("answer_metrics", {})
            sources = question_data.get("sources", 0)
            topic_name = question_data.get("topic_name", "Generated Q&A")
            
            q_score = metrics.get("overall_score", 0) * 100
            a_score = answer_metrics.get("overall_score", 0) * 100
            
            # Question card with chat button
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                    <h4 style="margin: 0;">{topic_name} - Question {question_num}</h4>
                    <div style="display: flex; gap: 1rem;">
                        <span style="background: #4CAF50; color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">Q: {q_score:.0f}%</span>
                        <span style="background: #2196F3; color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">A: {a_score:.0f}%</span>
                    </div>
                </div>
                
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">{question}</p>
                
                <p style="font-size: 1rem; margin-bottom: 1rem; color: #888;">{answer[:200]}...</p>
                
                <div style="text-align: center; margin-top: 1rem;">
                    <button class="aesthetic-btn" onclick="window.location.reload()">
                        💬 Chat About This Question
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
    
    # Chat container - moved to top
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat history header
    st.markdown("### 📜 Chat History")
    
    # Display messages
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Enhanced display for agent responses
            if 'dashboard_generation' in message.get('tools_used', []):
                st.markdown(f"""
                <div class="chat-message">
                    <strong>AI Assistant:</strong>  Dashboard generated successfully! Scroll down to view.
                </div>
                """, unsafe_allow_html=True)
            else:
                # Show metrics, sources, and metadata for all responses
                st.markdown(f"""
                <div class="chat-message">
                    <strong>AI Assistant:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # Always show metrics if available
                if message.get('metrics'):
                    with st.expander(" Response Metrics", expanded=True):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric(" Overall", f"{message['metrics'].get('overall_score', 0)*100:.0f}%")
                        with col2:
                            st.metric(" Coverage", f"{message['metrics'].get('coverage_final', 0)*100:.0f}%")
                        with col3:
                            st.metric(" Specificity", f"{message['metrics'].get('specificity_final', 0)*100:.0f}%")
                        with col4:
                            st.metric(" Groundedness", f"{message['metrics'].get('groundedness_final', 0)*100:.0f}%")
                
                # Always show sources if available
                if message.get('sources'):
                    with st.expander(" Source Documents", expanded=True):
                        for j, source in enumerate(message['sources'][:5], 1):
                            st.write(f"**Source {j}:**")
                            st.write(f"• **Content:** {source.get('content', 'N/A')}")
                            st.write(f"• **Similarity Score:** {source.get('score', 0):.2f}")
                            
                            # Show metadata
                            if source.get('metadata'):
                                st.write("• **Metadata:**")
                                metadata = source['metadata']
                                
                                # Show document link if available
                                if metadata.get('source_file'):
                                    st.write(f"  - **Document:** {metadata['source_file']}")
                                if metadata.get('dataset'):
                                    st.write(f"  - **Dataset:** {metadata['dataset']}")
                                if metadata.get('content_type'):
                                    st.write(f"  - **Type:** {metadata['content_type']}")
                                if metadata.get('id'):
                                    st.write(f"  - **ID:** {metadata['id']}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Regular chat interface
    st.markdown("### 💬 Direct Chat")
    st.markdown("Ask me anything about the data, analytics, or request visualizations...")
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="What would you like to know?",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button(" Send", type="primary", use_container_width=True)
    
    # Clear button below input
    clear_button = st.button(" Clear Chat History", use_container_width=True)
    
    # Clear chat history
    if clear_button:
        st.session_state.messages = []
        st.session_state.chat_context = []
        st.rerun()
    
    # Send message
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Get response from agent
        try:
            # First check if backend is available
            backend_check = requests.get("http://localhost:8001/", timeout=5)
            
            if backend_check.status_code != 200:
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': "Backend service is not responding properly. Please check if the backend server is running on localhost:8001.",
                    'timestamp': datetime.now()
                })
            else:
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
                    ai_response = result.get('response', 'Sorry, I couldn\'t process that request.')
                    sources = result.get('sources', [])
                    metrics = result.get('metrics', {})
                    tools_used = result.get('tools_used', [])
                    
                    # Store response with full metadata
                    st.session_state.messages.append({
                        'role': 'assistant', 
                        'content': ai_response,
                        'sources': sources,
                        'metrics': metrics,
                        'tools_used': tools_used,
                        'timestamp': datetime.now()
                    })
                    
                    # Handle dashboard generation
                    if 'dashboard_generation' in tools_used:
                        st.success(' Dashboard code generated successfully!')
                        
                        # Display metrics and sources first
                        if metrics:
                            st.markdown("###  Response Metrics")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric(" Overall", f"{metrics.get('overall_score', 0)*100:.0f}%")
                            with col2:
                                st.metric(" Coverage", f"{metrics.get('coverage_final', 0)*100:.0f}%")
                            with col3:
                                st.metric(" Specificity", f"{metrics.get('specificity_final', 0)*100:.0f}%")
                            with col4:
                                st.metric(" Insightfulness", f"{metrics.get('insightfulness_final', 0)*100:.0f}%")
                        
                        if sources:
                            st.markdown("###  Source Documents")
                            for j, source in enumerate(sources[:3], 1):
                                st.write(f"**Source {j}:**")
                                st.write(f"• **Content:** {source.get('content', 'N/A')}")
                                st.write(f"• **Similarity Score:** {source.get('score', 0):.2f}")
                                
                                # Show metadata
                                if source.get('metadata'):
                                    st.write("• **Metadata:**")
                                    st.json(source['metadata'])
                        
                        # Extract and clean dashboard code
                        dashboard_code = ai_response.strip()
                        
                        # Remove any leading/trailing quotes and clean
                        if '```python' in dashboard_code:
                            dashboard_code = dashboard_code.split('```python')[1].split('```')[0]
                        elif '```' in dashboard_code:
                            dashboard_code = dashboard_code.split('```')[1].split('```')[0]
                        
                        # Remove problematic patterns
                        dashboard_code = dashboard_code.strip().strip('"\'')
                        dashboard_code = dashboard_code.replace('st.set_page_config(', '# st.set_page_config(')
                        dashboard_code = dashboard_code.replace('"""', '')
                        
                        # Display in canvas
                        st.markdown("###  Generated Dashboard")
                        st.markdown("""
                        <div class="canvas-container">
                            <div class="canvas-header">
                                <div class="canvas-title">
                                     Generated Dashboard
                                </div>
                                <div class="canvas-actions">
                                    <button class="canvas-btn" onclick="window.location.reload()"> Refresh</button>
                                    <button class="canvas-btn" onclick="window.print()"> Print</button>
                                </div>
                            </div>
                            <div class="canvas-content">
                        </div>
                        """, unsafe_allow_html=True)
                        
                        try:
                            # Create a safe execution environment
                            exec_globals = {
                                'st': st,
                                'pd': pd,
                                'px': px,
                                'go': go,
                                'np': np,
                                'datetime': datetime,
                                'base64': base64
                            }
                            
                            # Execute the dashboard code
                            exec(dashboard_code, exec_globals)
                            st.success(" Dashboard executed successfully!")
                            
                        except Exception as e:
                            st.error(f" Dashboard execution failed: {e}")
                            st.write("This might be due to missing dependencies or incompatible Streamlit components.")
                            
                            # Show the problematic code for debugging
                            with st.expander(" Debug - Generated Code"):
                                st.code(dashboard_code, language='python')
                    
                    else:
                        st.session_state.messages.append({
                            'role': 'assistant',
                            'content': f"Backend service returned error: {response.status_code}. Please check the backend logs.",
                            'timestamp': datetime.now()
                        })
                        
        except requests.exceptions.RequestException as e:
            st.session_state.messages.append({
                'role': 'assistant',
                'content': f"Connection error: Unable to reach the backend service. Please ensure the backend is running on localhost:8001. Error: {str(e)}",
                'timestamp': datetime.now()
            })
        except Exception as e:
            st.session_state.messages.append({
                'role': 'assistant',
                'content': f"Unexpected error: {str(e)}",
                'timestamp': datetime.now()
            })
        
        # Only rerun if no dashboard was generated and no navigation intent
        if 'dashboard_generation' not in tools_used:
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: white; opacity: 0.7;">'
        ' Powered by 6sense Revenue AI | Advanced Analytics & Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )
