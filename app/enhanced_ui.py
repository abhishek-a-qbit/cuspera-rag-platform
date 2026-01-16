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
    page_title="🚀 Cuspera Supreme - Beautiful Dashboard",
    page_icon="🚀",
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
