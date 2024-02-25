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
from PIL import Image

def verify(username:str, password:str) -> bool:
    """Dummy API

    Args:
        username (str): username to be checked
        password (str): password to be checked

    Returns:
        bool: True if verified, else False
    """
    
    # call database check here
    return True if username == "genta" and password == "genta0" else False

def fetch_message_database(username:str, password:str):
    if verify(username, password):
        # call for chat database
        return {
        "username": "genta",
        "chatbot_token": "0000",
        "chatbot_session_id": "0000",
        "chat_history": [{'role': 'user', 'content':"test data input 01"}, 
                         {'role':'response', 'content': "API output 01"}]
    }
    else:
        return {"chat_history": []}

def delete_last_response():
    if  "messages" in st.session_state and st.session_state.messages and st.session_state.messages[-1]["role"] == "response":
        # also delete the response in database here 
        st.session_state.messages = st.session_state.messages[:-1]
    else:
        st.warning("cannot delete last message")

def edit_last_message():
    if  "messages" in st.session_state and st.session_state.messages and st.session_state.messages[-1]["role"] == "response":
        st.session_state.messages[-1]["content"] = st.chat_input()
    else:
        st.warning("cannot edit last message")

logo = Image.open("./genta_logo.png")

PAGE_CONFIG = {"page_title": "Chat Dashboard", "page_icon": "./genta_logo.png"}

st.set_page_config(**PAGE_CONFIG)

with st.sidebar:
    st.title("Control Panel")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image(logo, use_column_width="always")
    
    genta_username = st.text_input("username", key="username", type="default")
    genta_password = st.text_input("password", key="password", type="password")
    if verify(genta_username, genta_password):
        stop_button_placeholder, start_button_placeholder = st.columns(2)
        
        with stop_button_placeholder: 
            stop_button = st.button("stop bot", type="primary")
            if stop_button:
                st.session_state.stop_bot = "true"
                
        with start_button_placeholder: 
            start_button = st.button("start bot")
            if start_button:
                st.session_state.stop_bot = "false"
        
        # set chat token here
        st.number_input("Chat Limit", key="chat_limit", min_value=0, max_value=30, step=1)
        
        advanced = st.toggle("Advanced Mode")
        if advanced:
            temperature = st.slider(
                ':blue[Temperature]',
                0.0, 2.0, 1.0)
            
            # Set the model max token to be generated
            max_length = st.slider(
                ":blue[Maximum lenght]",
                0, 4096, 2048
            )

            # Set the model top P value
            top_p = st.slider(
                ":blue[Top P]",
                0.0, 0.1, 0.95
            )

            # Set the model repetition penalty
            rep_penalty = st.slider(
                ":blue[Repetition penalty]",
                0.0, 2.0, 1.03
            )
    elif genta_username and genta_password:
        st.caption(":red[Wrong username or password]")

st.title("Genta Social Media API Manager")
st.caption("Manage your social media account with Genta Technology")

if "messages" not in st.session_state :
    st.session_state["messages"] = fetch_message_database(genta_username, genta_password)["chat_history"]

if "stop_bot" not in st.session_state:
    st.session_state["stop_bot"] = "false"

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

st.write(st.session_state)