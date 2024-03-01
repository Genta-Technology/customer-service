"""
This is the main file for the dashboard menu
"""

import streamlit as st 
from PIL import Image
import os

#def dashboard_page():
"""
Main dashboard page
"""
logo = Image.open("genta_logo.png")

PAGE_CONFIG = {"page_title": "GentaChat", "page_icon": "genta_logo.png"}

#st.set_page_config(page_icon="./genta_logo.png")
st.title('Dashboard')
st.write('Welcome to the dashboard!')

def fetch_message_database(g_usr, g_password):
    """test data

    Args:
        g_usr (_type_): _description_
        g_password (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [{"chatbot_token": "0001", 
             "chatbot_session_id": "XXXX",
             "chat_history": [{'role': 'user', 'content':"input 1"}, 
                              {'role':'response', 'content': "output 1"}]},
            {"chatbot_token": "0002", 
             "chatbot_session_id": "ADFGADF",
             "chat_history": [{'role': 'user', 'content':"input 1"}, 
                              {'role':'response', 'content': "output 1"}]},]

with st.sidebar:
    st.title("Control Panel")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image(logo, use_column_width="always")
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
        
st.title("Genta Social Media API Manager")
st.caption("Manage your social media account with Genta Technology")

if "messages" not in st.session_state :
    st.session_state["messages"] = fetch_message_database('admin', 'test')
    
if "stop_bot" not in st.session_state:
    st.session_state["stop_bot"] = "false"
    
for msg in st.session_state.messages:
    with st.container():
        total_keys = len(list(msg.keys()))-1
        list_of_cols = st.columns(total_keys)
        for i in range(total_keys):
            with list_of_cols[i]:
                st.write(msg[list(msg.keys())[i]])
        with st.expander("show messages"):
            col1_chat, col2_chat = st.columns(2)
            with col1_chat:
                st.button("delete last message", key=msg["chatbot_session_id"]+"delete", type="primary")
            with col2_chat:
                st.button("edit last message", key=msg["chatbot_session_id"]+"replace", type="secondary")
            for ch in msg["chat_history"]:
                st.chat_message(ch["role"]).write(ch["content"])

