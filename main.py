import streamlit as st
import os
from agent import FinancialPlanningAgent
from ui import render_sidebar, render_chat_interface, render_formula_explanation
from utils import initialize_session_state, format_currency

def main():
    st.set_page_config(
        page_title="Financial Planning Advisor",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("💰 Financial Planning Advisor")
    st.markdown("Get personalized retirement planning advice powered by proven financial formulas and conversational AI.")

    # Initialize session state
    initialize_session_state()

    # Initialize the agent
    if 'agent' not in st.session_state:
        st.session_state.agent = FinancialPlanningAgent()
    
    # Clear any mock data if questionnaire hasn't been completed
    if not st.session_state.get('questionnaire_completed', False):
        st.session_state.agent.user_data = {}
        st.session_state.user_data = {}

    # Create layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Main chat interface
        render_chat_interface(st.session_state.agent)

    with col2:
        # Sidebar with summary and formula explanation
        render_sidebar()
        
        # Formula explanation section
        if st.session_state.get('show_formula_explanation', False):
            render_formula_explanation()


if __name__ == "__main__":
    main()
