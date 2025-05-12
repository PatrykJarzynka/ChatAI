import pytest
from sqlmodel import Session

from models.user_chat_data import UserChatData
from tables.chat_item import ChatItem
from tables.chat import Chat
from services.chat_service import ChatService
from enums.tenant import Tenant
from tables.user import User
from typing import cast


@pytest.fixture
def chat_service(session: Session):
    return ChatService(session)

@pytest.fixture
def init_user_fixture(session: Session) -> User:
    new_user = User(email='test@test.pl', password='someHashedPassword',full_name='XYZ', tenant=Tenant.LOCAL)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    new_user.tenant_id = str(new_user.id)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

@pytest.fixture
def init_chat_fixture(init_user_fixture: User, session: Session) -> Chat:
    chat = Chat(user_id=init_user_fixture.id)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat


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


def test_add_chat_item_to_chat(chat_service: ChatService, init_chat_fixture: Chat):
    chat_item = ChatItem(user_message='Hello there', chat_id=init_chat_fixture.id)
    
    chat_service.add_chat_item_to_chat(chat_item, init_chat_fixture.id)

    current_chat = chat_service.get_chat_by_id(init_chat_fixture.id)

    assert current_chat is not None, "Chat not found when it should exist"
    assert chat_item in current_chat.chat_items

    
def test_save_chat(chat_service: ChatService, init_user_fixture: User):
    chat = Chat(user_id=init_user_fixture.id)
    chat_service.save_chat(chat)
    
    assert chat.id is not None

    saved_chat = chat_service.get_chat_by_id(chat.id)
    
    assert saved_chat is not None
    assert saved_chat == chat
    assert saved_chat.chat_items == []


def test_get_chat_items(chat_service: ChatService, init_user_fixture: User):
    initial_chat_items = [ChatItem(user_message='Hello there', chat_id=1, bot_message='Hello'),
                          ChatItem(user_message='How are you?', chat_id=1, bot_message='Good.')]
    
    chat = Chat(chat_items=initial_chat_items, user_id=init_user_fixture.id)

    chat_service.save_chat(chat)

    assert chat.id is not None

    chat_items = chat_service.get_chat_items(chat.id)

    assert initial_chat_items == chat_items


def test_get_chat_by_id(chat_service: ChatService, init_chat_fixture: Chat):
    assert init_chat_fixture.id is not None

    result = chat_service.get_chat_by_id(init_chat_fixture.id)

    assert result == init_chat_fixture


def test_delete_chat(chat_service: ChatService, init_chat_fixture: Chat):
    assert init_chat_fixture.id is not None

    chat_service.delete_chat(init_chat_fixture.id)

    assert chat_service.get_chat_by_id(init_chat_fixture.id) is None
