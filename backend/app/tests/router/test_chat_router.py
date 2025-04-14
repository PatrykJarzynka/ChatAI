import pytest
from unittest.mock import patch

from sqlmodel import Session
from starlette.testclient import TestClient

from db_models.chat_item_model import ChatItem
from db_models.chat_model import Chat
from services.open_ai_chat_service import OpenAIChatService
from services.auth.jwt_service import JWTService

@pytest.fixture
def jwt_service():
    return JWTService()



def test_get_new_chat(session: Session, client: TestClient, jwt_service: JWTService):
    test_token = jwt_service.create_access_token({"sub": '1'})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    response = client.get("/chat", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["chat_items"] == []


def test_get_chat_histories(session: Session, client: TestClient, jwt_service: JWTService):
    test_token = jwt_service.create_access_token({"sub": '1'})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    chat_items = [ChatItem(user_message='Hello', bot_message='Hello.')]
    chat_items2 = [ChatItem(user_message='Hello!', bot_message='Hello!')]
    chat = Chat(chat_items=chat_items, user_id=1)
    chat2 = Chat(chat_items=chat_items2, user_id=2) #second_user

    session.add(chat)
    session.add(chat2)
    session.commit()
    session.refresh(chat)

    response = client.get(f"/chat/history?userId={1}", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data == [{"id": chat.id, "title": chat_items[0].user_message}]


def test_get_chat_by_id(session: Session, client: TestClient, jwt_service: JWTService):
    test_token = jwt_service.create_access_token({"sub": '1'})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    chat_items = [ChatItem(user_message='Hello', bot_message='Hello.')]
    chat = Chat(chat_items=chat_items, user_id=1)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    response = client.get(f"/chat/{chat.id}", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data == {"id": chat.id, "chat_items": [
        {"user_message": chat_items[0].user_message, "bot_message": chat.chat_items[0].bot_message}]}


def test_on_user_query_send(session: Session, client: TestClient, jwt_service: JWTService):
    test_token = jwt_service.create_access_token({"sub": '1'})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    chat = Chat(chat_items=[], user_id=1)
    session.add(chat)
    session.commit()

    user_chat_data = {
        "message": "Hello",
        "chat_id": 1
    }

    mock_response = "Mock response."

    with patch.object(OpenAIChatService, "fetch_bot_response", return_value=mock_response) as mock_fetch:
        response = client.post("/chat", json=user_chat_data, headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert data == mock_response
    assert mock_fetch.call_count == 1
