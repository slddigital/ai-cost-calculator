# app.py
"""Main Streamlit application"""
import streamlit as st
import streamlit.components.v1 as components
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
st.markdown("**Analyse 50+ models across 8 providers** | Updated October 2025")

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Models Analysed", "50+")
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
        with st.expander(f"🔧 {tool.replace('_', ' ').title()}"):
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
    
    if st.button("🎯 Analyse All Spending", type="primary", use_container_width=True):
        st.session_state.analysis_done = True
        
        with st.spinner("Analysing..."):
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
            st.metric("Optimised Monthly", f"${optimized:,.0f}")
        
        # Chart
        fig = go.Figure(data=[
            go.Bar(name='Current', x=['Cost'], y=[summary['total_monthly_cost']], marker_color='#FF6B6B'),
            go.Bar(name='Optimised', x=['Cost'], y=[optimized], marker_color='#4ECDC4')
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
        
        # Payment section with Formspree
        st.divider()
        st.header("📄 Get Your Detailed Implementation Report")
        
        # Create three columns for pricing options
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            st.subheader("📧 Free Summary")
            st.markdown("**Perfect for:** Quick overview")
            st.write("")
            st.write("✅ Email summary of findings")
            st.write("✅ Top 3 recommendations")
            st.write("✅ Estimated savings")
            st.write("")
            
            monthly_cost = summary.get('total_monthly_cost', 0)
            savings = summary.get('total_monthly_savings', 0)
            
            # Formspree form using components.html
            form_html = f"""
            <form action="https://formspree.io/f/mwprzpgz" method="POST" style="display: flex; flex-direction: column; gap: 10px;">
                <input type="email" name="email" placeholder="you@company.com" required 
                       style="padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box;">
                
                <input type="text" name="company" placeholder="Your Company" required 
                       style="padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box;">
                
                <select name="role" required 
                        style="padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box;">
                    <option value="">Select Role...</option>
                    <option value="Engineering Lead">Engineering Lead</option>
                    <option value="CTO/VP Engineering">CTO/VP Engineering</option>
                    <option value="Product Manager">Product Manager</option>
                    <option value="Finance/Operations">Finance/Operations</option>
                    <option value="Founder/CEO">Founder/CEO</option>
                    <option value="Other">Other</option>
                </select>
                
                <input type="hidden" name="monthly_cost" value="${monthly_cost:,.2f}">
                <input type="hidden" name="potential_savings" value="${savings:,.2f}">
                <input type="hidden" name="_subject" value="New AI Cost Calculator Lead">
                <input type="text" name="_gotcha" style="display:none">
                
                <button type="submit" 
                        style="padding: 12px; background-color: #4CAF50; color: white; border: none; 
                               border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%;">
                    📨 Get Free Summary
                </button>
            </form>
            
            <p style="font-size: 12px; color: #666; margin-top: 10px; text-align: center;">
                We'll email you within 24 hours
            </p>
            """
            
            components.html(form_html, height=350)
        
        with col2:
            st.subheader("📊 Basic Report")
            st.markdown("**£79** ~~£299~~")
            st.caption("Limited time offer")
            st.write("")
            st.write("✅ 15-page detailed PDF")
            st.write("✅ Complete cost breakdown")
            st.write("✅ All recommendations")
            st.write("✅ Implementation roadmap")
            st.write("✅ ROI calculator")
            st.write("✅ Business case template")
            st.write("")
            st.write("📅 Delivered within 48 hours")
            st.write("")
            
            st.markdown(
                """
                <a href="https://buy.stripe.com/eVq00cgT03sTgtS1Og3ks00" target="_blank">
                    <button style="
                        background-color: #4CAF50;
                        color: white;
                        padding: 12px 24px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        width: 100%;
                        font-size: 16px;
                        font-weight: bold;
                    ">
                        Buy Basic Report →
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.subheader("💎 Premium + Call")
            st.markdown("**£229** ~~£599~~")
            st.caption("Best value")
            st.write("")
            st.write("✅ Everything in Basic")
            st.write("✅ **30-min consultation**")
            st.write("✅ Screen-sharing walkthrough")
            st.write("✅ Custom prioritisation")
            st.write("✅ Implementation Q&A")
            st.write("✅ Call recording")
            st.write("✅ 30 days email support")
            st.write("")
            st.write("📅 Report: 48hrs | Call: 5 days")
            st.write("")
            
            st.markdown(
                """
                <a href="https://buy.stripe.com/14AaEQ1Y60gH5Pe3Wo3ks01" target="_blank">
                    <button style="
                        background-color: #FF6B35;
                        color: white;
                        padding: 12px 24px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        width: 100%;
                        font-size: 16px;
                        font-weight: bold;
                    ">
                        Buy Premium →
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Trust signals
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(" Secure payment via Stripe")
        with col2:
            st.caption(" Delivered to your inbox")
        with col3:
            st.caption(" Money-back guarantee")

# Footer
st.divider()
st.caption("💡 Pricing updated October 2025 | Results are estimates based on current published pricing")