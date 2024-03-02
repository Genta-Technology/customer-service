"""
Streamlit-based Dashboard for AI Customer Service Monitoring.

This module implements a dashboard using Streamlit for monitoring and managing
an AI customer service system. It provides real-time oversight and interaction
capabilities for chat service administrators and managers.

Features:
- Chat Monitoring: View live customer-AI interactions for quality assurance.
- Message Management: Delete or modify messages for error correction.
- Analytics Dashboard: Access usage patterns and performance metrics.
- Secure Login: Restrict dashboard access to authorized personnel.

Getting Started:
To run the dashboard, ensure Streamlit is installed and execute:
`streamlit run dashboard.py`
Login is required for access.

Prerequisites:
- Python 3.x
- Streamlit
- Dependencies listed in requirements.txt

NOTES FOR API Developers:

    Session state dashboard:
    {
        "password": str (unhashed)
        "chat_limit":int
        "messages": list
        "stop_bot": str: "true" or "false"
        "username": str
    }

Note:
Ensure API communication with the intended website and LangChain for RAG
(Retrieval-Augmented Generation) are properly configured for seamless integration.
"""

import streamlit as st 

from monitoring_system.dashboard import dashboard_page
from monitoring_system.login import login_page
from monitoring_system.chats import chats_page

from PIL import Image

# Genta Logo
logo = Image.open("genta_logo.png")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

st.set_page_config(page_icon="./genta_logo.png")
st.sidebar.image(logo, use_column_width="always")

st.sidebar.title('Navigation')
page = st.sidebar.radio('Menu', ['Dashboard', 'Chat'], 
                        disabled=not st.session_state['authenticated'], 
                        label_visibility="hidden")

if page == 'Login' or not st.session_state['authenticated']:
    login_page()
elif page == 'Dashboard':
    dashboard_page()
elif page == 'Chat':
    chats_page()

if st.session_state['authenticated']:
    if st.sidebar.button('Logout'):
        st.session_state['authenticated'] = False
        st.experimental_rerun()
