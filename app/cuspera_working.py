import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="Cuspera", page_icon="🚀", layout="wide")

st.title("🚀 Cuspera B2B Intelligence Platform")

API_URL = "http://localhost:8000"

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose Page", ["Chat", "Analytics", "ROI Calculator", "Status"])

if page == "Chat":
    st.header("💬 AI Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input
    if prompt := st.chat_input("Ask about B2B software, ROI, etc."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": prompt, "product": "6sense"},
                        timeout=15
                    )
                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result["answer"]
                        st.write(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    else:
                        st.error("API Error")
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "Analytics":
    st.header("📊 Analytics Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Queries", "1,247", "↑ 12%")
    with col2:
        st.metric("Avg ROI", "3.5x", "↑ 0.3x")
    with col3:
        st.metric("Success Rate", "94%", "↑ 2%")
    
    st.subheader("Performance Chart")
    chart_data = {"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "Queries": [120, 135, 125, 145, 160]}
    st.bar_chart(chart_data)

elif page == "ROI Calculator":
    st.header("📈 ROI Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        company_size = st.selectbox("Company Size", ["1-10", "11-50", "51-200", "201-500", "500+"])
        industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance"])
        revenue = st.number_input("Annual Revenue ($)", min_value=0, value=1000000)
    
    with col2:
        software = st.selectbox("Software", ["6sense", "Demandbase", "Bombora"])
        implementation = st.slider("Implementation (months)", 1, 12, 3)
        growth = st.slider("Expected Growth (%)", 10, 200, 50)
    
    if st.button("Calculate ROI"):
        base_roi = 3.5
        size_mult = {"1-10": 0.8, "11-50": 1.0, "51-200": 1.2, "201-500": 1.5, "500+": 2.0}
        calculated_roi = base_roi * size_mult[company_size] * (1 + growth/100)
        
        st.success(f"🎯 Calculated ROI: {calculated_roi:.2f}x")
        st.write(f"Expected return: ${revenue * calculated_roi:,.0f}")
        st.write(f"Payback period: {implementation} months")

elif page == "Status":
    st.header("⚙️ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            if response.status_code == 200:
                st.success("🤖 API Online")
                health_data = response.json()
                st.json(health_data)
            else:
                st.error("🤖 API Error")
        except:
            st.error("🤖 API Offline")
    
    with col2:
        st.info("📊 Vector Store")
        st.write("Documents: 9,602")
        st.write("Cache: Active")
    
    with col3:
        st.info("🌐 System")
        st.write("Uptime: 99.9%")
        st.write("Response Time: 1.2s")

st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ for B2B Success")
