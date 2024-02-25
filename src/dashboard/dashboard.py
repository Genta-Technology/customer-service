import streamlit as st 
import numpy as np
from PIL import Image
import streamlit_authenticator as sa
from main import verify

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
        return {}

def delete_last_response():
    if "messages" in st.session_state and st.session_state.messages[-1]['role'] == "response":
            # also delete the response in database here
            st.session_state.messages = st.session_state.messages[:-1]
    else:
        st.toggle(":red[sorry last message is not from Genta]")

with st.sidebar():
    stop_button, delete_button, edit_button = st.columns(3)
        
    with stop_button: 
        st.button("stop bot", type="primary")
    with delete_button: 
        st.button("edit last response",
                    type="secondary",
                    on_click=delete_last_response())
        
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
if "messages" not in st.session_state:
    #st.session_state["messages"] = [{"role": "assistant", "content": "Ini adalah chat dari genta API"}]
    
        st.session_state["messages"] = fetch_message_database(genta_username, genta_password)["chat_history"]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])