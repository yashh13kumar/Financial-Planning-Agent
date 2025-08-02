import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
from utils import format_currency, format_percentage

def render_questionnaire(agent):
    st.subheader("📋 Let's Build Your Retirement Plan")
    st.markdown("I’ll ask you a few quick questions to understand your financial picture. This helps me tailor a plan just for you.")

    questions = [
        {"key": "name", "q": "👋 What should I call you?", "type": "text"},
        {"key": "age", "q": "🎂 What is your current age?", "type": "number"},
        {"key": "current_income", "q": "💼 What is your current **annual** income (in ₹)?", "type": "number"},
        {"key": "current_savings", "q": "💰 How much have you saved so far (in ₹)?", "type": "number"},
        {"key": "retirement_age", "q": "🏖️ At what age do you wish to retire?", "type": "number"},
        {"key": "risk_tolerance", "q": "📈 Your risk tolerance?", "options": ["Conservative", "Moderate", "Aggressive"], "type": "select"},
        {"key": "monthly_expenses", "q": "💸 Your approximate **monthly expenses** (in ₹)?", "type": "number"},
        {"key": "goal_summary", "q": "🎯 What's your main goal? (optional)", "type": "text"}
    ]

    if 'questionnaire_data' not in st.session_state:
        st.session_state.questionnaire_data = {}

    # ✅ Begin form
    with st.form("financial_questionnaire"):
        for question in questions:
            key = question["key"]
            if question["type"] == "text":
                value = st.text_input(
                    question["q"],
                    value=st.session_state.questionnaire_data.get(key, ""),
                    key=f"q_{key}"
                )
            elif question["type"] == "number":
                value = st.number_input(
                    question["q"],
                    min_value=0,
                    value=st.session_state.questionnaire_data.get(key, 0),
                    key=f"q_{key}"
                )
            elif question["type"] == "select":
                value = st.selectbox(
                    question["q"],
                    options=question["options"],
                    index=question["options"].index(st.session_state.questionnaire_data.get(key, question["options"][0])) if key in st.session_state.questionnaire_data else 0,
                    key=f"q_{key}"
                )
            st.session_state.questionnaire_data[key] = value

        # ✅ Must be inside the form block
        submitted = st.form_submit_button("🚀 Generate My Retirement Plan")
        if submitted:
            agent.update_user_data(st.session_state.questionnaire_data)
            st.session_state.user_data = agent.get_user_data()
            st.session_state.questionnaire_completed = True

            if agent._has_sufficient_data():
                plan = agent.chat("Can you generate my retirement plan?")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": plan
                })
                st.session_state.show_formula_explanation = True
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Thanks! I still need a few more details to create your retirement plan. Can you tell me your exact age, income, and savings?"
                })
            st.rerun()

