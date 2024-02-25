import requests
import uuid

from utilities.utilities import EnvironmentVariables

env = EnvironmentVariables()

url_key = "http://127.0.0.1:8000/get_chat_token"
url_key_rewrite = "http://127.0.0.1:8000/set_chat_token"
url_chat = "http://127.0.0.1:8000/chatbot"

# The token for dashboard communication
DASHBOARD_TOKEN = env['DASHBOARD_TOKEN']

# Create a new key
chatbot_token = requests.request("POST", url=url_key, json={'dashboard_token': DASHBOARD_TOKEN}).json()['chatbot_token']

print(chatbot_token)

chat = [
    {"role": "user", "content": "How much does a car cost?"}
]

chatbot_data = {
    "chatbot_token": chatbot_token,
    "chatbot_session_id": str(uuid.uuid4()),
    "chat_history": chat
}

response = requests.request("POST", url=url_chat, json=chatbot_data)

print(response.status_code)
print(response.json())