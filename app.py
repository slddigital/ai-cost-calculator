# app.py
"""Main Streamlit application"""
import streamlit as st
import plotly.graph_objects as go
from calculator import (
    calculate_api_cost, 
    optimize_api_usage, 
    analyze_dev_tools,
    generate_summary_report
)
from pricing_data import API_PRICING, DEV_TOOLS

# Page config
st.set_page_config(
    page_title="AI Cost Optimizer",
    page_icon="💰",
    layout="wide"
)

# Header
st.title("💰 AI Cost Optimization Calculator")
st.markdown("### Find 30-90% savings in your AI spending")
st.markdown("**Analyze 50+ models across 8 providers** | Updated October 2025")

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Models Analyzed", "50+")
with col2:
    st.metric("Average Savings", "67%")
with col3:
    st.metric("Analysis Time", "5 min")

st.divider()

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Create tabs
tab1, tab2, tab3 = st.tabs(["🤖 API Usage", "👨‍💻 Developer Tools", "📊 Results"])

# TAB 1: API Usage
with tab1:
    st.header("AI API Cost Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        provider = st.selectbox(
            "API Provider",
            options=['openai', 'anthropic', 'google', 'deepseek', 'mistral', 'cohere', 'xai'],
            format_func=lambda x: x.title()
        )
        
        current_model = st.selectbox(
            "Current Model",
            options=list(API_PRICING[provider].keys())
        )
        
        monthly_calls = st.number_input(
            "Monthly API Calls",
            min_value=0,
            value=100000,
            step=10000
        )
    
    with col2:
        avg_input_tokens = st.number_input(
            "Average Input Tokens",
            min_value=0,
            value=500,
            step=50
        )
        
        avg_output_tokens = st.number_input(
            "Average Output Tokens",
            min_value=0,
            value=200,
            step=50
        )
        
        use_case = st.selectbox(
            "Primary Use Case",
            options=['customer_support', 'content_generation', 'code_generation', 'document_analysis', 'data_extraction'],
            format_func=lambda x: x.replace('_', ' ').title()
        )
    
    # Show current cost
    if monthly_calls > 0:
        current_api_cost = calculate_api_cost(provider, current_model, monthly_calls, avg_input_tokens, avg_output_tokens)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Monthly Cost", f"${current_api_cost:,.2f}")
        with col2:
            st.metric("Annual Cost", f"${current_api_cost * 12:,.2f}")

# TAB 2: Developer Tools
with tab2:
    st.header("Developer Tools Analysis")
    
    dev_tools_data = {}
    
    for tool in ['gitlab_duo', 'github_copilot', 'cursor', 'codeium']:
        with st.expander(f"📝 {tool.replace('_', ' ').title()}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                uses_tool = st.checkbox(f"We use {tool.replace('_', ' ').title()}", key=f"use_{tool}")
            
            if uses_tool:
                with col2:
                    total_seats = st.number_input(
                        "Total Seats",
                        min_value=0,
                        value=50,
                        key=f"total_{tool}"
                    )
                
                with col3:
                    active_seats = st.number_input(
                        "Active Users",
                        min_value=0,
                        max_value=total_seats,
                        value=int(total_seats * 0.65),
                        key=f"active_{tool}"
                    )
                
                dev_tools_data[tool] = {'total_seats': total_seats, 'active_seats': active_seats}
            else:
                dev_tools_data[tool] = {'total_seats': 0, 'active_seats': 0}

# TAB 3: Results
with tab3:
    st.header("📊 Your AI Cost Analysis")
    
    if st.button("🎯 Analyze All Spending", type="primary", use_container_width=True):
        st.session_state.analysis_done = True
        
        with st.spinner("Analyzing..."):
            all_recommendations = []
            
            if monthly_calls > 0:
                api_recs = optimize_api_usage(provider, current_model, monthly_calls, avg_input_tokens, avg_output_tokens, use_case)
                all_recommendations.extend(api_recs)
            
            dev_recs = analyze_dev_tools(dev_tools_data)
            all_recommendations.extend(dev_recs)
            
            summary = generate_summary_report(all_recommendations)
            st.session_state.summary = summary
    
    if st.session_state.analysis_done:
        summary = st.session_state.summary
        
        # Key metrics
        st.markdown("### 🎯 Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Monthly", f"${summary['total_monthly_cost']:,.0f}")
        with col2:
            st.metric("Potential Savings", f"${summary['total_monthly_savings']:,.0f}", delta=f"-{summary['savings_percentage']:.0f}%")
        with col3:
            st.metric("Annual Savings", f"${summary['total_annual_savings']:,.0f}")
        with col4:
            optimized = summary['total_monthly_cost'] - summary['total_monthly_savings']
            st.metric("Optimized Monthly", f"${optimized:,.0f}")
        
        # Chart
        fig = go.Figure(data=[
            go.Bar(name='Current', x=['Cost'], y=[summary['total_monthly_cost']], marker_color='#FF6B6B'),
            go.Bar(name='Optimized', x=['Cost'], y=[optimized], marker_color='#4ECDC4')
        ])
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("### 🎯 Top Recommendations")
        
        for i, rec in enumerate(summary['top_recommendations'], 1):
            with st.expander(f"#{i}: {rec['title']} • Save ${rec['annual_savings']:,.0f}/year", expanded=(i==1)):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Description:** {rec['description']}")
                    st.write(f"**Effort:** {rec['effort']}")
                    st.code(rec['implementation'])
                with col2:
                    st.metric("Monthly Savings", f"${rec['monthly_savings']:,.0f}")
                    st.metric("Annual Savings", f"${rec['annual_savings']:,.0f}")

# Footer
st.divider()
st.caption("💡 Pricing updated October 2025 | Results are estimates based on current published pricing")