def render_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def render_chat_input(agent):
    if prompt := st.chat_input("Ask me anything about your financial plan..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                response = agent.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.user_data = agent.get_user_data()
                if any(keyword in response.lower() for keyword in ['plan', 'retirement', 'save', 'nest egg']):
                    st.session_state.show_formula_explanation = True
                st.rerun()

def render_sidebar():
    """Render the sidebar with user data summary and controls."""
    st.sidebar.header("📊 Your Financial Summary")
    
    user_data = st.session_state.get('user_data', {})

    if user_data:
        # Normalize possible keys from chat or form
        age = user_data.get("age")
        income = user_data.get("income") or user_data.get("current_income")
        savings = user_data.get("savings") or user_data.get("current_savings")
        retirement_age = user_data.get("retirement_age")
        risk_tolerance = user_data.get("risk_tolerance")

        if age:
            st.sidebar.metric("Current Age", f"{age} years")

        if income:
            st.sidebar.metric("Annual Income", format_currency(income))

        if savings:
            st.sidebar.metric("Current Savings", format_currency(savings))

        if retirement_age:
            st.sidebar.metric("Target Retirement Age", f"{retirement_age} years")
            if age:
                years_to_retirement = retirement_age - age
                if years_to_retirement > 0:
                    st.sidebar.metric("Years to Retirement", f"{years_to_retirement} years")

        if risk_tolerance:
            st.sidebar.metric("Risk Tolerance", risk_tolerance.title())

        # Progress indicators
        required_fields = ['age', 'income', 'savings', 'retirement_age']
        completed_fields = sum(1 for field in required_fields if user_data.get(field) or user_data.get(f"current_{field}"))
        progress = completed_fields / len(required_fields)

        st.sidebar.subheader("Information Progress")
        st.sidebar.progress(progress)
        st.sidebar.caption(f"{completed_fields}/{len(required_fields)} required fields completed")

        missing_fields = [
            field.replace('_', ' ').title()
            for field in required_fields
            if not (user_data.get(field) or user_data.get(f"current_{field}"))
        ]
        if missing_fields:
            st.sidebar.warning(f"Still needed: {', '.join(missing_fields)}")

        # Action buttons
        st.sidebar.subheader("Quick Actions")

        if st.sidebar.button("🔄 Start Over"):
            st.session_state.messages = []
            st.session_state.user_data = {}
            st.session_state.agent.reset_conversation()
            st.session_state.show_formula_explanation = False
            st.rerun()

        if st.sidebar.button("📈 Show Calculations"):
            st.session_state.show_formula_explanation = True
            st.rerun()

        # Additional calculators
        render_quick_calculators(user_data)

    else:
        st.sidebar.info("Start chatting to see your financial summary here!")

        # Option to restart questionnaire or sample questions
        st.sidebar.subheader("💡 Quick Actions")

        if st.sidebar.button("📋 Retake Questionnaire"):
            st.session_state.questionnaire_completed = False
            st.session_state.questionnaire_data = {}
            st.session_state.messages = []
            st.session_state.user_data = {}
            st.session_state.agent.reset_conversation()
            st.rerun()

        st.sidebar.subheader("💡 Sample Questions")
        sample_questions = [
            "What if I could save 20% of my income?",
            "Should I pay off my mortgage or invest?",
            "Can I retire 5 years earlier?",
            "What if inflation rises to 6%?"
        ]

        for question in sample_questions:
            if st.sidebar.button(f"💬 {question}", key=f"sample_{question[:10]}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()


def render_quick_calculators(user_data: Dict):
    """Render quick calculator widgets in the sidebar."""
    st.sidebar.subheader("🧮 Quick Calculators")
    
    # Rule of 72 Calculator
    with st.sidebar.expander("Rule of 72 - Doubling Time"):
        rate_input = st.number_input("Annual Return Rate (%)", min_value=1.0, max_value=20.0, value=7.0, step=0.1)
        doubling_time = 72 / rate_input
        st.metric("Years to Double", f"{doubling_time:.1f} years")
    
    # Emergency Fund Calculator
    with st.sidebar.expander("Emergency Fund Calculator"):
        monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=1000, value=4000, step=100)
        months_coverage = st.slider("Months of Coverage", 3, 12, 6)
        emergency_fund = monthly_expenses * months_coverage
        st.metric("Recommended Emergency Fund", format_currency(emergency_fund))
    
    # Retirement Withdrawal Rate
    if 'current_savings' in user_data:
        with st.sidebar.expander("Safe Withdrawal Rate"):
            current_savings = user_data['current_savings']
            withdrawal_rates = [0.03, 0.035, 0.04, 0.045]
            
            for rate in withdrawal_rates:
                annual_withdrawal = current_savings * rate
                st.metric(f"{rate*100}% Rule", format_currency(annual_withdrawal))

def render_formula_explanation():
    """Render detailed formula explanations and calculations."""
    st.subheader("📊 Formula Explanations")
    
    user_data = st.session_state.get('user_data', {})
    
    if not user_data or len(user_data) < 4:
        st.info("Complete your financial profile to see detailed calculations!")
        return
    
    # Create tabs for different formula categories
    tab2, tab3 = st.tabs([ "Your Calculations", "Scenarios"])
    
    
    with tab2:
        render_user_calculations(user_data)
    
    with tab3:
        render_scenario_analysis(user_data)


def render_user_calculations(user_data: Dict):
    """Render specific calculations for the user's data."""
    from formulas import FinancialFormulas
    formulas = FinancialFormulas()
    
    # Extract values
    age = user_data.get('age')
    retirement_age = user_data.get('retirement_age')
    current_income = user_data.get('income') or user_data.get('current_income')
    current_savings = user_data.get('savings') or user_data.get('current_savings')
    risk_tolerance = user_data.get('risk_tolerance', 'Moderate')

    # Validate required fields
    if None in [age, retirement_age, current_income, current_savings]:
        st.warning("⚠️ Please complete all required fields to see your calculations.")
        return

    # Calculate
    years_to_retirement = retirement_age - age
    if years_to_retirement <= 0:
        st.error("❌ Retirement age must be greater than your current age.")
        return

    return_rates = {'conservative': 0.05, 'moderate': 0.07, 'aggressive': 0.09}
    annual_return = return_rates[risk_tolerance.lower()]
    retirement_income_target = current_income * 0.8
    future_current_savings = formulas.future_value(current_savings, annual_return, years_to_retirement)
    retirement_years = 25
    required_nest_egg = formulas.present_value_annuity(retirement_income_target, annual_return, retirement_years)
    additional_needed = max(0, required_nest_egg - future_current_savings)
    monthly_savings = formulas.payment_for_future_value(additional_needed, annual_return, years_to_retirement) / 12 if additional_needed > 0 else 0

    # Render
    st.markdown("## 🎯 Your Specific Calculations")

    st.markdown(f"""
### 1. Growth of Current Savings  
- **Formula**: `FV = PV × (1 + r)^n`  
- **Calculation**: ₹{current_savings:,.0f} × (1 + {annual_return:.1%})^{years_to_retirement}  
- **Result**: **{format_currency(future_current_savings)}**
""")

    st.markdown(f"""
### 2. Required Nest Egg for Retirement  
- **Formula**: `PV = PMT × [1 - (1 + r)^(-n)] / r`  
- **Calculation**: {format_currency(retirement_income_target)} × [1 - (1 + {annual_return:.1%})^(-{retirement_years})] / {annual_return:.1%}  
- **Result**: **{format_currency(required_nest_egg)}**
""")

    if additional_needed > 0:
        st.markdown(f"""
### 3. Required Monthly Savings  
- **Shortfall**: {format_currency(required_nest_egg)} - {format_currency(future_current_savings)} = **{format_currency(additional_needed)}**  
- **Formula**: `PMT = FV × r / [(1 + r)^n - 1]`  
- **Annual Calculation**: {format_currency(additional_needed)} × {annual_return:.1%} / [(1 + {annual_return:.1%})^{years_to_retirement} - 1]  
- **Monthly Result**: **{format_currency(monthly_savings)} / month**
""")
    else:
        st.success("🎉 Your current savings are sufficient for your retirement goals!")

    render_retirement_chart(user_data, formulas)

def render_retirement_chart(user_data: Dict, formulas):
    """Render retirement planning visualization."""
    age = user_data.get('age')
    retirement_age = user_data.get('retirement_age')
    current_savings = user_data.get('savings') or user_data.get('current_savings')
    risk_tolerance = user_data.get('risk_tolerance', 'Moderate')

    if None in [age, retirement_age, current_savings]:
        st.warning("⚠️ Missing fields: age, retirement age, or current savings.")
        return

    try:
        return_rates = {'conservative': 0.05, 'moderate': 0.07, 'aggressive': 0.09}
        annual_return = return_rates[risk_tolerance.lower()]
    except KeyError:
        st.warning("⚠️ Invalid risk tolerance provided. Defaulting to Moderate (7%).")
        annual_return = 0.07

    if retirement_age <= age:
        st.error("❌ Retirement age must be greater than current age.")
        return

    # Generate year-by-year projections
    years = list(range(age, retirement_age + 1))
    savings_growth = []
    for year in years:
        years_elapsed = year - age
        future_value = formulas.future_value(current_savings, annual_return, years_elapsed)
        savings_growth.append(future_value)

    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=savings_growth,
        mode='lines+markers',
        name='Savings Growth',
        line=dict(width=3),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title='Projected Savings Growth Over Time',
        xaxis_title='Age',
        yaxis_title='Savings Amount (₹)',
        hovermode='x unified',
        template='plotly_white'
    )
    fig.update_layout(yaxis_tickformat=',.0f')
    st.plotly_chart(fig, use_container_width=True)

