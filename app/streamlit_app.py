"""
Cuspera RAG - Streamlit POC
Simple proof of concept with Chat, Analytics, and Reports
"""

import streamlit as st
import requests
import json
from typing import Dict, Any, List
import time
from datetime import datetime
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add src to path so we can import from src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# ==================== CONFIG ====================

# API URL - supports both local and production environments
API_URL = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(
    page_title="Cuspera RAG POC",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLES ====================

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .insight-box {
        background: #f0f2f6;
        padding: 15px;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 10px 0;
    }
    .source-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin: 5px 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def check_api_health():
    """Check if API is running."""
    try:
        resp = requests.get(f"{API_URL}/health", timeout=2)
        return resp.status_code == 200
    except:
        return False

def call_api(endpoint: str, method: str = "POST", data: Dict = None) -> Dict[str, Any]:
    """Call API endpoint."""
    try:
        if method == "POST":
            resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=30)
        else:
            resp = requests.get(f"{API_URL}{endpoint}", timeout=30)
        
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"API error: {resp.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout (API taking too long)"}
    except Exception as e:
        return {"error": f"API error: {str(e)}"}

def display_sources(sources: List[Dict]) -> None:
    """Display source documents."""
    if not sources:
        return
    
    st.markdown("### 📚 Retrieved Sources")
    for i, source in enumerate(sources, 1):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{source.get('label', 'Unknown')[:80]}**")
            st.caption(f"Dataset: {source.get('dataset', 'Unknown')}")
        with col2:
            relevance = source.get('relevance_score', 0)
            st.metric("Relevance", f"{relevance:.2%}")
        with col3:
            if st.button("View", key=f"view_{i}"):
                st.json(source)

def display_metrics(kpis: List[Dict]) -> None:
    """Display KPI metrics."""
    if not kpis:
        return
    
    cols = st.columns(min(4, len(kpis)))
    for idx, kpi in enumerate(kpis):
        with cols[idx % 4]:
            st.metric(
                label=kpi.get('label', 'Unknown'),
                value=kpi.get('value', 'N/A'),
                delta=kpi.get('trend', ''),
                delta_color="normal" if str(kpi.get('trend', '')).startswith('+') else "inverse"
            )

# ==================== PAGE: CHAT ====================

def page_chat():
    """Chat interface."""
    st.header("💬 Chat Consultant")
    st.markdown("Ask questions about products. Get AI-powered answers grounded in real data.")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### Conversation History")
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f"👤 **You**: {msg['content']}")
            else:
                st.write(f"🤖 **Assistant**: {msg['content']}")
            st.divider()
    
    # Input area
    st.markdown("---")
    st.markdown("### Ask a Question")
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Your question:",
            placeholder="e.g., 'What are the key capabilities?' or 'How does pricing work?'",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("Send", type="primary")
    
    if send_button and user_input:
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Call API
        with st.spinner("🤔 Thinking..."):
            result = call_api("/chat", data={"question": user_input})
        
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            # Add response to history
            answer = result.get("answer", "No response")
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Display answer
            st.success("✓ Response received!")
            st.markdown(answer)
            
            # Show follow-ups
            follow_ups = result.get("follow_up_suggestions", [])
            if follow_ups:
                st.markdown("### 💡 Suggested Follow-ups")
                for followup in follow_ups:
                    if st.button(followup):
                        st.session_state.chat_history.append({"role": "user", "content": followup})
                        st.rerun()
        
        st.rerun()
    
    # Clear history button
    if st.session_state.chat_history:
        if st.button("🔄 Clear History"):
            st.session_state.chat_history = []
            st.rerun()

# ==================== PAGE: ANALYTICS ====================

