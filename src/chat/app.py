"""
This is the demo UI interface for the Chatbot API
"""

import streamlit as st
import requests

def call_customer_service(messages: list):
    """
    Call the customer service bot API and return the new chat
    """
    return [{"role": "user", "content": "prompt"}, {"role": "response", "content": "prompt"}]

st.title("Genta Customer Service")
st.caption("A simple demonstration of integrated GentaAPI for customer service purposes")

# Initialize a new message if there isn't a message in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display all messages in the chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# If user inputted something in the chat input, call the API for the response
user_input = st.text_input("Type your message here:")
if user_input:
    # Update the chat history immediately with the user's message and API's response
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"] = call_customer_service(st.session_state["messages"])

