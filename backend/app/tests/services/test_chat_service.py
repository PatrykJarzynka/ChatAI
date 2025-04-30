import pytest
from sqlmodel import Session

from models.user_chat_data import UserChatData
from db_models.chat_item_model import ChatItem
from db_models.chat_model import Chat
from services.chat_service import ChatService


@pytest.fixture
def chat_service(session: Session):
    return ChatService(session)


def test_create_new_chat(chat_service: ChatService):
    chat = chat_service.create_new_chat(1)
    assert isinstance(chat, Chat)


def test_create_chat_item(chat_service: ChatService):
    user_data = UserChatData(message="Hello", chat_id=1)
    expected_chat_item = ChatItem(user_message=user_data.message, chat_id=user_data.chat_id,
                                  bot_message=None)

    chat_item = chat_service.create_chat_item(user_data)

    assert isinstance(chat_item, ChatItem)
    assert chat_item == expected_chat_item


def test_add_chat_item_to_chat(chat_service: ChatService):
    initial_chat = Chat(chat_items=[], user_id=1)
    chat_service.save_chat(initial_chat)

    chat_item = ChatItem(user_message='Hello there', chat_id=initial_chat.id)

    chat_service.add_chat_item_to_chat(chat_item, initial_chat.id)

    current_chat = chat_service.get_chat_by_id(initial_chat.id)

    assert chat_item in current_chat.chat_items


def test_save_chat(chat_service: ChatService):
    chat = Chat(user_id=1)
    chat_service.save_chat(chat)

    saved_chat = chat_service.get_chat_by_id(chat.id)

    assert saved_chat == chat
    assert saved_chat.chat_items == []


def test_get_chat_items(chat_service: ChatService):
    initial_chat_items = [ChatItem(user_message='Hello there', chat_id=1, bot_message='Hello'),
                          ChatItem(user_message='How are you?', chat_id=1, bot_message='Good.')]
    chat = Chat(chat_items=initial_chat_items, user_id=1)

    chat_service.save_chat(chat)

    chat_items = chat_service.get_chat_items(chat.id)

    assert initial_chat_items == chat_items


def test_get_chat_by_id(chat_service: ChatService):
    chat = Chat(user_id=1)

    chat_service.save_chat(chat)

    result = chat_service.get_chat_by_id(chat.id)

    assert result == chat


def test_delete_chat(chat_service: ChatService):
    chat = Chat(user_id=1)

    chat_service.save_chat(chat)

    chat_service.delete_chat(chat.id)

    assert chat_service.get_chat_by_id(chat.id) is None
