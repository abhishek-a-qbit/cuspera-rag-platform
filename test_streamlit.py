import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Cuspera RAG Test",
    page_icon="🤖",
    layout="wide"
)

# API URL
API_URL = "http://localhost:8000"

st.title("🤖 Cuspera RAG Platform Test")
st.markdown("---")

# Test the API
st.header("Test ROI Query")
question = st.text_input("Enter your question:", value="What is the ROI of 6sense for a 50-person startup?")

if st.button("Get Answer"):
    if question:
        with st.spinner("Getting answer..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question, "product": "6sense"},
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Answer received!")
                    
                    st.subheader("💬 Answer")
                    st.write(result["answer"])
                    
                    st.subheader("📊 Sources")
                    if result["sources"]:
                        for i, source in enumerate(result["sources"]):
                            with st.expander(f"Source {i+1}"):
                                st.write(f"**ID:** {source.get('id', 'unknown')}")
                                st.write(f"**Content:** {source.get('content', 'No content')}")
                                st.write(f"**Metadata:** {source.get('metadata', {})}")
                    else:
                        st.info("No sources found")
                    
                    st.subheader("📈 Metrics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Confidence", f"{result.get('confidence', 0):.1%}")
                    with col2:
                        st.metric("Context", result.get('context', 'N/A'))
                    with col3:
                        st.metric("Sources", len(result.get('sources', [])))
                    
                    st.subheader("💡 Follow-up Suggestions")
                    for suggestion in result.get('follow_up_suggestions', []):
                        st.write(f"• {suggestion}")
                        
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Health check
st.header("Backend Health")
if st.button("Check Health"):
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            st.success("✅ Backend is healthy!")
            st.json(health)
        else:
            st.error(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Health check error: {e}")
