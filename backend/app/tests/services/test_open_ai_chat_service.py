from unittest.mock import patch, Mock

import pytest
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage

from services.open_ai_chat_service import OpenAIChatService

from llama_index.core.tools import FunctionTool
from services.memory_buffer_service import MemoryBufferService


@pytest.fixture
def open_ai_chat_service():
    test_tool_1 = FunctionTool.from_defaults(lambda: 'mock_tool_1', description='Tool that always returns mock_tool_1 string')
    test_tool_2 = FunctionTool.from_defaults(lambda: 'mock_tool_2', description='Tool that always returns mock_tool_2 string')
    bot_description = 'You are intelligent assistant whose responsibility is to select proper tool to use.'
    chat_messages = [
                ChatMessage(content=f"Hello.", role='user'),
                ChatMessage(content=f"Hello there.", role='assistant')
            ]
    memory = MemoryBufferService(chat_messages) 

    return OpenAIChatService(tools = [test_tool_1, test_tool_2], memory = memory.get_memory(), bot_description=bot_description)

def test_chat(open_ai_chat_service: OpenAIChatService):
    query = 'Hello'
    mock_response = Mock()
    mock_response.response = 'How can I help you?'

    with patch.object(open_ai_chat_service.chat_agent, 'chat', return_value=mock_response) as mock_chat:
        response = open_ai_chat_service.chat(query)

    mock_chat.assert_called_once_with(query)
    assert response == 'How can I help you?'
