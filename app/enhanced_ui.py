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
    
    if st.button("� Question Generator", use_container_width=True, key="nav_questions"):
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
            
            # Temperature slider for creativity
            temperature = st.slider(
                "Creativity (Temperature):",
                min_value=0.1,
                max_value=2.0,
                value=0.7,
                step=0.1,
                help="Higher values = more creative, lower values = more focused"
            )
            
            # Output format option
            output_format = st.selectbox(
                "Output Format:",
                options=["Standard", "JSON", "Detailed"],
                help="Choose how questions are formatted in the output"
            )
            
            custom_prompt = st.text_area(
                "🔍 Custom Prompt (Optional)",
                value="",
                height=100,
                help="Enter a custom prompt for question generation. Leave empty to use default settings.",
                placeholder="Example: Generate questions about implementation challenges and ROI for enterprise clients..."
            )
        
        with col2:
            st.info("""
            **Advanced Features Available:**
            - ✅ Real LLM grading (not proxy scores)
            - ✅ Real groundedness calculation
            - ✅ Answer metrics included
            - ✅ NLP-based specificity
            - ✅ Semantic similarity scoring
            - ✅ Temperature control for creativity
            - ✅ JSON output format option
            - ✅ Amazon Rufus style display
            - ✅ Direct chat redirection
            """)
            
            # JSON Generator Info
            if output_format == "JSON":
                st.success("""
                📋 **JSON Mode Enabled**
                Questions will be generated in structured JSON format with:
                - Question text
                - Answer text  
                - Metrics data
                - Source information
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
                            "include_rag": include_rag,
                            "temperature": temperature,
                            "output_format": output_format.lower(),
                            "custom_prompt": custom_prompt if custom_prompt.strip() else None
                        },
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("status") == "success":
                            # Store results exactly like cuspera_working.py
                            st.session_state.question_gen_results = {
                                "questions": result.get("questions", []),
                                "metrics": result.get("metrics", {}),
                                "product": target_product,
                                "target_count": target_count
                            }
                            st.success(f"✅ Generated {len(result.get('questions', []))} questions successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # Display Results - exactly like cuspera_working.py
    if st.session_state.question_gen_results:
        results = st.session_state.question_gen_results
        metrics = results.get("metrics", {})
        product_name = results.get('product', 'Unknown Product')
        
        st.markdown(f"### 🎯 Generation Results for {product_name}")
        
        # Top-level metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Questions Generated", len(results.get("questions", [])))
        with col2:
            st.metric("Avg Question Score", f"{metrics.get('overall_q_avg', 0)*100:.1f}%")
        with col3:
            st.metric("Avg Answer Score", f"{metrics.get('overall_a_avg', 0)*100:.1f}%")
        with col4:
            st.metric("Total Sources", metrics.get('total_sources', 0))
        
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
                line_color='#ff6b6b'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Question vs Answer Performance"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Chart generation failed: {e}")
        
        # Detailed Q&A table - exactly like cuspera_working.py
        st.markdown("### 📋 Detailed Question & Answer Metrics")
        
        # Display Q&A pairs with expanders for full text
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
                        "Pass": ["—", "—", "—", "—", "✅" if a_metrics.get("overall_pass") else "❌"]
                    })
                    st.dataframe(a_metrics_df, use_container_width=True, hide_index=True)
                
                st.markdown(f"**📚 Sources Retrieved:** {q.get('retrieved_sources', 0)}")
                st.markdown(f"**🔗 Context Source:** {q.get('context_source', '')}")
                
                # Display sources if available
                sources = q.get('sources', [])
                if sources:
                    st.markdown("##### 📚 Source Documents")
                    for j, source in enumerate(sources[:3], 1):
                        st.write(f"**Source {j}:**")
                        st.write(f"• **Content:** {source.get('content', 'N/A')}")
                        st.write(f"• **Similarity Score:** {source.get('score', 0):.2f}")
                        
                        # Show metadata
                        if source.get('metadata'):
                            st.write("• **Metadata:**")
                            metadata = source['metadata']
                            
                            if metadata.get('source_file'):
                                st.write(f"  - **Document:** {metadata['source_file']}")
                            if metadata.get('dataset'):
                                st.write(f"  - **Dataset:** {metadata['dataset']}")
                            if metadata.get('content_type'):
                                st.write(f"  - **Type:** {metadata['content_type']}")
                            if metadata.get('id'):
                                st.write(f"  - **ID:** {metadata['id']}")
                
                # Amazon Rufus style chat redirection button
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button(f"💬 Chat About This Question", key=f"chat_about_question_{i}", type="primary", use_container_width=True):
                        # Store selected question in session state
                        st.session_state[f"selected_question_{i}"] = {
                            "question": q.get("question", ""),
                            "answer": q.get("answer", ""),
                            "metrics": q_metrics,
                            "answer_metrics": a_metrics,
                            "sources": sources,
                            "retrieved_sources": q.get('retrieved_sources', 0),
                            "context_source": q.get('context_source', ''),
                            "topic_name": product_name,
                            "question_index": i
                        }
                        # Switch to chat page
                        st.session_state.page_selector = "💬 Chat Assistant"
                        st.success(f"🎯 Question {i} selected for chat! Switching to Chat Assistant...")
                        st.rerun()
                
                st.markdown("---")
        
        # Export options
        st.markdown("### 📤 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV Export
            if st.button("� Download CSV", use_container_width=True):
                try:
                    import pandas as pd
                    from datetime import datetime
                    
                    # Create DataFrame for export
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
                            "Q_Overall_Score": q_m.get("overall_score", 0),
                            "Q_Coverage": q_m.get("coverage_final", 0),
                            "Q_Specificity": q_m.get("specificity_final", 0),
                            "Q_Insightfulness": q_m.get("insightfulness_final", 0),
                            "Q_Groundedness": q_m.get("groundedness_final", 0),
                            "Q_Pass": q_m.get("overall_pass", False),
                            "A_Overall_Score": a_m.get("overall_score", 0),
                            "A_Coverage": a_m.get("coverage_final", 0),
                            "A_Specificity": a_m.get("specificity_final", 0),
                            "A_Insightfulness": a_m.get("insightfulness_final", 0),
                            "A_Groundedness": a_m.get("groundedness_final", 0),
                            "A_Pass": a_m.get("overall_pass", False)
                        })
                    
                    df = pd.DataFrame(export_data)
                    csv_data = df.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"qa_{product_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"CSV generation failed: {str(e)}")
        
        with col2:
            # FAQ Export - exactly like cuspera_working.py
            if st.button("📋 Generate FAQ Format", use_container_width=True):
                try:
                    faq_data = []
                    for i, q in enumerate(results.get("questions", []), 1):
                        q_m = q.get("metrics", {})
                        a_m = q.get("answer_metrics", {})
                        
                        # Create FAQ entry with exact structure from cuspera_working.py
                        faq_entry = {
                            "question": q.get("question", ""),
                            "answer": q.get("answer", ""),
                            "section": "General",  # Can be customized
                            "context": [
                                {
                                    "name": q.get("topic_name", "6sense Analytics"),  # Use generated topic
                                    "code": f"Q_{i}",
                                    "type": "capability",
                                    "score": q_m.get("overall_score", 0)
                                }
                            ],
                            "evidence": q.get("enhanced_evidence", [
                                {
                                    "link": f"#question_{i}",
                                    "type": "generated",
                                    "score": q_m.get("groundedness_final", 0)
                                }
                            ])
                        }
                        faq_data.append(faq_entry)
                    
                    # Convert to JSON and provide download - exactly like cuspera_working.py
                    faq_json = json.dumps(faq_data, indent=2)
                    st.download_button(
                        label="📋 Download FAQ JSON",
                        data=faq_json,
                        file_name=f"faq_{product_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        mime="application/json"
                    )
                    
                except Exception as e:
                    st.error(f"FAQ generation failed: {str(e)}")
        
        with col3:
            if st.button("💬 Go to Chat Assistant", type="primary", use_container_width=True):
                st.session_state.page_selector = "💬 Chat Assistant"
                st.rerun()
            

def display_agent_response(response_data: Dict, question_data: Dict):
    """Display agent response exactly like rufus_chat_interface.py"""
    response = response_data.get("response", "")
    sources = response_data.get("sources", [])
    metrics = response_data.get("metrics", {})
    
    # Response container
    st.subheader("🤖 AI Agent Response")
    
    # Response content
    st.write(response)
    
    # Sources section
    if sources:
        st.markdown("##### 📚 Source Documents")
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
                st.text_area("Content", value=preview, height=150, disabled=True, label_visibility="collapsed", key=f"preview_msg_{doc_id[:8]}")
    
    # Metrics section
    if metrics:
        st.markdown("##### 📊 Response Quality Metrics")
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
    st.markdown("##### 🔄 Follow-up Questions")
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

else:  # Chat Assistant page - Amazon Rufus Style
    # Initialize chat state like rufus_chat_interface.py
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = None
    if "agent_responses" not in st.session_state:
        st.session_state.agent_responses = {}
    
    # Chat history header - moved to top for ChatGPT-like experience
    if st.session_state.chat_messages:
        st.subheader("📜 Chat History")
        
        # Display chat messages with expanders for better UX
        for msg_index, msg in enumerate(st.session_state.chat_messages[-10:], 1):  # Show last 10 messages
            with st.expander(f"**{msg['type'].title()} {msg_index}**", expanded=False):
                if msg["type"] == "user":
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4CAF50, #45a049); 
                                color: white; padding: 15px 20px; border-radius: 18px 18px 4px 18px; 
                                margin: 10px 0; max-width: 80%; margin-left: auto;">
                        <strong>You:</strong> {msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Enhanced agent message display
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #2196F3, #1976D2); 
                                color: white; padding: 15px 20px; border-radius: 18px 18px 18px 4px; 
                                margin: 10px 0; max-width: 80%;">
                        <strong>🤖 Assistant:</strong> {msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show sources if available - exactly like rufus_chat_interface.py
                if msg.get("sources") and len(msg["sources"]) > 0:
                    with st.expander("📚 Sources for this response", expanded=False):
                        for i, source in enumerate(msg["sources"][:3], 1):  # Show top 3 sources
                            # Get actual content and metadata
                            content = source.get("content", "")
                            metadata = source.get("metadata", {})
                            similarity_score = source.get("score", 0)
                            
                            # Extract key metadata fields
                            doc_id = metadata.get("id", f"doc_{i}")
                            content_type = metadata.get("content_type", "unknown")
                            dataset = metadata.get("dataset", "unknown")
                            source_file = metadata.get("source", "unknown")
                            
                            with st.expander(f"📄 Source {i} ({similarity_score:.1%} match)", expanded=False):
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
                                st.text_area("Content", value=preview, height=150, disabled=True, label_visibility="collapsed", key=f"preview_msg_{msg_index}_{doc_id[:8]}")
                
                # Show metrics if available - exactly like rufus_chat_interface.py
                if msg.get("metrics") and msg["metrics"]:
                    with st.expander("📊 Quality Metrics", expanded=False):
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
    
    # Check if we have generated questions from question generator
    if st.session_state.get("question_gen_results"):
        questions = st.session_state.question_gen_results.get("questions", [])
        
        if questions:
            st.markdown("### 📋 Generated Questions - Click to Chat")
            
            # Display question cards exactly like rufus_chat_interface.py
            for i, question_data in enumerate(questions, 1):
                # Simple question card like rufus_chat_interface.py
                with st.container():
                    # Header with scores
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(f"🤔 Question {i}")
                    with col2:
                        q_metrics = question_data.get("metrics", {})
                        a_metrics = question_data.get("answer_metrics", {})
                        q_score = q_metrics.get("overall_score", 0) * 100
                        a_score = a_metrics.get("overall_score", 0) * 100
                        st.markdown(f"🟢 Q: {q_score:.0f}% | 🔵 A: {a_score:.0f}%")
                    
                    # Question text
                    st.write(question_data.get("question", ""))
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        sources_count = question_data.get("retrieved_sources", 0)
                        st.metric("📚 Sources", sources_count)
                    with col2:
                        st.metric("🎯 Coverage", f"{q_metrics.get('coverage_final', 0)*100:.0f}%")
                    with col3:
                        st.metric("📊 Specificity", f"{q_metrics.get('specificity_final', 0)*100:.0f}%")
                    
                    # Chat button - exactly like rufus_chat_interface.py
                    if st.button(f"💬 Chat About This Question", key=f"chat_btn_{i}"):
                        st.session_state.selected_question = i
                        st.rerun()
                    
                    st.divider()
            
            # Check if this question was clicked - exactly like rufus_chat_interface.py
            if st.session_state.get("selected_question") == i:
                # Generate agent response for this question
                if i not in st.session_state.agent_responses:
                    with st.spinner("🤖 Thinking..."):
                        question_text = questions[i-1].get("question", "")
                        
                        try:
                            response = requests.post(
                                "http://localhost:8001/advanced-chat",
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
                    # Display agent response - exactly like rufus_chat_interface.py
                    response_data = st.session_state.agent_responses[i]
                    display_agent_response(response_data, questions[i-1])
    
    # Chat input area - exactly like rufus_chat_interface.py
    st.markdown("### 💬 Direct Chat")
    
    # Handle quick actions if any
    user_input = ""
    if hasattr(st.session_state, 'quick_action'):
        user_input = st.text_input(
            "Ask me anything about 6sense, analytics, ROI, or visualizations...",
            value=user_input,
            key="user_input",
            placeholder="e.g., 'Generate analytics report', 'Calculate ROI', 'Create dashboard', 'What are 6sense features?'"
        )
    else:
        user_input = st.text_input(
            "Ask me anything about 6sense, analytics, ROI, or visualizations...",
            key="user_input",
            placeholder="Try: 'Show me revenue trends' or 'Create a dashboard for customer analytics'"
        )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        send_button = st.button("🚀 Send", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    # Send message
    if send_button and user_input:
        # Add user message
        st.session_state.chat_messages.append({
            "type": "user",
            "message": user_input,
            "timestamp": datetime.now()
        })
        
        # Get response from agent
        try:
            # First check if advanced agent is available
            advanced_agent_check = requests.get("http://localhost:8001/health", timeout=2)
            
            # If advanced agent is available, use it
            if advanced_agent_check.status_code == 200:
                response = requests.post(
                    "http://localhost:8001/advanced-chat",
                    json={
                        "message": user_input,
                        "session_id": st.session_state.session_id
                    },
                    timeout=60
                )
            else:
                # Fallback to simple chat agent if advanced agent is not available
                response = requests.post(
                    "http://localhost:8001/chat",
                    json={
                        "message": user_input,
                        "session_id": st.session_state.session_id
                    },
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                agent_response = result.get("response", "I'm having trouble processing your request.")
                sources = result.get("sources", [])
                metrics = result.get("metrics", {})
                
                # Add to chat history - exactly like rufus_chat_interface.py
                st.session_state.chat_messages.append({
                    "type": "agent", 
                    "message": agent_response,
                    "sources": sources,
                    "metrics": metrics,
                    "timestamp": datetime.now()
                })
            else:
                st.session_state.chat_messages.append({
                    "type": "agent",
                    "message": f"Backend service returned error: {response.status_code}",
                    "sources": [],
                    "metrics": {},
                    "timestamp": datetime.now()
                })
                
        except requests.exceptions.RequestException as e:
            st.session_state.chat_messages.append({
                "type": "agent",
                "message": f"Connection error: Unable to reach the backend service. Please ensure that backend is running on localhost:8001. Error: {str(e)}",
                "sources": [],
                "metrics": {},
                "timestamp": datetime.now()
            })
        except Exception as e:
            st.session_state.chat_messages.append({
                "type": "agent",
                "message": f"Unexpected error: {str(e)}",
                "sources": [],
                "metrics": {},
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
