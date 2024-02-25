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
    response_old_chat_token = client.post(
        '/get_chat_token', json={'dashboard_token': DASHBOARD_TOKEN})
    assert response_old_chat_token.status_code == 200
    old_chat_token = response_old_chat_token.json()['chatbot_token']

    # Set the new chat token
    response_set_new_chat_token = client.post(
        '/set_chat_token', json={'dashboard_token': DASHBOARD_TOKEN})
    assert response_set_new_chat_token.status_code == 200
    generated_new_chat_token = response_set_new_chat_token.json()[
        'chatbot_token']
    assert old_chat_token != generated_new_chat_token

    # Get the new chat token
    response_new_chat_token = client.post(
        '/get_chat_token', json={'dashboard_token': DASHBOARD_TOKEN})
    assert response_new_chat_token.status_code == 200
    new_chat_token = response_new_chat_token.json()['chatbot_token']

    # Compare the chat token
    assert old_chat_token != new_chat_token


def test_chat_status(client):
    """
    Test the chat status: /chat_status, /chat_off, /chat_on
    """

    response_current_status = client.post('/chat_status')
    # Check that the chat default is set to ON (True)
    assert response_current_status.status_code == 200
    assert response_current_status.json()['chatbot_status'] == True

    # Test turn off
    client.post('/chat_off', json={'dashboard_token': DASHBOARD_TOKEN})
    response_off_status = client.post('/chat_status')
    # Check that the chat default is set to ON (True)
    assert response_off_status.status_code == 200
    assert response_off_status.json()['chatbot_status'] == False

    # Test turn on
    client.post('/chat_on', json={'dashboard_token': DASHBOARD_TOKEN})
    response_on_status = client.post('/chat_status')
    # Check that the chat default is set to ON (True)
    assert response_on_status.status_code == 200
    assert response_on_status.json()['chatbot_status'] == True


def test_chat_size(client):
    """
    Test get the chat size by calling /chat_size and set the chat size by /chat_size_set
    """
    # Get current chat size
    response_current_chat_size = client.post('/chat_size')
    assert response_current_chat_size.status_code == 200

    # Set new chat size
    response_set_chat_size = client.post('/chat_size_set',
                                         json={'dashboard_token': DASHBOARD_TOKEN,
                                               'max_size': ((response_current_chat_size.json()['chat_size']) + 20)})

    assert response_set_chat_size.status_code == 200

    # Get new current chat size
    response_new_chat_size = client.post('/chat_size')
    assert response_new_chat_size.status_code == 200
    assert response_current_chat_size.json()['chat_size'] != (response_set_chat_size.json()[
        'chat_size'] == response_new_chat_size.json()['chat_size'])
