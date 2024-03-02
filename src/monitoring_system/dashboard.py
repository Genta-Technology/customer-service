"""
This is the main file for the dashboard menu
"""

import streamlit as st
import os

def dashboard_page():
    """
    Main dashboard page
    """
    #st.set_page_config(page_icon="./genta_logo.png")
    st.title('Dashboard')
    st.write('Welcome to the dashboard!')

    # Dashboard stuff (graph, etc put here)

    st.title("Control Panel")
    # Bot Status Control Panel

    col1, col2, col3 = st.columns(3)

    # Col 1, turn off bot button
    with col1:
        bot_stop_button = st.button("stop bot", type="primary")
        if bot_stop_button:
            st.session_state.stop_bot = "true"
            # Call the API to stop the Bot Activity and refresh
    
    # Col 2, bot status
    with col2:
        # Call API for Bot Status
        bot_status = True

        # Display the bot status
        display_status(bot_status)

    # Col 3, turn on bot button
    with col3:
        bot_start_button = st.button("start bot", type="primary")
        if bot_start_button:
            st.session_state.stop_bot = "false"
            # Call the API to stop the Bot Activity and refresh
    
    # Set max chat size
    chat_size = 10 # Call API for chat size
    chat_size_setting = st.number_input("Chat Limit", key="chat_limit", value=chat_size, min_value=5, max_value=100, step=1)

    if chat_size_setting != chat_size:
        # Update the API for change in chat size and then refresh the page
        pass

    st.title("Chatbot Panel")
    # Control panel to adjust the bot prompt and temperature

    # Prompt
    current_prompt = "Prompt 1" # Call API for current prompt
    input_prompt = st.text_area(label="Chatbot Prompt:",value=current_prompt)

    if input_prompt != current_prompt:
        print("hehe")

def display_status(status: bool):
    """
    Function to display a colored rectangle based on the status
    """
    color = "green" if status else "red"
    st.markdown(f"""
        <style>
        .rectangle {{
            width: 100px;
            height: 50px;
            background-color: {color};
        }}
        </style>
        <div class="rectangle"></div>
        """, unsafe_allow_html=True)