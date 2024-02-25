"""
API Core for AI Customer Service System.

This module serves as the main application for the API, 
constituting the core of the AI customer service system. 
It is designed to facilitate communication between the 
dashboard and the underlying data and functionalities of the system.

Key Functions:
    - Interface with the dashboard: Enables data exchange for monitoring and management tasks.
    - Integration with LangChain submodule: Utilizes LangChain for AI inference, 
        leveraging its capabilities to process and understand customer queries effectively.

Usage:
    The API acts as a middleware, processing requests 
    from the dashboard to access or modify data. 
    It also handles the invocation of the LangChain 
    submodule to generate AI responses based on the input data.

Important:
    Ensure that the LangChain submodule is correctly set up 
    and configured to work seamlessly with this API. 
    The integration is crucial for the effective 
    functioning of the AI customer service system.
"""

import uuid

from api.api_utils import check_package, validate_token, check_chat_length, get_current_time, save_conversation
from langchain.langchain import langchain_main

from genta import GentaAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utilities.utilities import EnvironmentVariables
from contextlib import asynccontextmanager

env = EnvironmentVariables()

# The file location of the database
JSON_DATABASE_URL = 'chat_history.json'

# The token for dashboard communication
DASHBOARD_TOKEN = env['DASHBOARD_TOKEN']

# Chatbot token is the token generated to validate input from the website in which the customer service chatbot is implemented
default_chatbot_token = ''

# Chatbot status is the bot status if the bot is turned on or off by the manager software, defaulted to on
chatbot_active = True

# Max chat size is the maximum user request, set default to 10 but can be changed in the dashboard
max_chat_size = 10

# Genta API for AI Inference purposes
GENTA_API_KEY = env['GENTA_API_KEY']
GENTA_API = GentaAPI(GENTA_API_KEY)

@asynccontextmanager
async def lifespan():
    '''
    Function that only run once while the API is starting
    '''

    # Load database

    # Create Token for API Access
    default_chatbot_token = uuid.uuid4()

app = FastAPI(lifespan=lifespan)

# Allow CORS (Removing CORS Error)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/chatbot')
async def chatbot_api(request_data: dict):
    """
    Main function that handle the main chat from the website

    Consumed dictionary data in form of
    {
        chatbot_token: UUID,
        chatbot_session_id: UUID,
        chat_history: [{'role': 'user', 'content':user_input}, 
                        {'role':'response', 'content': llm_output}]
    }
    """

    # Verify that the user send data is complete
    check_package(request_data)

    # Get the data
    chatbot_token = request_data.get('chatbot_token')
    chatbot_session_id = request_data.get('chatbot_session_id')
    chat_history = request_data.get('chat_history')

    # Check chatbot token
    if not validate_token(chatbot_token, default_chatbot_token):
        raise HTTPException(status_code=206, detail="chatbot_token is not valid")

    # Check chatbot active
    if not chatbot_active:
        raise HTTPException(
            status_code=206,
            detail="chatbot is currently unavailable/disabled, please contact your administrator")

    # Check total chat if its greater than the max value
    if not check_chat_length(chat_history, max_chat_size):
        raise HTTPException(status_code=206, detail="you have exceed the maximum chat limit")

    # Forward the data to the langchain part for inference
    builded_chat = langchain_main(chat_history)

    # Call Genta API
    response = GENTA_API.ChatCompletion(builded_chat,
                                        model_name='llama2-7b')

    # Update the JSON database for chat history
    save_conversation(chatbot_session_id=chatbot_session_id,
                      chatbot_time=get_current_time,
                      chat_history=chat_history,
                      json_path=JSON_DATABASE_URL)

    return response

@app.post('/set_chat_token')
def set_chat_token(request_data: dict):
    """
    Generate a new chat token, only able to do it from the dashboard
    """
    global default_chatbot_token

    if not validate_token(request_data.get('dashboard_token'), DASHBOARD_TOKEN):
        raise HTTPException(status_code=206, detail="Dashboard token is not valid")

    default_chatbot_token = uuid.uuid4()
    return JSONResponse(content={"chatbot_token": str(default_chatbot_token)})

@app.post('/get_chat_token')
def get_chat_token(request_data: dict):
    """
    Return the chat token, only able to do it from the dashboard
    """
    global default_chatbot_token
    
    if not validate_token(request_data.get('dashboard_token'), DASHBOARD_TOKEN):
        raise HTTPException(status_code=206, detail="Dashboard token is not valid")
    
    return JSONResponse(content={"chatbot_token": str(default_chatbot_token)})

@app.post('/chat_status')
def chat_status():
    """
    Check if the chatbot is active
    """
    return JSONResponse(content={"chatbot_status": chatbot_active})

@app.post('/chat_off')
def chat_off(request_data: dict):
    """
    Turn off the chat feature, only able to do it from the dashboard
    """
    if not validate_token(request_data.get('dashboard_token'), DASHBOARD_TOKEN):
        raise HTTPException(status_code=206, detail="Dashboard token is not valid")
    global chatbot_active
    chatbot_active = False
    return JSONResponse(content={"chatbot_status": chatbot_active})

@app.post('/chat_on')
def chat_on(request_data: dict):
    """
    Turn on the chat feature, only able to do it from the dashboard
    """
    if not validate_token(request_data.get('dashboard_token'), DASHBOARD_TOKEN):
        raise HTTPException(status_code=206, detail="Dashboard token is not valid")
    global chatbot_active
    chatbot_active = True
    return JSONResponse(content={"chatbot_status": chatbot_active})

@app.post('/chat_size')
def chat_size():
    """
    Check the maximum chat size allowed
    """
    return JSONResponse(content={"chat_size": chat_size})

@app.post('/chat_size_set')
def chat_size_set(request_data: dict):
    """
    Set the maximum chat size allowed, only able to do it from the dashboard
    """
    if not validate_token(request_data.get('dashboard_token'), DASHBOARD_TOKEN):
        raise HTTPException(status_code=206, detail="Dashboard token is not valid")
    
    chat_size = request_data.get('max_size')
    return JSONResponse(content={"chat_size": chat_size})
