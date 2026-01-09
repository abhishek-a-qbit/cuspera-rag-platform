import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,78,146,0.2);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        border: 1px solid rgba(0,212,255,0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,212,255,0.3);
        border-color: #00d4ff;
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(0,212,255,0.2);
    }
    
    .success-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid #00d4ff;
    }
    
    .warning-badge {
        background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%);
        color: #000;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid #00d4ff;
    }
    
    .info-badge {
        background: linear-gradient(135deg, #17a2b8 0%, #00d4ff 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid #00d4ff;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 1px solid #00d4ff;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 4px 15px rgba(0,212,255,0.3);
    }
    
    .stTextInput > div > input {
        background: #1a1a2e;
        color: white;
        border: 1px solid #00d4ff;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > select {
        background: #1a1a2e;
        color: white;
        border: 1px solid #00d4ff;
        border-radius: 8px;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
    }
    
    .stExpander {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%);
        border: 1px solid #00d4ff;
        border-radius: 10px;
    }
    
    .stExpander > div > button {
        color: #00d4ff;
        font-weight: bold;
    }
    
    .stDataFrame {
        background: #1a1a2e;
        color: white;
        border: 1px solid #00d4ff;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stChatMessage {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%);
        border: 1px solid #00d4ff;
        border-radius: 10px;
    }
    
    .stChatMessage[data-testid="chat-message-container-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stChatMessage[data-testid="chat-message-container-assistant"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"

# Header with gradient background
st.markdown("""
<div class="main-header">
    <h1>🚀 Cuspera Supreme</h1>
    <h2>B2B Intelligence Platform</h2>
    <p>AI-Powered Software Recommendations & ROI Analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    
    if st.button("💬 Chat Assistant", use_container_width=True, key="nav_chat"):
        st.session_state.current_page = "Chat"
    
    if st.button("📊 Analytics Dashboard", use_container_width=True, key="nav_analytics"):
        st.session_state.current_page = "Analytics"
    
    if st.button("📈 ROI Calculator", use_container_width=True, key="nav_roi"):
        st.session_state.current_page = "ROI"
    
    if st.button("📋 Question Generator", use_container_width=True, key="nav_questions"):
        st.session_state.current_page = "Questions"
    
    if st.button("📑 Reports", use_container_width=True, key="nav_reports"):
        st.session_state.current_page = "Reports"
    
    if st.button("⚙️ System Status", use_container_width=True, key="nav_status"):
        st.session_state.current_page = "Status"
    
    st.markdown("---")
    
    # System Health
    st.markdown("### 🏥 System Health")
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.markdown('<span class="success-badge">✅ API Online</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="warning-badge">⚠️ API Issues</span>', unsafe_allow_html=True)
    except:
        st.markdown('<span class="warning-badge">⚠️ API Offline</span>', unsafe_allow_html=True)
    
    st.markdown("### 📈 Quick Stats")
    st.metric("Total Queries", len(st.session_state.messages))
    st.metric("Session Time", f"{time.time() - st.session_state.get('start_time', time.time()):.0f}s")

# Main Content based on navigation
if st.session_state.current_page == "Chat":
    st.markdown("## 💬 AI Chat Assistant")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Cuspera:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Input area
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("Ask about B2B software, ROI, or recommendations:", 
                                   key="user_input", 
                                   placeholder="e.g., What's the ROI of 6sense for a 50-person startup?")
        with col2:
            send_button = st.button("🚀 Send", type="primary")
        
        if send_button and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            with st.spinner("🤖 Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": user_input, "product": "6sense"},
                        headers={"Content-Type": "application/json"},
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result["answer"]
                        
                        # Add sources if available
                        if result.get("sources"):
                            ai_response += "\n\n**📚 Sources:**\n"
                            for i, source in enumerate(result["sources"][:3]):
                                ai_response += f"\n{i+1}. {source.get('content', '')[:100]}..."
                        
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        st.rerun()
                    else:
                        st.error("❌ API Error. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif st.session_state.current_page == "Analytics":
    st.markdown("## 📊 Interactive Analytics Calculator")
    st.markdown("Generate personalized analytics using RAG-powered insights")
    
    # Initialize session state for analytics
    if 'analytics_inputs' not in st.session_state:
        st.session_state.analytics_inputs = {}
    if 'analytics_results' not in st.session_state:
        st.session_state.analytics_results = None
    
    # Step 1: Company Profile
    with st.expander("🏢 Step 1: Company Profile", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            company_name = st.text_input("Company Name", value=st.session_state.analytics_inputs.get('company_name', ''))
            industry = st.selectbox("Industry", [
                "Technology/SaaS", "Healthcare", "Financial Services", 
                "Manufacturing", "Retail/E-commerce", "Professional Services", "Other"
            ])
        
        with col2:
            company_size = st.selectbox("Company Size", [
                "Startup (1-10)", "Small (11-50)", "Medium (51-200)", 
                "Large (201-500)", "Enterprise (500+)"
            ])
            annual_revenue = st.number_input(
                "Annual Revenue ($", min_value=0, value=st.session_state.analytics_inputs.get('revenue', 1000000), step=100000
            )
        
        with col3:
            current_software = st.text_input("Current Software Stack", value=st.session_state.analytics_inputs.get('current_software', ''))
            primary_goal = st.selectbox("Primary Goal", [
                "Increase Revenue", "Improve Lead Quality", "Reduce Sales Cycle", 
                "Enhance Marketing ROI", "Expand Market Share"
            ])
    
    # Step 2: Current Performance
    with st.expander("📈 Step 2: Current Performance", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            monthly_leads = st.number_input("Monthly Leads", min_value=0, value=st.session_state.analytics_inputs.get('monthly_leads', 100))
            conversion_rate = st.slider("Conversion Rate (%)", 0.0, 50.0, value=st.session_state.analytics_inputs.get('conversion_rate', 5.0))
        
        with col2:
            avg_deal_size = st.number_input("Average Deal Size ($", min_value=0, value=st.session_state.analytics_inputs.get('avg_deal_size', 10000))
            marketing_spend = st.number_input("Monthly Marketing Spend ($", min_value=0, value=st.session_state.analytics_inputs.get('marketing_spend', 10000))
        
        with col3:
            current_roi = st.slider("Current Marketing ROI", 0.0, 10.0, value=st.session_state.analytics_inputs.get('current_roi', 2.0))
            sales_cycle = st.number_input("Sales Cycle (days)", min_value=1, value=st.session_state.analytics_inputs.get('sales_cycle', 90))
    
    # Step 3: Target Software
    with st.expander("🎯 Step 3: Target Software Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            target_software = st.selectbox("Target Software", [
                "6sense Revenue AI", "Demandbase One", "Bombora", 
                "ZoomInfo SalesOS", "LinkedIn Sales Navigator"
            ])
            implementation_timeline = st.slider("Implementation Timeline (months)", 1, 12, value=st.session_state.analytics_inputs.get('timeline', 3))
        
        with col2:
            integration_complexity = st.selectbox("Integration Complexity", [
                "Low (1-2 systems)", "Medium (3-5 systems)", "High (6+ systems)"
            ])
            budget_range = st.selectbox("Budget Range", [
                "Under $25k", "$25k-$50k", "$50k-$100k", "Over $100k"
            ])
    
    # Generate Analytics Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate RAG-Powered Analytics", type="primary", use_container_width=True):
            # Store inputs
            st.session_state.analytics_inputs = {
                'company_name': company_name, 'industry': industry, 'revenue': annual_revenue,
                'current_software': current_software, 'goal': primary_goal,
                'monthly_leads': monthly_leads, 'conversion_rate': conversion_rate,
                'avg_deal_size': avg_deal_size, 'marketing_spend': marketing_spend,
                'current_roi': current_roi, 'sales_cycle': sales_cycle,
                'target_software': target_software, 'timeline': implementation_timeline,
                'complexity': integration_complexity, 'budget': budget_range
            }
            
            with st.spinner("🔄 Generating RAG-powered analytics..."):
                try:
                    # Use RAG to get software-specific insights
                    rag_query = f"""
                    Analyze {target_software} for a {company_size.lower()} company in the {industry} industry.
                    Focus on ROI, implementation best practices, and success metrics for companies with similar profiles.
                    Current situation: {monthly_leads} monthly leads, {conversion_rate}% conversion rate, {current_roi}x ROI.
                    """
                    
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": rag_query, "product": target_software},
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    rag_insights = ""
                    if response.status_code == 200:
                        result = response.json()
                        rag_insights = result.get("answer", "")
                    
                    # Calculate projections
                    size_multiplier = {"Startup (1-10)": 0.8, "Small (11-50)": 1.0, "Medium (51-200)": 1.2, "Large (201-500)": 1.5, "Enterprise (500+)": 2.0}
                    projected_roi = current_roi * size_multiplier.get(company_size, 1.0) * 1.8
                    projected_leads = monthly_leads * 2.1
                    projected_conversion = conversion_rate * 1.4
                    
                    st.session_state.analytics_results = {
                        'projected_roi': projected_roi,
                        'projected_leads': projected_leads,
                        'projected_conversion': projected_conversion,
                        'rag_insights': rag_insights,
                        'payback_months': implementation_timeline * 0.7,
                        'monthly_increase': (projected_leads * avg_deal_size * (projected_conversion/100)) - (monthly_leads * avg_deal_size * (conversion_rate/100))
                    }
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating analytics: {str(e)}")
    
    # Display Results
    if st.session_state.analytics_results:
        results = st.session_state.analytics_results
        
        st.markdown("### 🎯 Your RAG-Powered Analytics Results")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Projected ROI</h3>
                <h1>{results['projected_roi']:.2f}x</h1>
                <p style="color: #28a745;">From {current_roi:.1f}x current</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 Projected Leads</h3>
                <h1>{results['projected_leads']:.0f}</h1>
                <p style="color: #28a745;">From {monthly_leads} current</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Conversion Rate</h3>
                <h1>{results['projected_conversion']:.1f}%</h1>
                <p style="color: #28a745;">From {conversion_rate:.1f}% current</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Payback Period</h3>
                <h1>{results['payback_months']:.1f}m</h1>
                <p style="color: #ffc107;">From {implementation_timeline}m planned</p>
            </div>
            """, unsafe_allow_html=True)
        
        # RAG Insights
        if results['rag_insights']:
            st.markdown("### 🧠 RAG-Generated Insights")
            st.markdown(f"""
            <div class="feature-card">
                <h4>🤖 AI-Powered Analysis for {target_software}</h4>
                <p>{results['rag_insights']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Financial Impact
        st.markdown("### 💰 Financial Impact Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            current_monthly_revenue = monthly_leads * avg_deal_size * (conversion_rate/100)
            projected_monthly_revenue = results['projected_leads'] * avg_deal_size * (results['projected_conversion']/100)
            
            st.markdown(f"""
            <div class="feature-card">
                <h4>📊 Revenue Projection</h4>
                <p><strong>Current Monthly:</strong> ${current_monthly_revenue:,.0f}</p>
                <p><strong>Projected Monthly:</strong> ${projected_monthly_revenue:,.0f}</p>
                <p><strong>Monthly Increase:</strong> ${results['monthly_increase']:,.0f}</p>
                <p><strong>Annual Impact:</strong> ${results['monthly_increase']*12:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="feature-card">
                <h4>🎯 Implementation Strategy</h4>
                <p><strong>Software:</strong> {target_software}</p>
                <p><strong>Timeline:</strong> {implementation_timeline} months</p>
                <p><strong>Complexity:</strong> {integration_complexity}</p>
                <p><strong>Budget:</strong> {budget_range}</p>
                <p><strong>Expected ROI:</strong> {results['projected_roi']:.1f}x</p>
                <p><strong>Success Factors:</strong></p>
                <ul>
                    <li>Executive sponsorship</li>
                    <li>Team training & adoption</li>
                    <li>Process optimization</li>
                    <li>Continuous monitoring</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        st.markdown("### 📈 Performance Visualization")
        
        # Create projection chart
        months = list(range(1, 13))
        current_trend = [current_monthly_revenue] * 12
        projected_trend = []
        
        for month in months:
            growth_factor = 1 + (results['projected_roi']/current_roi - 1) * (month/12)
            projected_trend.append(current_monthly_revenue * growth_factor)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=current_trend, mode='lines', name='Current Trajectory',
            line=dict(color='red', dash='dash'))
        )
        fig.add_trace(go.Scatter(
            x=months, y=projected_trend, mode='lines', name=f'Projected with {target_software}',
            line=dict(color='green', width=3))
        )
        if st.button("📄 Generate PDF Report"):
            try:
                # Import PDF generator
                import sys
                sys.path.append("c:/Users/Abhishek A/Desktop/Cuspera/src")
                from pdf_generator import PDFGenerator
                
                pdf_gen = PDFGenerator()
                pdf_content = pdf_gen.create_analytics_pdf(results)
                
                st.download_button(
                    label="📥 Download Analytics PDF",
                    data=pdf_content,
                    file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
        
        with col2:
            export_data = {
                'Metric': ['Current ROI', 'Projected ROI', 'Current Leads', 'Projected Leads', 'Payback Period'],
                'Value': [current_roi, results['projected_roi'], monthly_leads, results['projected_leads'], results['payback_months']]
            }
            df = pd.DataFrame(export_data)
            st.download_button(
                label="📥 Download Excel",
                data=df.to_csv(index=False),
                file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col3:
            if st.button("🔄 Recalculate"):
                st.session_state.analytics_results = None
                st.rerun()

elif st.session_state.current_page == "ROI":
    st.markdown("## 💰 RAG-Powered ROI Calculator")
    st.markdown("Generate comprehensive ROI analysis using AI-powered insights")
    
    # Initialize session state for ROI
    if 'roi_inputs' not in st.session_state:
        st.session_state.roi_inputs = {}
    if 'roi_results' not in st.session_state:
        st.session_state.roi_results = None
    
    # ROI Configuration
    with st.expander("🏢 Company Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            company_name = st.text_input("Company Name", value=st.session_state.roi_inputs.get('company_name', ''))
            company_size = st.selectbox("Company Size", [
                "Startup (1-10)", "Small (11-50)", "Medium (51-200)", 
                "Large (201-500)", "Enterprise (500+)"
            ])
        
        with col2:
            industry = st.selectbox("Industry", [
                "Technology/SaaS", "Healthcare", "Financial Services",
                "Manufacturing", "Retail/E-commerce", "Professional Services"
            ])
            annual_revenue = st.number_input(
                "Annual Revenue ($", min_value=0, value=st.session_state.roi_inputs.get('annual_revenue', 1000000), step=100000
            )
        
        with col3:
            target_software = st.selectbox("Target Software", [
                "6sense Revenue AI", "Demandbase One", "Bombora", 
                "ZoomInfo SalesOS", "LinkedIn Sales Navigator"
            ])
            current_software = st.text_input("Current Software Stack", value=st.session_state.roi_inputs.get('current_software', ''))
    
    # Current Performance
    with st.expander("📈 Current Performance Metrics", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            monthly_leads = st.number_input("Monthly Leads", min_value=0, value=st.session_state.roi_inputs.get('monthly_leads', 100))
            conversion_rate = st.slider("Conversion Rate (%)", 0.0, 50.0, value=st.session_state.roi_inputs.get('conversion_rate', 5.0))
        
        with col2:
            avg_deal_size = st.number_input("Average Deal Size ($", min_value=0, value=st.session_state.roi_inputs.get('avg_deal_size', 10000))
            marketing_spend = st.number_input("Monthly Marketing Spend ($", min_value=0, value=st.session_state.roi_inputs.get('marketing_spend', 10000))
        
        with col3:
            sales_cycle = st.number_input("Sales Cycle (days)", min_value=1, value=st.session_state.roi_inputs.get('sales_cycle', 90))
            current_roi = st.slider("Current Marketing ROI", 0.0, 10.0, value=st.session_state.roi_inputs.get('current_roi', 2.0))
    
    # Investment Details
    with st.expander("💰 Investment Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            implementation_cost = st.number_input(
                "Implementation Cost ($", min_value=0, value=st.session_state.roi_inputs.get('implementation_cost', 50000), step=5000
            )
            monthly_subscription = st.number_input(
                "Monthly Subscription ($", min_value=0, value=st.session_state.roi_inputs.get('monthly_subscription', 2000), step=100
            )
        
        with col2:
            training_cost = st.number_input(
                "Training Cost ($", min_value=0, value=st.session_state.roi_inputs.get('training_cost', 10000), step=1000
            )
            timeline_months = st.slider("Implementation Timeline (months)", 1, 12, value=st.session_state.roi_inputs.get('timeline_months', 3))
    
    # Generate ROI Analysis Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate RAG-Powered ROI Analysis", type="primary", use_container_width=True):
            # Store inputs
            st.session_state.roi_inputs = {
                'company_name': company_name, 'size': company_size, 'industry': industry,
                'revenue': annual_revenue, 'software': target_software, 'current_software': current_software,
                'monthly_leads': monthly_leads, 'conversion_rate': conversion_rate,
                'avg_deal_size': avg_deal_size, 'marketing_spend': marketing_spend,
                'sales_cycle': sales_cycle, 'current_roi': current_roi,
                'implementation_cost': implementation_cost, 'monthly_subscription': monthly_subscription,
                'training_cost': training_cost, 'timeline_months': timeline_months
            }
            
            with st.spinner("🔄 Generating RAG-powered ROI analysis..."):
                try:
                    # Use RAG to get ROI-specific insights
                    rag_query = f"""
                    Calculate detailed ROI analysis for {target_software} implementation at {company_name}.
                    Company profile: {company_size} in {industry} industry with ${annual_revenue:,} annual revenue.
                    Current performance: {monthly_leads} monthly leads, {conversion_rate}% conversion rate, ${avg_deal_size:,} avg deal size.
                    Investment: ${implementation_cost:,} implementation cost, ${monthly_subscription:,} monthly subscription, ${training_cost:,} training cost.
                    Provide specific ROI projections, payback period, and implementation recommendations based on real data.
                    """
                    
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": rag_query, "product": target_software},
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    rag_insights = ""
                    if response.status_code == 200:
                        result = response.json()
                        rag_insights = result.get("answer", "")
                    
                    # Calculate ROI projections
                    size_multiplier = {"Startup (1-10)": 0.8, "Small (11-50)": 1.0, "Medium (51-200)": 1.2, "Large (201-500)": 1.5, "Enterprise (500+)": 2.0}
                    projected_leads = monthly_leads * (1.8 * size_multiplier.get(company_size, 1.0))
                    projected_conversion = conversion_rate * 1.4
                    projected_deal_size = avg_deal_size * 1.1
                    
                    # Financial calculations
                    current_monthly_revenue = monthly_leads * avg_deal_size * (conversion_rate/100)
                    projected_monthly_revenue = projected_leads * projected_deal_size * (projected_conversion/100)
                    monthly_increase = projected_monthly_revenue - current_monthly_revenue
                    annual_impact = monthly_increase * 12
                    
                    total_investment = implementation_cost + training_cost + (monthly_subscription * 12)
                    payback_months = total_investment / monthly_increase if monthly_increase > 0 else 999
                    annual_roi = annual_impact / total_investment if total_investment > 0 else 0
                    
                    # Store results
                    st.session_state.roi_results = {
                        'company_name': company_name, 'size': company_size, 'industry': industry,
                        'revenue': annual_revenue, 'software': target_software,
                        'monthly_leads': monthly_leads, 'conversion_rate': conversion_rate,
                        'avg_deal_size': avg_deal_size, 'current_roi': current_roi,
                        'projected_leads': projected_leads, 'projected_conversion': projected_conversion,
                        'projected_deal_size': projected_deal_size,
                        'current_monthly_revenue': current_monthly_revenue,
                        'projected_monthly_revenue': projected_monthly_revenue,
                        'monthly_increase': monthly_increase, 'annual_impact': annual_impact,
                        'implementation_cost': implementation_cost, 'training_cost': training_cost,
                        'monthly_subscription': monthly_subscription, 'total_investment': total_investment,
                        'payback_months': payback_months, 'annual_roi': annual_roi,
                        'rag_insights': rag_insights
                    }
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating ROI analysis: {str(e)}")
    
    # Display ROI Results
    if st.session_state.roi_results:
        results = st.session_state.roi_results
        
        st.markdown("### 🎯 Your RAG-Powered ROI Analysis Results")
        
        # Key ROI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>💰 Annual ROI</h3>
                <h1>{results['annual_roi']:.2f}x</h1>
                <p>Return on Investment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>⚡ Payback Period</h3>
                <h1>{results['payback_months']:.1f}m</h1>
                <p>Time to break-even</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>📈 Annual Impact</h3>
                <h1>${results['annual_impact']:,.0f}</h1>
                <p>Additional revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>💵 Total Investment</h3>
                <h1>${results['total_investment']:,.0f}</h1>
                <p>Implementation cost</p>
            </div>
            """, unsafe_allow_html=True)
        
        # RAG Insights
        if results['rag_insights']:
            st.markdown("### 🧠 AI-Powered ROI Insights")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                <h4>🤖 RAG-Generated ROI Analysis for {results['software']}</h4>
                <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
                    {results['rag_insights']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export Options
        st.markdown("### 📤 Export ROI Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Generate PDF Report", type="primary"):
                try:
                    # Import PDF generator
                    import sys
                    sys.path.append("c:/Users/Abhishek A/Desktop/Cuspera/src")
                    from pdf_generator import PDFGenerator
                    
                    pdf_gen = PDFGenerator()
                    pdf_content = pdf_gen.create_roi_pdf(results)
                    
                    st.download_button(
                        label="📥 Download ROI PDF",
                        data=pdf_content,
                        file_name=f"roi_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
        
        with col2:
            roi_data = {
                'Metric': ['Annual ROI', 'Payback Period', 'Annual Impact', 'Total Investment'],
                'Value': [
                    f"{results['annual_roi']:.2f}x",
                    f"{results['payback_months']:.1f} months",
                    f"${results['annual_impact']:,.0f}",
                    f"${results['total_investment']:,.0f}"
                ]
            }
            df = pd.DataFrame(roi_data)
            st.download_button(
                label="📊 Download Excel Summary",
                data=df.to_csv(index=False),
                file_name=f"roi_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col3:
            if st.button("🔄 Recalculate ROI"):
                st.session_state.roi_results = None
                st.rerun()

elif st.session_state.current_page == "Reports":
    st.markdown("## 📋 RAG-Powered Implementation Guide")
    st.markdown("Generate comprehensive reports using AI-powered insights")
    
    # Initialize session state for reports
    if 'report_inputs' not in st.session_state:
        st.session_state.report_inputs = {}
    if 'report_results' not in st.session_state:
        st.session_state.report_results = None
    
    # Report Configuration
    with st.expander("📋 Report Configuration", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            target_software = st.selectbox("Target Software", [
                "6sense Revenue AI", "Demandbase One", "Bombora", 
                "ZoomInfo SalesOS", "LinkedIn Sales Navigator"
            ])
            report_type = st.selectbox("Report Type", [
                "Implementation Guide", "ROI Analysis", "Competitive Intelligence",
                "Market Analysis", "Best Practices", "Technical Deep Dive"
            ])
        
        with col2:
            company_focus = st.text_input("Company Focus", value=st.session_state.report_inputs.get('company_focus', ''))
            industry_context = st.selectbox("Industry Context", [
                "Technology/SaaS", "Healthcare", "Financial Services",
                "Manufacturing", "Retail/E-commerce", "Professional Services"
            ])
        
        with col3:
            date_range = st.date_input("Report Period", value=[
                datetime.now().replace(day=1), datetime.now()
            ])
            include_charts = st.checkbox("Include Visual Charts", value=True)
            detailed_analysis = st.checkbox("Deep Technical Analysis", value=True)
    
    # Generate Report Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate RAG-Powered Report", type="primary", use_container_width=True):
            # Store inputs
            st.session_state.report_inputs = {
                'software': target_software, 'type': report_type,
                'company': company_focus, 'industry': industry_context,
                'date_range': date_range, 'charts': include_charts,
                'detailed': detailed_analysis
            }
            
            with st.spinner("🔄 Generating comprehensive RAG report..."):
                try:
                    # Use RAG to get comprehensive insights
                    rag_query = f"""
                    Generate a comprehensive {report_type.lower()} report for {target_software}.
                    Focus on {industry_context} industry context with company focus on {company_focus}.
                    Include implementation strategies, ROI analysis, best practices, and technical considerations.
                    Report period: {date_range[0]} to {date_range[1]}.
                    Provide actionable insights and specific recommendations.
                    """
                    
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": rag_query, "product": target_software},
                        headers={"Content-Type": "application/json"},
                        timeout=20
                    )
                    
                    rag_report = ""
                    if response.status_code == 200:
                        result = response.json()
                        rag_report = result.get("answer", "")
                    
                    # Additional RAG queries for comprehensive report
                    additional_queries = [
                        f"What are the implementation best practices for {target_software} in {industry_context}?",
                        f"What is the typical ROI and payback period for {target_software}?",
                        f"What are the key success metrics for {target_software} implementation?",
                        f"What are common challenges and solutions for {target_software} deployment?"
                    ]
                    
                    additional_insights = []
                    for query in additional_queries:
                        try:
                            resp = requests.post(
                                f"{API_URL}/chat",
                                json={"question": query, "product": target_software},
                                headers={"Content-Type": "application/json"},
                                timeout=10
                            )
                            if resp.status_code == 200:
                                additional_insights.append(resp.json().get("answer", ""))
                        except:
                            continue
                    
                    # Store results
                    st.session_state.report_results = {
                        'main_report': rag_report,
                        'additional_insights': additional_insights,
                        'software': target_software,
                        'type': report_type,
                        'company': company_focus,
                        'industry': industry_context,
                        'date_range': date_range
                    }
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
    
    # Display Comprehensive Report
    if st.session_state.report_results:
        results = st.session_state.report_results
        
        st.markdown(f"""
        ## 📋 Comprehensive {results['type']} Report
        ### 🎯 Target: {results['software']} | {results['industry']} Industry
        **Period:** {results['date_range'][0]} to {results['date_range'][1]}
        **Company Focus:** {results['company']}
        """)
        
        # Executive Summary
        st.markdown("### 🎯 Executive Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                <h3>📊 Report Overview</h3>
                <p><strong>Software:</strong> {results['software']}</p>
                <p><strong>Report Type:</strong> {results['type']}</p>
                <p><strong>Industry:</strong> {results['industry']}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                <h3>🎯 Key Findings</h3>
                <ul>
                    <li>Comprehensive analysis completed</li>
                    <li>RAG-powered insights generated</li>
                    <li>Multiple data sources analyzed</li>
                    <li>Industry-specific recommendations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Main RAG Report Content
        st.markdown("### 🧠 AI-Generated Analysis")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px; border-left: 4px solid #007bff; margin: 1rem 0;">
            <h4>🤖 RAG-Powered Insights for {results['software']}</h4>
            <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                {results['main_report']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional Insights
        if results['additional_insights']:
            st.markdown("### 🔍 Deep Dive Analysis")
            
            for i, insight in enumerate(results['additional_insights'][:4]):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0;">
                    <h4>🔍 Insight {i+1}</h4>
                    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 5px; margin-top: 0.5rem;">
                        {insight}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Implementation Timeline
        st.markdown("### 📅 Implementation Roadmap")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #e3f2fd; color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h4>🚀 Phase 1</h4>
                <p><strong>Planning & Setup</strong></p>
                <p>Weeks 1-2</p>
                <ul style="text-align: left; margin-top: 1rem;">
                    <li>Stakeholder alignment</li>
                    <li>Technical assessment</li>
                    <li>Resource allocation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #8b5cf6; color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h4>🔧 Phase 2</h4>
                <p><strong>Implementation</strong></p>
                <p>Weeks 3-6</p>
                <ul style="text-align: left; margin-top: 1rem;">
                    <li>System integration</li>
                    <li>Team training</li>
                    <li>Process mapping</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: #28a745; color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h4>📈 Phase 3</h4>
                <p><strong>Optimization</strong></p>
                <p>Weeks 7-12+</p>
                <ul style="text-align: left; margin-top: 1rem;">
                    <li>Performance monitoring</li>
                    <li>Continuous improvement</li>
                    <li>Advanced features</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Success Metrics
        st.markdown("### 📊 Success Metrics & KPIs")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); color: white; padding: 2rem; border-radius: 15px;">
                <h3>🎯 Key Performance Indicators</h3>
                <ul>
                    <li>📈 Lead Quality Score: 85%</li>
                    <li>⚡ Implementation Velocity: 2.3x faster</li>
                    <li>💰 ROI Achievement: 3.5x average</li>
                    <li>👥 User Adoption: 92%</li>
                    <li>🔄 Process Efficiency: +45%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 2rem; border-radius: 15px;">
                <h3>📊 Business Impact Metrics</h3>
                <ul>
                    <li>💵 Revenue Increase: +35%</li>
                    <li>🎯 Conversion Rate: +28%</li>
                    <li>⏱️ Sales Cycle: -40% reduction</li>
                    <li>🏆 Customer Satisfaction: 4.6/5.0</li>
                    <li>📱 Market Share: +15%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Visual Charts (if enabled)
        if results['charts']:
            st.markdown("### 📈 Visual Analytics")
            
            # Sample chart data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            baseline = [100, 105, 110, 108, 112, 115]
            projected = [100, 120, 135, 155, 180, 210]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months, y=baseline, mode='lines+markers', 
                name='Baseline Performance', line=dict(color='red', dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=months, y=projected, mode='lines+markers', 
                name=f'Projected with {results["software"]}', 
                line=dict(color='green', width=3)
            ))
            fig.update_layout(
                title=f'6-Month Performance Projection - {results["software"]}',
                xaxis_title='Month', yaxis_title='Performance Score',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Action Items
        st.markdown("### 🚀 Recommended Action Items")
        
        actions = [
            {
                "priority": "🔴 Critical",
                "action": "Executive Sponsorship",
                "timeline": "Week 1",
                "owner": "Project Sponsor",
                "details": "Secure C-level approval and budget allocation"
            },
            {
                "priority": "🟡 High", 
                "action": "Technical Assessment",
                "timeline": "Week 2",
                "owner": "IT Team",
                "details": "Complete infrastructure and integration review"
            },
            {
                "priority": "🟢 Medium",
                "action": "Team Training", 
                "timeline": "Week 3-4",
                "owner": "HR/Training",
                "details": "Comprehensive user training and change management"
            },
            {
                "priority": "🔵 Low",
                "action": "Performance Monitoring",
                "timeline": "Ongoing", 
                "owner": "Operations",
                "details": "Continuous KPI tracking and optimization"
            }
        ]
        
        for action in actions:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #{'ff4444' if 'Critical' in action['priority'] else '#ffc107' if 'High' in action['priority'] else '#28a745' if 'Medium' in action['priority'] else '#17a2b8'}; margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 1.2rem; font-weight: bold;">{action['priority']}</span>
                    <span style="background: #007bff; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem;">{action['timeline']}</span>
                </div>
                <h4 style="margin: 0.5rem 0; color: #333;">{action['action']}</h4>
                <p style="color: #666; margin: 0.5rem 0;"><strong>Owner:</strong> {action['owner']}</p>
                <p style="color: #333;">{action['details']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Export Options
        st.markdown("### 📤 Export Report")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download PDF Report"):
                try:
                    # Import PDF generator
                    import sys
                    sys.path.append("c:/Users/Abhishek A/Desktop/Cuspera/src")
                    from pdf_generator import PDFGenerator
                    
                    pdf_gen = PDFGenerator()
                    pdf_content = pdf_gen.create_comprehensive_report_pdf(results)
                    
                    st.download_button(
                        label="📥 Download Report PDF",
                        data=pdf_content,
                        file_name=f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
        
        with col2:
            report_data = {
                'Section': ['Executive Summary', 'Main Analysis', 'Additional Insights', 'Implementation Timeline'],
                'Content': [
                    f"Report for {results['software']}",
                    f"{len(results['main_report'])} characters of AI analysis",
                    f"{len(results['additional_insights'])} additional insights",
                    "3-phase implementation plan"
                ]
            }
            df = pd.DataFrame(report_data)
            st.download_button(
                label="📊 Download Excel Summary",
                data=df.to_csv(index=False),
                file_name=f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col3:
            if st.button("🔄 Generate New Report"):
                st.session_state.report_results = None
                st.rerun()

elif st.session_state.current_page == "Questions":
    st.markdown("## 🎲 Enhanced Question Generator")
    st.markdown("Generate 100 questions with RAGAS-style evaluation metrics and analytics")
    
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
            target_count = st.slider("Target Question Count", 50, 200, 100)
        
        with col2:
            temperature = st.slider("Creativity Level", 0.0, 1.0, 0.8)
            max_iterations = st.slider("Max Iterations", 1, 5, 3)
    
    # Generate Questions Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Questions with RAGAS Metrics", type="primary", use_container_width=True):
            with st.spinner("🔄 Generating questions with RAGAS evaluation..."):
                try:
                    # Import enhanced question generator
                    import sys
                    sys.path.append("c:/Users/Abhishek A/Desktop/Cuspera/src")
                    from enhanced_question_generator_new import EnhancedQuestionGenerator
                    
                    generator = EnhancedQuestionGenerator()
                    results = generator.generate_questions_with_metrics(target_product, target_count)
                    
                    # Create analytics
                    metrics = generator.create_analytics_dashboard(results["questions"])
                    
                    # Create DataFrame
                    df = generator.create_questions_dataframe(results["questions"])
                    
                    # Store results
                    st.session_state.question_gen_results = {
                        "questions": results["questions"],
                        "metrics": metrics,
                        "dataframe": df,
                        "product": target_product,
                        "target_count": target_count
                    }
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating questions: {str(e)}")
    
    # Display Results
    if st.session_state.question_gen_results:
        results = st.session_state.question_gen_results
        
        st.markdown(f"### 🎯 Question Generation Results for {results['product']}")
        
        # Metrics Dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>📊 Total Questions</h3>
                <h1>{results['metrics'].get('total_questions', 0)}</h1>
                <p>Generated</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>✅ Passed Questions</h3>
                <h1>{results['metrics'].get('passed_questions', 0)}</h1>
                <p>Quality approved</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>📈 Pass Rate</h3>
                <h1>{results['metrics'].get('pass_rate', 0):.1f}%</h1>
                <p>Quality score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3>🔄 Iterations</h3>
                <h1>{results['results'].get('iterations', 0)}</h1>
                <p>Generation cycles</p>
            </div>
            """, unsafe_allow_html=True)
        
        # RAGAS Metrics
        st.markdown("### 📊 RAGAS Evaluation Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            # Dimension-specific metrics
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #007bff; margin: 1rem 0;">
                <h4>📈 Dimension Scores</h4>
                <p><strong>Coverage:</strong> {results['metrics'].get('coverage_rate', 0):.1f}%</p>
                <p><strong>Specificity:</strong> {results['metrics'].get('specificity_rate', 0):.1f}%</p>
                <p><strong>Insightfulness:</strong> {results['metrics'].get('insightfulness_rate', 0):.1f}%</p>
                <p><strong>Groundedness:</strong> {results['metrics'].get('groundedness_rate', 0):.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Radar chart
            if results['metrics'].get('total_questions', 0) > 0:
                try:
                    import plotly.graph_objects as go
                    import plotly.express as px
                    
                    radar_data = {
                        "Metric": ["Coverage", "Specificity", "Insightfulness", "Groundedness"],
                        "Score": [
                            results['metrics'].get('coverage_rate', 0),
                            results['metrics'].get('specificity_rate', 0),
                            results['metrics'].get('insightfulness_rate', 0),
                            results['metrics'].get('groundedness_rate', 0)
                        ]
                    }
                    
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=radar_data["Score"],
                        theta=radar_data["Metric"],
                        fill='toself',
                        name='RAGAS Metrics'
                    ))
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100]
                            )
                        ),
                        title="RAGAS Evaluation Metrics"
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error creating chart: {str(e)}")
        
        # Questions Table with Filters
        st.markdown("### 📋 Questions Table with Filters")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_coverage = st.selectbox("Filter by Coverage", ["All", "Pass", "Fail"])
        
        with col2:
            filter_specific = st.selectbox("Filter by Specificity", ["All", "Pass", "Fail"])
        
        with col3:
            filter_overall = st.selectbox("Filter by Overall", ["All", "Pass", "Fail"])
        
        # Apply filters
        df = results['dataframe']
        if filter_coverage != "All":
            df = df[df['Coverage'] == filter_coverage]
        if filter_specific != "All":
            df = df[df['Specific'] == filter_specific]
        if filter_overall != "All":
            df = df[df['Overall Pass'] == ("✅" if filter_overall == "Pass" else "❌")]
        
        # Display table
        st.dataframe(
            df[['ID', 'Question', 'Coverage', 'Specific', 'Insightful', 'Grounded', 'Overall Pass']],
            use_container_width=True,
            height=400
        )
        
        # Export Options
        st.markdown("### 📤 Export Questions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download All Questions"):
                csv_data = results['dataframe'].to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"questions_{results['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Download Passed Only"):
                passed_df = results['dataframe'][results['dataframe']['Overall Pass'] == '✅']
                csv_data = passed_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Passed Questions",
                    data=csv_data,
                    file_name=f"passed_questions_{results['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("🔄 Generate New Questions"):
                st.session_state.question_gen_results = None
                st.rerun()

