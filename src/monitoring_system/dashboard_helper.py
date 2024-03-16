"""
A file for helper function that primarily serve the calling API for information and updating
"""
import json

api_url = "http://127.0.0.1:8000"


import requests

def get_bot_token(dashboard_token: str):
    """
    Get the chat bot access token
    """

    data = {
        "dashboard_token": dashboard_token
    }

    response = requests.request("POST", url=api_url + "/get_chat_token", json=data, timeout=10)

    return response.json()['chatbot_token']

def set_bot_token(dashboard_token: str):
    """
    Rewrite the chat bot access token
    """

    data = {
        "dashboard_token": dashboard_token
    }

    response = requests.request("POST", url=api_url + "/set_chat_token", json=data, timeout=10)

    return response.json()['chatbot_token']

def get_bot_status():
    """
    get the bot status (on or off)
    """
    
    response = requests.request("POST", url=api_url + "/chat_status", timeout=10)

    return response.json()["chatbot_status"]

def set_bot_off(dashboard_token: str):
    """
    Set the bot status to off
    """

    data = {
        "dashboard_token": dashboard_token
    }

    response = requests.request("POST", url=api_url + "/chat_off", json=data, timeout=10)

    return response.json()['chatbot_status']

def set_bot_on(dashboard_token: str):
    """
    Set the bot status to on
    """

    data = {
        "dashboard_token": dashboard_token
    }

    response = requests.request("POST", url=api_url + "/chat_on", json=data, timeout=10)

    return response.json()['chatbot_status']

def get_chat_size():
    """
    Get from the API the maximum chat size
    """

    response = requests.request("POST", url=api_url + "/chat_size", timeout=10)

    return response.json()["chat_size"]

def set_chat_size(dashboard_token: str, size:str):
    """
    Set the new chat size for the API
    """

    data = {
        "dashboard_token": dashboard_token,
        "max_size": size
    }

    response = requests.request("POST", url=api_url + "/chat_size_set", json=data, timeout=10)

    return response.json()['chat_size']

def read_system_prompt(json_path:str):
    """
    Read the system prompt from the JSON file
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if 'system' not in data:
        data['system'] = "you are a helpful assistant"
    
    return data['system']

def write_system_prompt(system_prompt:str, json_path:str):
    """
    Rewrite the new prompt into the JSON file
    """

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Update the 'system' key with the new prompt
    data['system'] = system_prompt

    # Write the updated data back to the file
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def get_chat_parameter(dashboard_token: str):
    """
    Get the temperature and max token parameter
    """

    data = {
        "dashboard_token": dashboard_token
    }

    response = requests.request("POST", url=api_url + "/chat_parameter", json=data, timeout=10)

    return response.json()['temperature'], response.json()['max_token']

def set_chat_parameter(temperature:float, max_token:int, dashboard_token:str):
    """
    Set the temperature and max token parameter
    """

    data = {
        "dashboard_token": dashboard_token,
        "temperature": temperature,
        "max_token": max_token
    }

    response = requests.request("POST", url=api_url + "/chat_parameter_set", json=data, timeout=10)

    return response.json()['temperature'], response.json()['max_token']