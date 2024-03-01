"""
This are the login menu for the streamlit dashboard app
"""
import streamlit as st
from utilities.utilities import EnvironmentVariables
env = EnvironmentVariables()

def login_page():
    """
    Main Login Function
    """
    st.title('Login Page')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if username == env["DASHBOARD_USERNAME"] and password == env["DASHBOARD_PASSWORD"]:  # Simple authentication logic
            st.session_state['authenticated'] = True
            st.experimental_rerun()
        else:
            st.error('Incorrect username or password.')