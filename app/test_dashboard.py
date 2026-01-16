import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="6sense AI Agent Dashboard Test",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 6sense AI Agent Dashboard Test")
st.markdown("Testing the enhanced AI agent's dashboard generation capabilities")

# API endpoint
API_URL = "http://localhost:8001/advanced-chat"

# User input
user_query = st.text_input(
    "Enter your query:",
    value="Create dashboard showing 6sense metrics",
    help="Try queries like: 'Create dashboard', 'Show analytics', 'Generate report', 'Calculate ROI'"
)

if st.button("Generate Response"):
    if user_query:
        with st.spinner("Processing your request..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_query, "session_id": "test_session"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display response
                    st.subheader("🤖 Agent Response")
                    
                    # Check if it's dashboard code
                    if "dashboard_generation" in result.get("tools_used", []):
                        st.success("✅ Dashboard code generated successfully!")
                        
                        # Display the code
                        with st.expander("📝 Generated Dashboard Code", expanded=True):
                            st.code(result["response"], language="python")
                        
                        # Execute the dashboard code
                        st.subheader("📊 Generated Dashboard")
                        try:
                            exec(result["response"])
                        except Exception as e:
                            st.error(f"Error executing dashboard code: {str(e)}")
                    else:
                        st.write(result["response"])
                    
                    # Display metrics
                    if result.get("metrics"):
                        st.subheader("📊 Response Metrics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Overall Score", f"{result['metrics'].get('overall_score', 0)*100:.0f}%")
                        with col2:
                            st.metric("Coverage", f"{result['metrics'].get('coverage_final', 0)*100:.0f}%")
                        with col3:
                            st.metric("Specificity", f"{result['metrics'].get('specificity_final', 0)*100:.0f}%")
                        with col4:
                            st.metric("Tools Used", len(result.get("tools_used", [])))
                    
                    # Display sources
                    if result.get("sources"):
                        st.subheader("📚 Sources")
                        for i, source in enumerate(result["sources"][:5], 1):
                            with st.expander(f"Source {i}"):
                                st.json(source)
                    
                    # Display tools used
                    if result.get("tools_used"):
                        st.subheader("🔧 Tools Used")
                        for tool in result["tools_used"]:
                            st.write(f"• {tool}")
                            
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
    else:
        st.warning("Please enter a query")

# Sample queries
st.markdown("---")
st.subheader("💡 Sample Queries to Try")
sample_queries = [
    "Create dashboard showing 6sense metrics",
    "Generate analytics report for Q3",
    "Calculate ROI for marketing campaign",
    "Show revenue trends and predictions",
    "Create infographic about customer success",
    "Generate performance report with charts"
]

for query in sample_queries:
    if st.button(query, key=f"sample_{query[:20]}"):
        st.session_state.sample_query = query
        st.rerun()

# Check if sample query was selected
if "sample_query" in st.session_state:
    st.info(f"Selected query: {st.session_state.sample_query}")
    user_query = st.session_state.sample_query
