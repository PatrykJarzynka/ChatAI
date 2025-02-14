from unittest.mock import patch

from sqlmodel import Session
from starlette.testclient import TestClient

from app.db_models.chat_item_model import ChatItem
from app.db_models.chat_model import Chat
from app.services.bot_service import BotService


def test_get_new_chat(session: Session, client: TestClient):
    response = client.get("/chat")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["chat_items"] == []


def test_get_all_chats_history(session: Session, client: TestClient):
    chat_items = [ChatItem(user_message='Hello', bot_message='Hello.', user_id='testUser')]
    chat = Chat(chat_items=chat_items)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    response = client.get("/chat/history")
    data = response.json()
    assert response.status_code == 200
    assert data == [{"id": chat.id, "title": chat_items[0].user_message}]


def test_get_chat_by_id(session: Session, client: TestClient):
    chat_items = [ChatItem(user_message='Hello', bot_message='Hello.', user_id='testUser')]
    chat = Chat(chat_items=chat_items)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    response = client.get(f"/chat/{chat.id}")
    data = response.json()
    assert response.status_code == 200
    assert data == {"id": chat.id, "chat_items": [
        {"user_message": chat_items[0].user_message, "bot_message": chat.chat_items[0].bot_message}]}


def test_on_user_query_send(session: Session, client: TestClient):
    chat = Chat(chat_items=[])
    session.add(chat)
    session.commit()

    user_chat_data = {
        "message": "Hello",
        "user_id": "testUser",
        "chat_id": 1
    }

    mock_response = "Mock response."

    with patch.object(BotService, "fetch_bot_response", return_value=mock_response) as mock_fetch:
        response = client.post("/chat", json=user_chat_data)

    data = response.json()
    assert response.status_code == 200
    assert data == mock_response
    assert mock_fetch.call_count == 1
