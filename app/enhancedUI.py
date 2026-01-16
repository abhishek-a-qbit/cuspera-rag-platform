import streamlit as st
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Set page configuration with beautiful theme
st.set_page_config(
    page_title="🚀 Cuspera Supreme - Beautiful Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with beautiful aesthetics
st.markdown("""
<style>
    /* Import beautiful fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        font-family: 'Inter', sans-serif;
        background-attachment: fixed;
    }
    
    /* Animated background particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="particles" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.05)"/><circle cx="10" cy="50" r="0.5" fill="rgba(255,255,255,0.05)"/><circle cx="90" cy="30" r="0.5" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23particles)"/></svg>');
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Main header with glassmorphism */
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Glassmorphic cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.3);
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
        transition: all 0.6s ease;
    }
    
    .metric-card:hover::before {
        animation: shimmer 0.6s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    }
    
    /* Chat messages with enhanced styling */
    .chat-message {
        margin: 1rem 0;
        padding: 1.5rem;
        border-radius: 20px;
        animation: slideIn 0.5s ease;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.5s ease;
    }
    
    .agent-message {
        background: rgba(255,255,255,0.95);
        color: #2c3e50;
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
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
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Enhanced inputs */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.95);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        background: rgba(255,255,255,1);
    }
    
    /* Sidebar with glassmorphism */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online .status-dot {
        background: #4CAF50;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    /* Feature showcase */
    .feature-showcase {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Hide streamlit elements */
    .stDeployButton {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255,255,255,0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Add floating particles
st.markdown('<div class="particles"></div>', unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Create beautiful logo
def create_logo():
    """Create a beautiful logo"""
    fig, ax = plt.subplots(figsize=(3, 3), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Create gradient circles
    for i in range(3, 0, -1):
        circle = plt.Circle((5, 5), i, color=['#667eea', '#764ba2', '#f093fb'][3-i], alpha=0.3)
        ax.add_patch(circle)
    
    # Add text
    ax.text(5, 5.5, 'Cuspera', fontsize=20, fontweight='bold', 
            ha='center', va='center', color='#667eea')
    ax.text(5, 4.5, 'Supreme', fontsize=8, 
            ha='center', va='center', color='#764ba2')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return img_str

# Sidebar with enhanced design
with st.sidebar:
    # Logo and branding
    try:
        logo_img = create_logo()
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{logo_img}" 
                 style="width: 100px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
            <h3 style="margin: 1rem 0 0.5rem 0; color: white;">Cuspera Supreme</h3>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Advanced Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="margin: 0; color: white; font-size: 3rem;">🚀</h1>
            <h3 style="margin: 0.5rem 0; color: white;">Cuspera Supreme</h3>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Advanced Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    
    nav_items = [
        ('🏠 Home', 'home'),
        ('💬 AI Chat', 'chat'),
        ('📊 Dashboard', 'dashboard'),
        ('📈 Analytics', 'analytics'),
        ('💰 ROI Calculator', 'roi'),
        ('📋 Reports', 'reports'),
        ('🎨 Infographics', 'infographics'),
        ('⚙️ Settings', 'settings')
    ]
    
    for label, page in nav_items:
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()
    
    # System status
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    # Check backend status
    try:
        response = requests.get("http://localhost:8001/", timeout=2)
        status = "online"
        status_color = "#4CAF50"
        status_text = "Online"
    except:
        status = "offline"
        status_color = "#f44336"
        status_text = "Offline"
    
    st.markdown(f"""
    <div class="status-indicator status-{status}">
        <div class="status-dot"></div>
        <span>Backend {status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick metrics
    st.markdown("### 📈 Quick Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Calls", "1,247", "+12%")
    with col2:
        st.metric("Response Time", "245ms", "-8%")

# Main content
if st.session_state.current_page == 'home':
    # Hero section
    st.markdown("""
    <div class="main-header">
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 4rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🚀 Welcome to Cuspera Supreme
            </h1>
            <h2 style="font-size: 2rem; margin-bottom: 1rem; opacity: 0.9;">
                Advanced Analytics & Intelligence Platform
            </h2>
            <p style="font-size: 1.3rem; opacity: 0.8; margin: 0;">
                Experience the future of revenue intelligence with AI-powered analytics, real-time dashboards, and predictive insights
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("### ✨ Features & Capabilities")
    
    features = [
        {
            'icon': '🤖',
            'title': 'AI-Powered Chat',
            'description': 'Intelligent conversational interface for all your analytics needs'
        },
        {
            'icon': '📊',
            'title': 'Instant Dashboards',
            'description': 'Generate beautiful, interactive dashboards with a single command'
        },
        {
            'icon': '📈',
            'title': 'Advanced Analytics',
            'description': 'Comprehensive analytics with trends, insights, and predictions'
        },
        {
            'icon': '💰',
            'title': 'ROI Calculator',
            'description': 'Detailed ROI analysis with NPV, IRR, and payback periods'
        },
        {
            'icon': '📋',
            'title': 'Report Generator',
            'description': 'Automated report generation with visualizations and insights'
        },
        {
            'icon': '🎨',
            'title': 'Infographics',
            'description': 'Beautiful visual content for presentations and marketing'
        }
    ]
    
    # Create feature grid
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="glass-card">
                <div class="feature-icon">{feature['icon']}</div>
                <h4 style="color: white; margin: 1rem 0 0.5rem 0;">{feature['title']}</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 0;">{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick start section
    st.markdown("### 🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Start Chatting", use_container_width=True):
            st.session_state.current_page = 'chat'
            st.rerun()
    
    with col2:
        if st.button("📊 Create Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col3:
        if st.button("📈 View Analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.rerun()

elif st.session_state.current_page == 'chat':
    # Chat interface
    st.markdown("""
    <div class="main-header">
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">💬 AI Assistant</h1>
            <h2 style="font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9;">
                Your Intelligent Analytics Companion
            </h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message agent-message">
                <strong>🤖 AI Assistant:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message...",
            placeholder="Ask me about dashboards, analytics, ROI, or reports...",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("📤 Send", use_container_width=True):
            if user_input:
                st.session_state.messages.append({'role': 'user', 'content': user_input})
                
                # Get AI response
                with st.spinner('Thinking...'):
                    try:
                        response = requests.post(
                            "http://localhost:8001/advanced-chat",
                            json={"message": user_input, "session_id": "beautiful_ui"},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            ai_response = result.get('response', 'Sorry, I couldn\'t process that request.')
                            st.session_state.messages.append({'role': 'assistant', 'content': ai_response})
                        else:
                            st.error(f"Error: {response.status_code}")
                            
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    quick_actions = [
        "Create a comprehensive dashboard",
        "Generate analytics report",
        "Calculate ROI for marketing",
        "Show revenue trends"
    ]
    
    for action in quick_actions:
        if st.button(action, key=f"quick_{action[:10]}"):
            st.session_state.messages.append({'role': 'user', 'content': action})
            st.rerun()

elif st.session_state.current_page == 'dashboard':
    # Dashboard page
    st.markdown("""
    <div class="main-header">
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">📊 Dashboard</h1>
            <h2 style="font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9;">
                Real-time Analytics & Insights
            </h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample dashboard content
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💰 Revenue", "$4.2M", "+23%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 Conversion", "28.5%", "+5.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⭐ Quality", "8.7/10", "+0.8")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📈 ROI", "312%", "+45%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sample chart
    fig = px.line(
        x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        y=[350000, 380000, 420000, 410000, 450000, 480000],
        title="Revenue Trend",
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50', family='Inter')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Beautiful footer
st.markdown("---")
st.markdown(f"""
<div style="background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2rem; border-radius: 20px; text-align: center; 
            color: white; margin-top: 2rem;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);">
    <h3 style="margin: 0; font-size: 1.8rem;">🚀 Cuspera Supreme Platform</h3>
    <p style="margin: 0.5rem 0; opacity: 0.9; font-size: 1.1rem;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
    <p style="margin: 0; opacity: 0.8; font-size: 1rem;">
        ✨ Powered by Advanced Analytics | Real-time Intelligence | Predictive Insights ✨
    </p>
    <div style="margin-top: 1rem;">
        <div class="status-indicator status-online">
            <div class="status-dot"></div>
            <span>System Operational</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
