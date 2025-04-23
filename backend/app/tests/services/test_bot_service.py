from unittest.mock import patch, Mock

import pytest
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage

from db_models.chat_item_model import ChatItem
from services.open_ai_chat_service import OpenAIChatService


@pytest.fixture
def bot_service():
    return OpenAIChatService()


def test_prepare_chat_memory(bot_service: OpenAIChatService):
    chat_items = [ChatItem(user_id='testUser', user_message='Hello there', chat_id=1, bot_message='Hello'),
                  ChatItem(user_id='testUser', user_message='How are you?', chat_id=1, bot_message='Good.')]
    expected_data = [
        ChatMessage(content=chat_items[0].user_message, role='user'),
        ChatMessage(content=chat_items[0].bot_message, role='assistant'),
        ChatMessage(content=chat_items[1].user_message, role='user'),
        ChatMessage(content=chat_items[1].bot_message, role='assistant')]

    chat_memory = bot_service.prepare_chat_memory(chat_items)

    assert chat_memory == expected_data


@patch('llama_index.core.memory.ChatMemoryBuffer.from_defaults', return_value=Mock())
@patch('llama_index.core.chat_engine.SimpleChatEngine.from_defaults', return_value=Mock())
def test_fetch_bot_response(mock_chat_engine, mock_memory, bot_service: BotService):
    mock_memory.return_value = Mock()

    mock_engine_instance = Mock()
    mock_engine_instance.chat.return_value.response = "Mock message."

    mock_chat_engine.return_value = mock_engine_instance

    response = bot_service.fetch_bot_response('Hello!', [])

    assert response == "Mock message."

    mock_memory.assert_called_once_with(chat_history=[])
    mock_chat_engine.assert_called_once_with(memory=mock_memory.return_value, llm=Settings.llm)
    mock_engine_instance.chat.assert_called_once_with("Hello!")
