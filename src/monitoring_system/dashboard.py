"""
This is the main file for the dashboard menu
"""

import streamlit as st

from utilities.utilities import EnvironmentVariables

from monitoring_system.dashboard_helper import get_bot_token, set_bot_token, get_bot_status, set_bot_off, set_bot_on, get_chat_size, set_chat_size, read_system_prompt, write_system_prompt, get_chat_parameter, set_chat_parameter

env = EnvironmentVariables()
# The token for dashboard communication
DASHBOARD_TOKEN = env['DASHBOARD_TOKEN']

# The file location of the database
JSON_DATABASE_URL = 'chat_history.json'

def dashboard_page():
    """
    Main dashboard page
    """
    #st.set_page_config(page_icon="./genta_logo.png")
    st.title('Dashboard')
    st.write('Welcome to the dashboard!')

    tab1, tab2 = st.tabs(["Control Panel", "Chatbot Panel"])

    # Dashboard stuff (graph, etc put here) Tab 1

    tab1.title("Control Panel")
    # Bot Status Control Panel

    # Generate new chatbot token
    change_token_button = tab1.button("Generate new token")
    if change_token_button:
        bot_token = set_bot_token(DASHBOARD_TOKEN)
    
    # Show chatbot token
    bot_token = get_bot_token(DASHBOARD_TOKEN)
    tab1.write('Chatbot Token: ' + bot_token)

    col1, col2 = tab1.columns(2)

    # Col 1, turn off bot button
    with col1:
        bot_stop_button = st.button("stop bot")
        if bot_stop_button:
            tab1.session_state.stop_bot = "true"
            # Call the API to stop the Bot Activity and refresh
            bot_status = set_bot_off(DASHBOARD_TOKEN)
        
        bot_start_button = st.button("start bot")
        if bot_start_button:
            tab1.session_state.stop_bot = "false"
            # Call the API to stop the Bot Activity and refresh
            bot_status = set_bot_on(DASHBOARD_TOKEN)
    
    # Col 2, bot status
    with col2:
        # Call API for Bot Status
        bot_status = get_bot_status()

        # Display the bot status
        display_status(bot_status)
        
    
    # Set max chat size
    chat_size = get_chat_size()
    chat_size_setting = tab1.number_input("Chat Limit", key="chat_limit", value=chat_size, min_value=5, max_value=100, step=1)

    if chat_size_setting:
        # Update the API for change in chat size and then refresh the page
        chat_size = set_chat_size(DASHBOARD_TOKEN, chat_size_setting)

    tab2.title("Chatbot Panel")
    # Control panel to adjust the bot prompt and temperature


    # Prompt
    current_prompt = read_system_prompt(JSON_DATABASE_URL) # Call API for current prompt
    input_prompt = tab2.text_area(label="Chatbot Prompt:",value=current_prompt)

    # Create a button to update the prompt
    if tab2.button("Update System Prompt"):
        write_system_prompt(input_prompt, JSON_DATABASE_URL)
        tab2.success("Prompt updated!")

    # Fetch the current chat parameters from the API
    current_temperature, current_max_token = get_chat_parameter(DASHBOARD_TOKEN)

    # Set the model temperature
    temperature = tab2.slider(
        ':blue[Temperature]',
        0.0, 2.0, current_temperature)
        
    # Set the model max token to be generated
    max_length = tab2.slider(
        ":blue[Maximum lenght]",
        0, 4096, current_max_token
    )

    # Button to update the chat parameters
    if tab2.button("Update Chat Parameters"):
        updated_temperature, updated_max_token = set_chat_parameter(temperature, max_length, DASHBOARD_TOKEN)
        if updated_temperature == temperature and updated_max_token == max_length:
            st.success("Chat parameters updated successfully!")
        else:
            st.error("Failed to update chat parameters.")



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