def render_scenario_analysis(user_data: Dict):
    """Render interactive scenario analysis tools."""
    st.markdown("### 🔄 Scenario Analysis")
    
    # Safely extract required values
    age = user_data.get('age')
    retirement_age = user_data.get('retirement_age')
    current_income = user_data.get('income') or user_data.get('current_income')
    current_savings = user_data.get('savings') or user_data.get('current_savings')

    if None in [age, retirement_age, current_income, current_savings]:
        st.warning("⚠️ Please complete all required fields (age, income, savings, retirement age) to run scenario analysis.")
        return

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retirement Age Impact")
        
        base_retirement_age = retirement_age
        scenario_retirement_ages = [base_retirement_age - 2, base_retirement_age, base_retirement_age + 2]
        
        for scenario_age in scenario_retirement_ages:
            years_to_retirement = scenario_age - age
            if years_to_retirement > 0:
                from formulas import FinancialFormulas
                formulas = FinancialFormulas()

                annual_return = 0.07  # Default moderate return
                retirement_income_target = current_income * 0.8
                
                future_current_savings = formulas.future_value(current_savings, annual_return, years_to_retirement)
                required_nest_egg = formulas.present_value_annuity(retirement_income_target, annual_return, 25)
                additional_needed = max(0, required_nest_egg - future_current_savings)
                
                if additional_needed > 0:
                    required_monthly = formulas.payment_for_future_value(additional_needed, annual_return, years_to_retirement) / 12
                    st.metric(f"Retire at {scenario_age}", format_currency(required_monthly), 
                             delta=f"vs age {base_retirement_age}" if scenario_age != base_retirement_age else None)
                else:
                    st.metric(f"Retire at {scenario_age}", "✅ On Track")
    
    with col2:
        st.subheader("Risk Tolerance Impact")
        
        risk_scenarios = {
            'Conservative (5%)': 0.05,
            'Moderate (7%)': 0.07,
            'Aggressive (9%)': 0.09
        }
        
        for risk_name, return_rate in risk_scenarios.items():
            years_to_retirement = retirement_age - age
            if years_to_retirement > 0:
                from formulas import FinancialFormulas
                formulas = FinancialFormulas()

                retirement_income_target = current_income * 0.8
                future_current_savings = formulas.future_value(current_savings, return_rate, years_to_retirement)
                required_nest_egg = formulas.present_value_annuity(retirement_income_target, return_rate, 25)
                additional_needed = max(0, required_nest_egg - future_current_savings)
                
                if additional_needed > 0:
                    required_monthly = formulas.payment_for_future_value(additional_needed, return_rate, years_to_retirement) / 12
                    st.metric(risk_name, format_currency(required_monthly))
                else:
                    st.metric(risk_name, "✅ On Track")

def render_chat_suggestions():
    """Render suggested follow-up questions."""
    st.subheader("💡 Ask me about:")
    
    suggestions = [
        "What if inflation rises to 5%?",
        "Can I retire 2 years earlier?",
        "Should I pay off my mortgage or invest?",
        "How much should I save for emergencies?",
        "What if I increase my income by 20%?",
        "Show me the math behind these calculations"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                # Add suggestion to chat
                st.session_state.messages.append({"role": "user", "content": suggestion})
                st.rerun()


def render_chat_interface(agent):
    if not st.session_state.get('questionnaire_completed', False):
        render_questionnaire(agent)
    else:
        render_chat_messages()
        render_chat_input(agent)
