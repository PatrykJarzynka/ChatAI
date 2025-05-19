import pytest
from unittest.mock import Mock

from starlette.testclient import TestClient

from models.chat_item_dto import ChatItemDTO
from tables.chat_item import ChatItem
from tables.chat import Chat
from tables.user import User
from models.user_chat_data import UserChatData
from enums.tenant import Tenant
from models.chat_dto import ChatDto
from services.auth.jwt_service import JWTService
from main import app
from containers import get_chat_service, get_user_service, get_bot_service, get_chat_history_service, auth_none
from typing import List, cast

mock_user = User(id=123, external_user_id='123', email='email@a.pl',password='password', tenant=Tenant.LOCAL, full_name='XYZ')
mock_chat=Chat(user_id=123, id=1, chat_items=[])
mock_bot_response = 'TEST'
mock_chat_item = ChatItem(user_message='Hello', chat_id=1)

@pytest.fixture
def jwt_service():
    return JWTService()

@pytest.fixture
def user_service():
    mock = Mock()
    mock.get_user_by_external_user_id.return_value = mock_user
    app.dependency_overrides[get_user_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def chat_service():
    mock = Mock()
    mock.create_new_chat.return_value = mock_chat
    mock.save_chat.return_value = None
    mock.get_chat_by_id.return_value = mock_chat
    mock.create_chat_item.return_value = mock_chat_item
    mock.delete_chat.return_value = None
    app.dependency_overrides[get_chat_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def chat_history_service():
    mock = Mock()
    mock.get_chats_history_data_by_user_id.return_value = []
    app.dependency_overrides[get_chat_history_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def bot_service():
    mock = Mock()
    mock.chat.return_value = mock_bot_response
    app.dependency_overrides[get_bot_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def bot_service_chat_error():
    mock = Mock()
    mock.chat.side_effect = Exception('Test exception')
    app.dependency_overrides[get_bot_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_decode():
    mock = Mock()
    mock.return_value = {"sub": 'test_sub'}
    app.dependency_overrides[auth_none] = lambda: mock()
    yield mock
    app.dependency_overrides.clear()

def test_get_new_chat(client: TestClient, user_service, chat_service, overrite_decode):
    headers = {"Authorization": "Bearer access_token"}
    expected_response = ChatDto(id=1,chat_items=[])

    response = client.get('/chat', headers=headers)

    assert response.json() == expected_response.model_dump()
    overrite_decode.assert_called_once()
    user_service.get_user_by_external_user_id.assert_called_once_with('test_sub')
    chat_service.create_new_chat.assert_called_once_with(mock_user.id)
    chat_service.save_chat.assert_called_once_with(mock_chat)

def test_get_chat_histories(client: TestClient, chat_history_service, overrite_decode):
    headers = {"Authorization": "Bearer access_token"}

    response = client.get('/chat/history?userId=1', headers=headers)

    assert response.json() == []
    overrite_decode.assert_called_once()
    chat_history_service.get_chats_history_data_by_user_id.assert_called_once_with(1)

def test_get_chat_by_id(client: TestClient, chat_service, overrite_decode):
    headers = {"Authorization": "Bearer access_token"}
    expected_response = ChatDto(id=mock_chat.id, chat_items=cast(List[ChatItemDTO],mock_chat.chat_items)) #casting type because response model does the real casting in routing

    response = client.get('/chat/1', headers=headers)

    assert response.json() == expected_response.model_dump()
    overrite_decode.assert_called_once()
    chat_service.get_chat_by_id.assert_called_once_with(1)

def test_on_user_query_send(client: TestClient, chat_service, bot_service, overrite_decode):
    headers = {"Authorization": "Bearer access_token"}
    body = {
        "message": "Hello",
        "chat_id": 1
    }

    expected_chat_item=ChatItem(id=mock_chat_item.id, user_message=mock_chat_item.user_message, bot_message='TEST', chat_id=mock_chat_item.chat_id)

    response = client.post('/chat', headers=headers, json=body)

    assert response.json() == 'TEST'
    overrite_decode.assert_called_once()
    chat_service.create_chat_item.assert_called_once_with(UserChatData(message=body['message'], chat_id=body['chat_id']))
    bot_service.chat.assert_called_once_with(body['message'])
    chat_service.add_chat_item_to_chat.assert_called_once_with(expected_chat_item, body['chat_id'])


def test_on_user_query_send_exception(client: TestClient, overrite_decode, chat_service, bot_service_chat_error):
    headers = {"Authorization": "Bearer access_token"}
    body = {
        "message": "Hello",
        "chat_id": 1
    }

    response = client.post('/chat', headers=headers, json=body)

    overrite_decode.assert_called_once()
    chat_service.delete_chat.assert_called_once_with(body['chat_id'])
    assert response.status_code == 500
    assert response.json()['detail'] == 'Something went wrong: Test exception'