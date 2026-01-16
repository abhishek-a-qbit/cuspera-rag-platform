import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64

# Set page configuration with beautiful theme
st.set_page_config(
    page_title="🚀 6sense Revenue AI Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Beautiful custom CSS with gradients and animations
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)

# Animated header with logo
st.markdown("""
<div class="main-header">
    <div style="position: relative; z-index: 1;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🚀 6sense Revenue AI Dashboard
        </h1>
        <h2 style="font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9;">
            Real-time Performance Analytics & Intelligence
        </h2>
        <p style="font-size: 1.1rem; opacity: 0.8; margin: 0;">
            ✨ Advanced Analytics | 💰 ROI Insights | 📈 Predictive Intelligence | 🎯 Smart Recommendations
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with beautiful styling
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                padding: 1.5rem; border-radius: 15px; color: white; 
                text-align: center; margin-bottom: 2rem;">
        <h3>📊 Dashboard Controls</h3>
        <p style="margin: 0; opacity: 0.9;">Customize your view</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    time_range = st.selectbox("📅 Time Range", [
        "Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"
    ])
    
    region = st.selectbox("🌍 Region", [
        "All Regions", "North America", "Europe", "Asia Pacific", "Latin America"
    ])
    
    product_focus = st.selectbox("🎯 Product Focus", [
        "All Products", "Revenue AI", "Account Intelligence", "Predictive Analytics", "Customer Insights"
    ])
    
    refresh_interval = st.slider("🔄 Auto Refresh (seconds)", min_value=30, max_value=300, value=60)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    if st.button("📥 Export Dashboard", use_container_width=True):
        st.info("Dashboard export functionality coming soon!")
    
    if st.button("📧 Email Report", use_container_width=True):
        st.info("Email scheduling coming soon!")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# Generate sample data based on filters
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
revenue_data = np.random.normal(400000, 50000, 12).clip(300000, 550000)
lead_data = np.random.normal(300, 50, 12).clip(200, 450).astype(int)
conversion_rates = np.random.normal(0.28, 0.05, 12).clip(0.15, 0.40)

# Beautiful metrics row with animations
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("💰 Total Revenue", f"${sum(revenue_data):,.0f}", "+23% YoY")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🎯 Conversion Rate", f"{np.mean(conversion_rates):.1%}", "+5.2%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("⭐ Lead Quality", "8.7/10", "+0.8")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📈 ROI", "312%", "+45%")
    st.markdown('</div>', unsafe_allow_html=True)

# Additional metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏢 Active Accounts", "2,847", "+12%")
with col2:
    st.metric("💎 Pipeline Value", "$24.3M", "+18%")
with col3:
    st.metric("🏆 Win Rate", "42.3%", "+3.1%")
with col4:
    st.metric("😊 Customer Satisfaction", "94%", "+2%")

# Charts Section with beautiful containers
st.markdown("### 📈 Performance Analytics")

# Row 1: Revenue and Lead Conversion
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💰 Monthly Revenue Trend")
    
    # Create beautiful revenue chart
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(
        x=months,
        y=revenue_data,
        mode='lines+markers',
        line=dict(color='#4CAF50', width=4),
        marker=dict(size=10, color='#4CAF50', line=dict(width=2, color='white')),
        name='Revenue'
    ))
    
    fig_revenue.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        yaxis_tickformat='$,.0f',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_revenue, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Lead Conversions")
    
    # Create beautiful bar chart
    colors = ['#2196F3', '#1976D2', '#1565C0', '#0D47A1', '#0277BD', '#01579B']
    fig_conversion = go.Figure()
    
    fig_conversion.add_trace(go.Bar(
        x=months,
        y=lead_data,
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        name='Leads Converted'
    ))
    
    fig_conversion.update_layout(
        title="Monthly Lead Conversions",
        xaxis_title="Month",
        yaxis_title="Number of Leads",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_conversion, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: Conversion Rate and Pipeline
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 Conversion Rate Trend")
    
    fig_conversion_rate = go.Figure()
    fig_conversion_rate.add_trace(go.Scatter(
        x=months,
        y=[rate * 100 for rate in conversion_rates],
        mode='lines+markers',
        line=dict(color='#FF9800', width=4),
        marker=dict(size=10, color='#FF9800', line=dict(width=2, color='white')),
        fill='tonexty',
        fillcolor='rgba(255, 152, 0, 0.2)',
        name='Conversion Rate %'
    ))
    
    fig_conversion_rate.update_layout(
        title="Monthly Conversion Rate",
        xaxis_title="Month",
        yaxis_title="Conversion Rate (%)",
        yaxis_ticksuffix="%",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_conversion_rate, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Pipeline by Stage")
    
    pipeline_stages = ['Prospecting', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won']
    pipeline_values = [4500000, 3200000, 2800000, 1900000, 1200000]
    
    fig_pipeline = go.Figure()
    fig_pipeline.add_trace(go.Funnel(
        y=pipeline_stages,
        x=pipeline_values,
        marker=dict(
            color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
            line=dict(width=2, color='white')
        ),
        textinfo="value+percent initial"
    ))
    
    fig_pipeline.update_layout(
        title="Pipeline Distribution by Stage",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_pipeline, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3: Regional Performance and Product Mix
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🌍 Regional Performance")
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    regional_revenue = [2800000, 1500000, 1200000, 500000]
    
    fig_regional = go.Figure()
    fig_regional.add_trace(go.Pie(
        labels=regions,
        values=regional_revenue,
        hole=0.4,
        marker=dict(colors=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
    ))
    
    fig_regional.update_layout(
        title="Revenue Distribution by Region",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_regional, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📦 Product Performance")
    
    products = ['Revenue AI', 'Account Intelligence', 'Predictive Analytics', 'Customer Insights']
    product_revenue = [2500000, 1800000, 1200000, 800000]
    
    fig_products = go.Figure()
    fig_products.add_trace(go.Bar(
        x=products,
        y=product_revenue,
        marker=dict(
            color=['#667eea', '#764ba2', '#f093fb', '#f5576c'],
            line=dict(color='white', width=2)
        ),
        name='Revenue'
    ))
    
    fig_products.update_layout(
        title="Revenue by Product",
        xaxis_title="Product",
        yaxis_title="Revenue ($)",
        yaxis_tickformat='$,.0f',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_products, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Export Options with beautiful styling
st.markdown("### 📤 Export Options")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Export to CSV", use_container_width=True):
        # Create sample data for export
        export_data = pd.DataFrame({
            "Month": months,
            "Revenue": revenue_data,
            "Leads": lead_data,
            "Conversion Rate": [rate * 100 for rate in conversion_rates]
        })
        csv_data = export_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"6sense_dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📊 Export to Excel", use_container_width=True):
        st.info("Excel export functionality coming soon!")

with col3:
    if st.button("📋 Generate PDF Report", use_container_width=True):
        st.info("PDF report generation coming soon!")

# Beautiful footer
st.markdown("---")
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea, #764ba2); 
            padding: 2rem; border-radius: 15px; text-align: center; 
            color: white; margin-top: 2rem;">
    <h3 style="margin: 0; font-size: 1.5rem;">🚀 6sense Revenue AI Dashboard</h3>
    <p style="margin: 0.5rem 0; opacity: 0.9;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
    <p style="margin: 0; opacity: 0.8;">
        Powered by Advanced Analytics | Real-time Intelligence | Predictive Insights
    </p>
</div>
""", unsafe_allow_html=True)
