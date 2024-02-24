"""
This is the test file for the main API function
"""

import pytest

from api.api import app
from fastapi.testclient import TestClient
from utilities.utilities import EnvironmentVariables

env = EnvironmentVariables()

DASHBOARD_TOKEN = env['DASHBOARD_TOKEN']
INVALID_TOKEN = "invalid_token_random_gibberish"

@pytest.fixture
def client():
    """
    create client app for test case
    """
    return TestClient(app)

def test_new_chat_token(client):
    """
    Test the /set_chat_token and /get_chat_token
    """

    # Get the old chat token
    response_old_chat_token = client.post('/get_chat_token', json={'dashboard_token': DASHBOARD_TOKEN})
    assert response_old_chat_token.status_code == 200
    old_chat_token = response_old_chat_token.json()['chatbot_token']

    # Set the new chat token
    response_set_new_chat_token = client.post('/set_chat_token', json={'dashboard_token': DASHBOARD_TOKEN})
    assert response_set_new_chat_token.status_code == 200
    generated_new_chat_token = response_set_new_chat_token.json()['chatbot_token']
    assert old_chat_token != generated_new_chat_token

    # Get the new chat token
    response_new_chat_token = client.post('/get_chat_token', json={'dashboard_token': DASHBOARD_TOKEN})
    assert response_new_chat_token.status_code == 200
    new_chat_token = response_new_chat_token.json()['chatbot_token']

    # Compare the chat token
    assert old_chat_token != new_chat_token