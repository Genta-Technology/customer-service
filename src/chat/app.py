"""
This is the demo UI interface for the Chatbot API
"""

import streamlit as st
import requests
import uuid

url_chat = "http://127.0.0.1:8000/chatbot"

if 'chat_id' not in st.session_state:
    st.session_state['chat_id'] = str(uuid.uuid4())

def call_customer_service(messages: list, api_key: str):
    """
    Call the customer service bot API and return the new chat
    """

    chatbot_data = {
        "chatbot_token": api_key,
        "chatbot_session_id": st.session_state['chat_id'],
        "chat_history": messages
        }

    response = requests.request("POST", url=url_chat, json=chatbot_data)

    return response.json()["updated_chat"]

st.title("Genta Customer Service")
st.caption("A simple demonstration of integrated GentaAPI for customer service purposes")
st.caption(st.session_state['chat_id'])

# Ask user to input their API Token
genta_api_key = st.text_input("Customer Service API key", key="chatbot_api_key", type="password")

# Initialize a new message if there isn't a message in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# If user inputted something in the chat input, call the API for the response
user_input = st.text_input("Type your message here:", )
if user_input:
    # Update the chat history immediately with the user's message and API's response
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"] = call_customer_service(st.session_state["messages"], genta_api_key)

# Display all messages in the chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