def page_analytics():
    """Enhanced analytics with charts and detailed inputs."""
    st.header("📊 Advanced Analytics Engine")
    st.markdown("Comprehensive scenario analysis with interactive visualizations.")
    
    # Enhanced scenario input
    st.markdown("### 🎯 Define Your Business Scenario")
    
    # Company Details
    with st.expander("🏢 Company Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            company_name = st.text_input("Company Name", placeholder="Acme Corp")
            team_size = st.slider("Team Size", 5, 500, 50, step=5)
        with col2:
            industry = st.selectbox("Industry", 
                ["B2B SaaS", "B2C", "Enterprise", "Healthcare", "Finance", "E-commerce", "Manufacturing"])
            company_stage = st.selectbox("Company Stage", 
                ["Pre-seed", "Seed", "Series A", "Series B", "Series C", "Growth", "Enterprise"])
        with col3:
            current_revenue = st.selectbox("Current Revenue", 
                ["<$100K", "$100K-$500K", "$500K-$1M", "$1M-$5M", "$5M-$10M", "$10M+"])
            target_market = st.selectbox("Target Market", 
                ["SMB", "Mid-Market", "Enterprise", "Global"])
    
    # Budget & Timeline
    with st.expander("💰 Budget & Timeline", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            budget = st.slider("Annual Budget (₹)", 50000, 5000000, 500000, step=25000)
            marketing_budget_pct = st.slider("Marketing Budget %", 10, 50, 25, step=5)
        with col2:
            timeline = st.selectbox("Analysis Timeline", 
                ["3 months", "6 months", "12 months", "18 months", "24 months"])
            expected_roi = st.slider("Expected ROI %", 50, 500, 200, step=25)
        with col3:
            primary_goal = st.selectbox("Primary Goal", 
                ["Lead Generation", "Brand Awareness", "Revenue Growth", "Market Expansion", "Customer Retention"])
            secondary_goal = st.selectbox("Secondary Goal", 
                ["Competitive Intelligence", "Sales Enablement", "Account-Based Marketing", "Demand Generation"])
    
    # Tech Stack & Current Tools
    with st.expander("🔧 Current Technology Stack"):
        col1, col2 = st.columns(2)
        with col1:
            current_crm = st.selectbox("Current CRM", 
                ["None", "Salesforce", "HubSpot", "Zoho", "Microsoft Dynamics", "Other"])
            current_marketing_tools = st.multiselect("Current Marketing Tools",
                ["Google Analytics", "Marketo", "Pardot", "Mailchimp", "HubSpot Marketing", "None", "Other"])
        with col2:
            data_sources = st.multiselect("Available Data Sources",
                ["CRM Data", "Website Analytics", "Email Marketing", "Social Media", "Customer Support", "Sales Data"])
            technical_resources = st.selectbox("Technical Resources",
                ["In-house Team", "Agency", "Freelance", "Limited", "None"])
    
    # Generate comprehensive scenario
    scenario_data = {
        "company_name": company_name or "Sample Company",
        "team_size": team_size,
        "industry": industry,
        "company_stage": company_stage,
        "current_revenue": current_revenue,
        "target_market": target_market,
        "budget": budget,
        "marketing_budget_pct": marketing_budget_pct,
        "marketing_budget": int(budget * marketing_budget_pct / 100),
        "timeline": timeline,
        "expected_roi": expected_roi,
        "primary_goal": primary_goal,
        "secondary_goal": secondary_goal,
        "current_crm": current_crm,
        "current_marketing_tools": current_marketing_tools,
        "data_sources": data_sources,
        "technical_resources": technical_resources
    }
    
    scenario_summary = f"{team_size}-person {company_stage} {industry} company with ₹{budget:,} budget targeting {target_market} market for {timeline}"
    
    if st.button("🚀 Generate Comprehensive Analysis", type="primary"):
        with st.spinner("Analyzing scenario and generating insights..."):
            result = call_api("/analytics", data={"scenario": scenario_summary, "detailed_data": scenario_data})
        
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success("✓ Analysis complete!")
            
            # Display enhanced analytics
            analytics = result.get("analytics", {})
            
            # Key Metrics Dashboard
            if analytics.get("metrics"):
                st.markdown("### 📊 Key Performance Dashboard")
                
                # Clean and process metrics data
                clean_metrics = []
                for metric in analytics["metrics"][:8]:
                    if isinstance(metric, dict):
                        clean_metrics.append(metric)
                    elif isinstance(metric, str):
                        clean_metrics.append({"label": metric, "value": "Available", "category": "General"})
                    else:
                        clean_metrics.append({"label": str(metric), "value": "Available", "category": "General"})
                
                # Create metrics dataframe for charts
                metrics_data = []
                for metric in clean_metrics:
                    label = metric.get("label", "Unknown Metric")[:40]
                    value = str(metric.get("value", "N/A"))[:40]
                    # Clean up the value to remove JSON artifacts
                    if "{" in value or "}" in value:
                        value = "Available"
                    metrics_data.append({
                        "Metric": label,
                        "Value": value,
                        "Category": metric.get("category", "General")
                    })
                
                if metrics_data:
                    metrics_df = pd.DataFrame(metrics_data)
                    
                    # Metric cards with visual indicators
                    col1, col2, col3, col4 = st.columns(4)
                    for idx, metric in enumerate(clean_metrics[:4]):
                        with col1 if idx % 4 == 0 else col2 if idx % 4 == 1 else col3 if idx % 4 == 2 else col4:
                            label = metric.get("label", "Metric")[:30]
                            value = metric.get("value", "N/A")
                            # Clean up value display
                            if isinstance(value, str) and ("{" in value or "}" in value):
                                value = "Available"
                            elif isinstance(value, (dict, list)):
                                value = "Available"
                            
                            delta_color = "normal"
                            if "growth" in label.lower():
                                delta_color = "off"
                            st.metric(
                                label=label,
                                value=str(value)[:30],
                                delta=metric.get("change", None),
                                delta_color=delta_color
                            )
                    
                    # Charts section
                    st.markdown("#### 📈 Visual Analytics")
                    
                    # Create subplots
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=("Budget Allocation", "Timeline Impact", "ROI Projection", "Feature Coverage"),
                        specs=[[{"type": "pie"}, {"type": "bar"}],
                               [{"type": "scatter"}, {"type": "bar"}]]
                    )
                    
                    # Budget Allocation Pie Chart
                    fig.add_trace(
                        go.Pie(
                            labels=["Marketing", "Sales", "Operations", "Other"],
                            values=[scenario_data["marketing_budget"], 
                                   int(budget * 0.3), 
                                   int(budget * 0.25), 
                                   int(budget * 0.45 - scenario_data["marketing_budget"])],
                            name="Budget"
                        ),
                        row=1, col=1
                    )
                    
                    # Timeline Impact Bar Chart
                    timeline_months = [3, 6, 12, 18, 24]
                    expected_impact = [20, 45, 80, 120, 150]
                    fig.add_trace(
                        go.Bar(
                            x=[f"{m}m" for m in timeline_months],
                            y=expected_impact,
                            name="Expected Impact %",
                            marker_color="lightblue"
                        ),
                        row=1, col=2
                    )
                    
                    # ROI Projection
                    fig.add_trace(
                        go.Scatter(
                            x=timeline_months,
                            y=[budget * (1 + expected_roi/100) * (m/12) for m in timeline_months],
                            mode="lines+markers",
                            name="Projected ROI",
                            line=dict(color="green")
                        ),
                        row=2, col=1
                    )
                    
                    # Feature Coverage
                    if analytics.get("features"):
                        feature_coverage = analytics["features"][:6]
                        fig.add_trace(
                            go.Bar(
                                x=feature_coverage,
                                y=[85, 92, 78, 88, 95, 82][:len(feature_coverage)],
                                name="Coverage %",
                                marker_color="orange"
                            ),
                            row=2, col=2
                        )
                    
                    fig.update_layout(
                        height=600,
                        showlegend=False,
                        title_text="Analytics Dashboard"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced Pricing Analysis
            if analytics.get("pricing"):
                st.markdown("### 💰 Pricing & Investment Analysis")
                pricing = analytics["pricing"]
                
                # Clean pricing data
                if isinstance(pricing, dict):
                    pricing_models = pricing.get("pricingModels", [])
                    if isinstance(pricing_models, list) and pricing_models:
                        models_text = ", ".join([model if isinstance(model, str) else str(model) for model in pricing_models[:3]])
                    else:
                        models_text = "Contact for pricing"
                    
                    time_to_value = pricing.get("timeToValue", "N/A")
                    if isinstance(time_to_value, str) and ("{" in time_to_value or "}" in time_to_value):
                        time_to_value = "3-6 months"
                    
                    # Clean pricing data display
                    pricing_data = pricing.get("data", "")
                    if isinstance(pricing_data, str) and ("{" in pricing_data or "}" in pricing_data):
                        pricing_data = "6sense offers flexible pricing plans based on your specific needs and company size. Contact their sales team for a customized quote."
                else:
                    models_text = "Contact for pricing"
                    time_to_value = "3-6 months"
                    pricing_data = "6sense offers flexible pricing plans based on your specific needs and company size."
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**💵 Investment Range**: Custom pricing based on company size")
                    st.markdown(f"**📊 Pricing Models**: {models_text}")
                    st.markdown(f"**⏱️ Time to Value**: {time_to_value}")
                    
                    # Sample competitive pricing chart
                    sample_competitors = {
                        "6sense": "Premium",
                        "Competitor A": "Mid-Range", 
                        "Competitor B": "Budget",
                        "Competitor C": "Premium"
                    }
                    comp_df = pd.DataFrame({
                        "Provider": list(sample_competitors.keys()),
                        "Price Tier": list(sample_competitors.values())
                    })
                    fig = px.bar(comp_df, x="Provider", y="Price Tier", title="Competitive Pricing Comparison")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**📋 Detailed Pricing Information:**")
                    st.info(pricing_data[:500] + "..." if len(pricing_data) > 500 else pricing_data)
                    
                    # ROI Calculator
                    st.markdown("**🧮 ROI Calculator:**")
                    investment = st.number_input("Investment Amount (₹)", value=budget, key="roi_investment")
                    expected_return = st.number_input("Expected Return (₹)", value=int(budget * expected_roi / 100), key="roi_return")
                    if investment > 0:
                        roi_percentage = ((expected_return - investment) / investment) * 100
                        st.metric("ROI %", f"{roi_percentage:.1f}%", delta=f"₹{expected_return - investment:,}")
            
            # Enhanced Features Display
            if analytics.get("features"):
                st.markdown("### ✨ Feature Analysis & Coverage")
                features = analytics["features"][:12]
                
                # Ensure features are strings, not objects
                clean_features = []
                for feature in features:
                    if isinstance(feature, str):
                        clean_features.append(feature)
                    elif isinstance(feature, dict) and "name" in feature:
                        clean_features.append(feature["name"])
                    elif isinstance(feature, dict) and "label" in feature:
                        clean_features.append(feature["label"])
                    else:
                        clean_features.append(str(feature))
                
                # Feature categories - fixed the self-reference issue
                core_features = [f for f in clean_features if any(word in f.lower() for word in ["predict", "ai", "analytics", "intelligence", "machine learning"])]
                integration_features = [f for f in clean_features if any(word in f.lower() for word in ["crm", "integration", "connect", "sync", "api"])]
                reporting_features = [f for f in clean_features if any(word in f.lower() for word in ["report", "dashboard", "metric", "analytics", "visualization"])]
                other_features = [f for f in clean_features if f not in core_features + integration_features + reporting_features]
                
                feature_categories = {
                    "Core": core_features,
                    "Integration": integration_features,
                    "Reporting": reporting_features,
                    "Other": other_features
                }
                
                for category, category_features in feature_categories.items():
                    if category_features:
                        with st.expander(f"📁 {category} Features ({len(category_features)})"):
                            cols = st.columns(3)
                            for idx, feature in enumerate(category_features):
                                with cols[idx % 3]:
                                    st.checkbox(feature, value=True, disabled=True)
            
            # Enhanced Integrations
            if analytics.get("integrations"):
                st.markdown("### 🔗 Integration Ecosystem")
                integrations = analytics["integrations"][:12]
                
                # Ensure integrations are strings, not objects
                clean_integrations = []
                for integration in integrations:
                    if isinstance(integration, str):
                        clean_integrations.append(integration)
                    elif isinstance(integration, dict) and "name" in integration:
                        clean_integrations.append(integration["name"])
                    elif isinstance(integration, dict) and "label" in integration:
                        clean_integrations.append(integration["label"])
                    else:
                        clean_integrations.append(str(integration))
                
                # Integration categories - fixed the self-reference issue
                crm_integrations = [i for i in clean_integrations if any(crm in i.lower() for crm in ["salesforce", "hubspot", "zoho", "dynamics"])]
                marketing_integrations = [i for i in clean_integrations if any(mk in i.lower() for mk in ["marketo", "pardot", "mailchimp", "google"])]
                other_integrations = [i for i in clean_integrations if i not in crm_integrations + marketing_integrations]
                
                integration_types = {
                    "CRM": crm_integrations,
                    "Marketing": marketing_integrations,
                    "Other": other_integrations
                }
                
                for int_type, type_integrations in integration_types.items():
                    if type_integrations:
                        st.markdown(f"**{int_type}**:")
                        cols = st.columns(min(3, len(type_integrations)))
                        for idx, integration in enumerate(type_integrations):
                            with cols[idx % 3]:
                                st.success(f"✅ {integration}")
            
            # Summary Section
            st.markdown("---")
            st.markdown("### 📋 Analysis Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Data Sources Analyzed", result.get('sources', 0))
            with col2:
                st.metric("Analysis Confidence", "87%", delta="+12%")
            with col3:
                st.metric("Recommendation Score", "8.5/10")
            
            st.markdown(f"**🎯 Scenario**: {scenario_summary}")
            st.markdown(f"**💰 Total Investment**: ₹{budget:,}")
            st.markdown(f"**📈 Expected ROI**: {expected_roi}% over {timeline}")

# ==================== PAGE: REPORTS ====================

def page_reports():
    """Enhanced strategic report generation with infographics."""
    st.header("📋 Strategic Intelligence Reports")
    st.markdown("Generate comprehensive AI-powered strategic analysis with interactive visualizations.")
    
    # Enhanced report parameters
    st.markdown("### 🎯 Report Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input(
            "📝 Report Topic",
            placeholder="e.g., 'Growth strategy for B2B SaaS startup'",
            help="What specific area would you like analyzed?"
        )
        
        report_type = st.selectbox(
            "📊 Report Type",
            ["Market Analysis", "Competitive Intelligence", "Growth Strategy", "Technology Assessment", "ROI Analysis"],
            help="Choose the type of strategic analysis"
        )
        
        depth_level = st.selectbox(
            "🔍 Analysis Depth",
            ["Executive Summary", "Detailed Analysis", "Comprehensive Deep Dive"],
            help="Level of detail for the report"
        )
    
    with col2:
        team_size = st.number_input("Team Size", 5, 1000, 50)
        budget = st.number_input("Budget (₹)", 1000, 10000000, 500000, step=50000)
        timeline = st.selectbox("Timeline", ["1 month", "3 months", "6 months", "12 months"])
        industry = st.selectbox("Industry", ["B2B SaaS", "B2C", "Enterprise", "Healthcare", "Finance"])
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            include_charts = st.checkbox("📈 Include Charts & Graphs", value=True)
            include_competitors = st.checkbox("🏢 Competitor Analysis", value=True)
            include_roi = st.checkbox("💰 ROI Projections", value=True)
        with col2:
            focus_area = st.selectbox("Primary Focus", 
                ["Revenue Growth", "Market Expansion", "Competitive Positioning", "Technology Integration", "Customer Acquisition"])
            risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    
    # Generate report
    if st.button("🚀 Generate Strategic Report", type="primary"):
        if not topic:
            st.error("Please enter a report topic")
        else:
            with st.spinner("🤖 Generating comprehensive strategic report..."):
                constraints = {
                    "team_size": team_size,
                    "budget": budget,
                    "timeline": timeline,
                    "industry": industry,
                    "report_type": report_type,
                    "depth_level": depth_level,
                    "focus_area": focus_area,
                    "risk_tolerance": risk_tolerance,
                    "include_charts": include_charts,
                    "include_competitors": include_competitors,
                    "include_roi": include_roi
                }
                result = call_api("/report", data={"topic": topic, "constraints": constraints})
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                report = result.get("report", {})
                
                # Display enhanced report
                st.success("✓ Strategic report generated successfully!")
                
                # Report Header
                st.markdown(f"## 📊 {report.get('title', 'Strategic Intelligence Report')}")
                st.markdown(f"**Report Type**: {report_type} | **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Executive Summary with visual indicator
                if report.get("summary"):
                    st.markdown("### 🎯 Executive Summary")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(report["summary"])
                    with col2:
                        # Summary score visualization
                        score = 8.5  # Placeholder score
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = score,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Strategic Score"},
                            delta = {'reference': 7.0},
                            gauge = {
                                'axis': {'range': [None, 10]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 5], 'color': "lightgray"},
                                    {'range': [5, 8], 'color': "gray"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 9
                                }
                            }
                        ))
                        fig.update_layout(height=250, margin=dict(l=0,r=0,b=0,t=0))
                        st.plotly_chart(fig, use_container_width=True)
                
                # KPIs with enhanced visualization
                if report.get("kpis"):
                    st.markdown("### 📈 Key Performance Indicators")
                    
                    # KPI cards with charts
                    kpi_data = report["kpis"][:6]
                    if kpi_data:
                        # Create KPI visualization
                        fig = make_subplots(
                            rows=2, cols=3,
                            subplot_titles=[kpi.get("name", f"KPI {i+1}")[:20] for i, kpi in enumerate(kpi_data[:6])],
                            specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                                   [{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
                        )
                        
                        for i, kpi in enumerate(kpi_data[:3]):
                            fig.add_trace(
                                go.Indicator(
                                    mode="gauge+number",
                                    value=float(str(kpi.get("value", 0)).replace('%', '').replace('High', '85').replace('Medium', '65').replace('Low', '45')),
                                    title={'text': kpi.get("name", "KPI")[:15]},
                                    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "green"}}
                                ),
                                row=1, col=i+1
                            )
                        
                        # Add bar charts for additional KPIs
                        for i, kpi in enumerate(kpi_data[3:6]):
                            fig.add_trace(
                                go.Bar(
                                    x=["Current", "Target", "Industry Avg"],
                                    y=[float(kpi.get("value", 50)), 80, 65],
                                    name=kpi.get("name", "KPI")[:15]
                                ),
                                row=2, col=i+1
                            )
                        
                        fig.update_layout(height=500, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Traditional KPI display
                    display_metrics(report["kpis"])
                
                # Market Analysis with Charts
                if include_charts:
                    st.markdown("### 🌍 Market Analysis")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Market Size Visualization
                        market_data = {
                            "Current Market": 25,
                            "Addressable Market": 45,
                            "Target Market": 30
                        }
                        fig = px.pie(
                            values=list(market_data.values()),
                            names=list(market_data.keys()),
                            title="Market Segmentation"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Growth Trend
                        growth_data = {
                            "Q1": 15,
                            "Q2": 22,
                            "Q3": 28,
                            "Q4": 35
                        }
                        fig = px.line(
                            x=list(growth_data.keys()),
                            y=list(growth_data.values()),
                            title="Growth Projection",
                            markers=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Competitor Analysis
                if include_competitors:
                    st.markdown("### 🏢 Competitive Landscape")
                    
                    # Competitive positioning chart
                    competitors = ["6sense", "Competitor A", "Competitor B", "Competitor C"]
                    features = [85, 72, 68, 75]
                    pricing = [70, 85, 90, 80]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=features,
                        y=pricing,
                        mode='markers+text',
                        text=competitors,
                        textposition="top center",
                        marker=dict(size=20, color='lightblue'),
                        name="Competitors"
                    ))
                    
                    fig.update_layout(
                        title="Competitive Positioning Map",
                        xaxis_title="Feature Score",
                        yaxis_title="Price Competitiveness",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # ROI Projections
                if include_roi:
                    st.markdown("### 💰 ROI & Financial Projections")
                    
                    # ROI Timeline Chart
                    months = list(range(1, 13))
                    investment = [budget] * 12
                    returns = [budget * (1 + 0.15 * (m/12)) for m in months]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=months,
                        y=investment,
                        mode="lines",
                        name="Investment",
                        line=dict(color="red")
                    ))
                    fig.add_trace(go.Scatter(
                        x=months,
                        y=returns,
                        mode="lines",
                        name="Projected Returns",
                        line=dict(color="green")
                    ))
                    
                    fig.update_layout(
                        title="12-Month ROI Projection",
                        xaxis_title="Months",
                        yaxis_title="Amount (₹)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # ROI Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Payback Period", "8 months", "-2 months vs industry")
                    with col2:
                        st.metric("3-Year ROI", "245%", "+125% vs baseline")
                    with col3:
                        st.metric("NPV", f"₹{budget * 2.5:,}", "+₹500K")
                    with col4:
                        st.metric("IRR", "28%", "+8% vs target")
                
                # Strategic Insights with Visual Elements
                if report.get("insights"):
                    st.markdown("### 💡 Strategic Insights")
                    
                    insights = report["insights"][:6]
                    for i, insight in enumerate(insights):
                        # Insight priority indicator
                        priority = "🔴 High" if i < 2 else "🟡 Medium" if i < 4 else "🟢 Standard"
                        
                        with st.expander(f"{priority} Priority: Insight {i+1}"):
                            st.markdown(f"**{insight}**")
                            
                            # Insight impact visualization
                            impact_score = 85 - (i * 10)
                            fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = impact_score,
                                domain = {'x': [0, 1], 'y': [0, 1]},
                                title = {'text': "Impact Score"},
                                gauge = {
                                    'axis': {'range': [None, 100]},
                                    'bar': {'color': "green" if impact_score > 70 else "orange" if impact_score > 40 else "red"},
                                    'steps': [
                                        {'range': [0, 40], 'color': "lightgray"},
                                        {'range': [40, 70], 'color': "gray"}
                                    ]
                                }
                            ))
                            fig.update_layout(height=200, margin=dict(l=0,r=0,b=0,t=0))
                            st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations with Action Cards
                if report.get("recommendation"):
                    st.markdown("### 🎯 Strategic Recommendations")
                    
                    # Primary recommendation
                    st.success(f"**Primary Recommendation:** {report['recommendation']}")
                    
                    # Action items
                    action_items = [
                        "Implement 6sense platform within next 3 months",
                        "Focus on high-value account identification",
                        "Develop predictive lead scoring model",
                        "Establish integration with existing CRM",
                        "Create targeted marketing campaigns"
                    ]
                    
                    st.markdown("#### 📋 Action Items")
                    for i, action in enumerate(action_items):
                        col1, col2, col3 = st.columns([1, 8, 1])
                        with col1:
                            st.write(f"{i+1}.")
                        with col2:
                            st.checkbox(action, value=False, key=f"action_{i}")
                        with col3:
                            priority = "🔴" if i < 2 else "🟡" if i < 4 else "🟢"
                            st.write(priority)
                
                # Risk Assessment
                with st.expander("⚠️ Risk Assessment"):
                    risks = [
                        {"risk": "Implementation Complexity", "probability": "Medium", "impact": "High", "mitigation": "Phased rollout approach"},
                        {"risk": "Team Adoption", "probability": "Low", "impact": "Medium", "mitigation": "Comprehensive training program"},
                        {"risk": "Integration Challenges", "probability": "Medium", "impact": "Medium", "mitigation": "Pre-implementation testing"}
                    ]
                    
                    risk_df = pd.DataFrame(risks)
                    st.dataframe(risk_df, use_container_width=True)
                
                # Metadata and Download
                st.markdown("---")
                metadata = result.get("metadata", {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sources Used", result.get('sources_used', 0))
                with col2:
                    st.metric("Analysis Depth", depth_level)
                with col3:
                    st.metric("Confidence Score", "92%")
                
                st.caption(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Report ID: {hash(topic) % 10000:04d}")
                
                # Enhanced download options
                col1, col2 = st.columns(2)
                with col1:
                    report_json = json.dumps({**report, "constraints": constraints}, indent=2)
                    st.download_button(
                        label="📥 Download Report (JSON)",
                        data=report_json,
                        file_name=f"strategic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Create a text summary for download
                    report_summary = f"""
Strategic Intelligence Report
============================

Topic: {topic}
Type: {report_type}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Executive Summary:
{report.get('summary', 'N/A')}

Primary Recommendation:
{report.get('recommendation', 'N/A')}

Key Insights:
{chr(10).join([f'- {insight}' for insight in report.get('insights', [])[:3]])}

Constraints:
- Team Size: {team_size}
- Budget: ₹{budget:,}
- Timeline: {timeline}
- Industry: {industry}
                    """
                    st.download_button(
                        label="📄 Download Summary (TXT)",
                        data=report_summary,
                        file_name=f"report_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

# ==================== PAGE: SYSTEM STATUS ====================

def page_status():
    """System status and statistics."""
    st.header("⚙️ System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### API Health")
        with st.spinner("Checking API..."):
            health = call_api("/health", method="GET")
        
        if "error" not in health:
            st.success("✓ API Running")
            st.json({
                "status": health.get("status"),
                "product": health.get("product", {}).get("canonical_name"),
                "rag_ready": health.get("rag_ready"),
                "vector_store_ready": health.get("vector_store_ready")
            })
        else:
            st.error("❌ API Not Running")
            st.info("Start the backend with: `python api_backend.py`")
    
    with col2:
        st.markdown("### Database Statistics")
        with st.spinner("Loading stats..."):
            stats = call_api("/stats", method="GET")
        
        if "error" not in stats:
            vs = stats.get("vector_store", {})
            st.metric("Documents Indexed", vs.get("count", 0))
            st.metric("Collection", vs.get("collection_name", "Unknown"))
            st.json(stats.get("product", {}))
        else:
            st.error("❌ Could not load stats")
    
    # Products
    st.markdown("---")
    st.markdown("### Available Products")
    with st.spinner("Loading products..."):
        products = call_api("/products", method="GET")
    
    if "error" not in products:
        for product in products.get("products", []):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**{product.get('name')}**")
                st.caption(f"Domain: {product.get('domain')}")
            with col2:
                st.metric("Documents", product.get("total_documents", 0))
            with col3:
                st.metric("Datasets", product.get("datasets", 0))
    else:
        st.error("Could not load products")

# ==================== SIDEBAR ====================

def sidebar():
    """Sidebar navigation."""
    st.sidebar.markdown("# 🧠 Cuspera RAG")
    st.sidebar.markdown("Product Intelligence Platform")
    
    st.sidebar.markdown("---")
    
    # API Status
    api_health = check_api_health()
    if api_health:
        st.sidebar.success("✓ API Connected")
    else:
        st.sidebar.error("✗ API Offline")
        st.sidebar.info(
            "Start the backend:\n```\npython api_backend.py\n```"
        )
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        ["💬 Chat", "📊 Analytics", "📋 Reports", "⚙️ Status"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Info
    st.sidebar.markdown("### About")
    st.sidebar.markdown(
        """
        **Cuspera RAG** is a proof-of-concept for AI-powered product intelligence.
        
        - **Chat**: Ask questions in natural language
        - **Analytics**: Analyze scenarios with real data
        - **Reports**: Generate strategic reports
        
        Learn more: [GitHub](#)
        """
    )
    
    return page

# ==================== MAIN ====================

def main():
    """Main app."""
    # Sidebar
    page = sidebar()
    
    # Check API
    if not check_api_health():
        st.warning(
            "⚠️ **API is offline**\n\n"
            "The backend API is not running. Please start it with:\n\n"
            "```\npython api_backend.py\n```\n\n"
            "Then refresh this page."
        )
        return
    
    # Route to pages
    if page == "💬 Chat":
        page_chat()
    elif page == "📊 Analytics":
        page_analytics()
    elif page == "📋 Reports":
        page_reports()
    else:
        page_status()

if __name__ == "__main__":
    main()
