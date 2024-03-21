"""
Test call the FastAPI for requests on chatbot
"""
import uuid
import requests

from utilities.utilities import EnvironmentVariables

env = EnvironmentVariables()

URL_KEY = "http://127.0.0.1:8000/get_chat_token"
URL_CHAT = "http://127.0.0.1:8000/chatbot"

# The token for dashboard communication
DASHBOARD_TOKEN = env['DASHBOARD_TOKEN']

# Create a new key
chatbot_token = requests.request("POST",
                                 url=URL_KEY,
                                 json={'dashboard_token': DASHBOARD_TOKEN},
                                 timeout=10  # Add timeout argument to prevent program from hanging indefinitely
                                 ).json()['chatbot_token']

print(chatbot_token)

chat = [
    {"role": "user", "content": "How much does a car cost?"}
]

chatbot_data = {
    "chatbot_token": chatbot_token,
    "chatbot_session_id": str(uuid.uuid4()),
    "chat_history": chat
}

response = requests.request("POST",
                            url=URL_CHAT,
                            json=chatbot_data,
                            timeout=10)

print(response.status_code)
print(response.json())
