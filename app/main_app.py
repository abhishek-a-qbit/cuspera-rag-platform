"""
Main Application Entry Point
Launches the enhanced AI agent interface
"""

import streamlit as st
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the enhanced chat interface
from enhanced_chat_interface import *

# This will run the enhanced chat interface
if __name__ == "__main__":
    st.write("🚀 Loading 6sense AI Agent...")
