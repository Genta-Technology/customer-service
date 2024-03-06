"""
Basic utilities files that consist of helper code for api.py
"""

import json
import time
from fastapi import HTTPException


def check_package(request_data: dict):
    """
    Check package recieved from the API

    Return none if package contained all items,
        raise error 206 if chatbot_token is not provided,
            chatbot_session_id is not provided,
            if chat_history is not provided
    """

    if request_data.get('chatbot_token') is None:
        return HTTPException(status_code=206, detail="chatbot_token is not provided")
    if request_data.get('chatbot_session_id') is None:
        return HTTPException(status_code=206, detail="chatbot_session_id is not provided")
    if request_data.get('chat_history') is None:
        return HTTPException(status_code=206, detail="chat_history is not provided")


def validate_token(input_token: str, default_token: str):
    """
    Check if the input token is valid by comparing it to the default token
    """
    return input_token == default_token


def check_chat_length(chat_history: list, max_size: int):
    """
    Check if the total length of chat by the user is less than 'max_size'.

    Parameters:
    - chat_history (list): A list containing the chat messages.
    - max_size (int): The maximum total length allowed for the chat messages.

    Returns:
    - bool: True if the total length of chat messages is less than 'max_size', False otherwise.
    """
    total_length = len([message for message in chat_history if message.get('role') == 'user'])

    return total_length <= max_size

def get_current_time():
    """
    Return the int of the current UNIX time
    """

    return int(time.time())


def save_conversation(chatbot_session_id: str,
                      chatbot_time: int,
                      chat_history: list,
                      json_path: str):
    """
    Adds a new chat entry or updates an existing one in the JSON file.

    :param chat_id: str - The unique identifier for the chat.
    :param time_last_conversation: int - The timestamp of the last conversation.
    :param chat_history: list - A list of dictionaries representing the chat history.
    :param json_path: str - The path to the JSON file.
    """

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'data' not in data:
        data['data'] = []

    # Check if the chat_id already exists and remove the existing entry if found
    existing_chat_index = next((index for (index, d)
                                in enumerate(data['data'])
                                if d["chat_id"] == chatbot_session_id), None)
    if existing_chat_index is not None:
        del data['data'][existing_chat_index]

    # Append or update the chat in the 'chats' list
    data['data'].append({
        'chat_id': chatbot_session_id,
        'time_last_conversation': chatbot_time,
        'chat_history': chat_history
    })

    # Write the updated content back to the JSON file
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def get_system(json_path: str):
    """
    Read the JSON file and search the system for the AI

    Return a string of the AI system
    """

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if 'system' not in data:
        data['system'] = "you are a helpful assistant"
    
    return data['system']