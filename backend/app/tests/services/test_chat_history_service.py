import pytest
from sqlmodel import Session

from enums.tenant import Tenant
from models.chat_history import ChatHistory
from tables.chat_item import ChatItem
from tables.chat import Chat
from services.chat_history_service import ChatHistoryService
from services.chat_service import ChatService
from tables.user import User


@pytest.fixture
def chat_service(session: Session):
    return ChatService(session)


@pytest.fixture
def chat_history_service(session: Session):
    return ChatHistoryService(session)

@pytest.fixture
def local_user_fixture(session: Session) -> User:
    new_user = User(email='test@test.pl', password='someHashedPassword',full_name='XYZ', tenant=Tenant.LOCAL)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    new_user.external_user_id = str(new_user.id)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def test_convert_chat_with_items_to_history_data(chat_history_service: ChatHistoryService):
    chat = Chat(id=1,
                chat_items=[ChatItem(user_message='Hello there', chat_id=1, bot_message='Hello'),
                            ChatItem(user_message='How are you?', chat_id=1, bot_message='Good.')],
                            user_id=1)

    expected_data = ChatHistory(id=chat.id, title=chat.chat_items[0].user_message)
    chat_history_data = chat_history_service.convert_chat_to_history_data(chat)

    assert chat_history_data == expected_data


def test_convert_chat_with_no_items_to_history_data(chat_history_service: ChatHistoryService):
    chat = Chat(id=2, chat_items=[], user_id=1)

    expected_data = ChatHistory(id=chat.id, title='')
    chat_history_data = chat_history_service.convert_chat_to_history_data(chat)

    assert chat_history_data == expected_data


def test_get_chats_history_data_by_user_id(chat_history_service: ChatHistoryService, chat_service: ChatService, local_user_fixture: User):
    chat_1 = Chat(user_id=local_user_fixture.id, chat_items=[ChatItem(user_message='Hello there', bot_message='Hello'), ChatItem(user_message='How are you?', bot_message='Good.')])
    chat_2 = Chat(user_id=local_user_fixture.id, chat_items=[ChatItem(user_message='Hello.', bot_message='Hello.')])
    chat_3 = Chat(user_id=12, chat_items=[])

    chat_service.save_chat(chat_1)
    chat_service.save_chat(chat_2)
    chat_service.save_chat(chat_3)

    expected_data = [ChatHistory(id=chat_1.id, title=chat_1.chat_items[0].user_message),
                     ChatHistory(id=chat_2.id, title=chat_2.chat_items[0].user_message)]

    chat_histories = chat_history_service.get_chats_history_data_by_user_id(1)

    assert chat_histories == expected_data

def test_get_chats_by_user_id(chat_history_service: ChatHistoryService, chat_service: ChatService, local_user_fixture: User):
    chat_1 = Chat(user_id=local_user_fixture.id, chat_items=[ChatItem(user_message='Hello there', bot_message='Hello'), ChatItem(user_message='How are you?', bot_message='Good.')])
    chat_2 = Chat(user_id=local_user_fixture.id, chat_items=[ChatItem(user_message='Hello.', bot_message='Hello.')])
    chat_3 = Chat(user_id=12, chat_items=[])
    
    chat_service.save_chat(chat_1)
    chat_service.save_chat(chat_2)
    chat_service.save_chat(chat_3)

    chats = chat_history_service.get_chats_by_user_id(1)

    assert chats == [chat_1, chat_2]