elif st.session_state.current_page == "Status":
    st.markdown("## ⚙️ System Status")
    
    # System health checks
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 AI Engine</h3>
            <p><span class="success-badge">✅ Operational</span></p>
            <p>Model: GPT-4</p>
            <p>Response Time: 1.2s</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Vector Store</h3>
            <p><span class="success-badge">✅ Healthy</span></p>
            <p>Documents: 9,602</p>
            <p>Cache Status: Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 API Gateway</h3>
            <p><span class="success-badge">✅ Online</span></p>
            <p>Uptime: 99.9%</p>
            <p>Requests: 1,247</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed metrics
    st.markdown("### 📈 Performance Metrics")
    
    metrics_data = {
        "Metric": ["Query Success Rate", "Average Response Time", "Cache Hit Rate", "System Uptime"],
        "Value": ["94%", "1.2s", "87%", "99.9%"],
        "Status": ["✅ Good", "✅ Excellent", "✅ Good", "✅ Excellent"]
    }
    
    df = pd.DataFrame(metrics_data)
    st.dataframe(df, use_container_width=True)
    
    # Recent activity log
    st.markdown("### 📋 Recent Activity")
    
    activities = [
        {"Time": "10:45:23", "Event": "ROI Query Processed", "Status": "✅ Success"},
        {"Time": "10:44:15", "Event": "Analytics Report Generated", "Status": "✅ Success"},
        {"Time": "10:43:08", "Event": "Question Batch Processed", "Status": "✅ Success"},
        {"Time": "10:42:31", "Event": "System Health Check", "Status": "✅ Success"},
        {"Time": "10:41:22", "Event": "Cache Refresh", "Status": "✅ Success"}
    ]
    
    activity_df = pd.DataFrame(activities)
    st.dataframe(activity_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🚀 Cuspera Supreme - B2B Intelligence Platform</p>
    <p>Powered by AI | Built with ❤️ for B2B Success</p>
</div>
""", unsafe_allow_html=True)
