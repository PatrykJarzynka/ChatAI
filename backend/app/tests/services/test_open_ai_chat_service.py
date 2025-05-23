from unittest.mock import patch, Mock

import pytest
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer

from services.open_ai_chat_service import OpenAIChatService

from llama_index.core.tools import FunctionTool

from fastapi import HTTPException


@pytest.fixture
def open_ai_chat_service():
    test_tool_1 = FunctionTool.from_defaults(lambda: 'mock_tool_1', description='Tool that always returns mock_tool_1 string')
    test_tool_2 = FunctionTool.from_defaults(lambda: 'mock_tool_2', description='Tool that always returns mock_tool_2 string')
    bot_description = 'You are intelligent assistant whose responsibility is to select proper tool to use.'
    chat_messages = [
                ChatMessage(content=f"Hello.", role='user'),
                ChatMessage(content=f"Hello there.", role='assistant')
            ]
    memory = ChatMemoryBuffer.from_defaults(chat_history=chat_messages)

    return OpenAIChatService(tools = [test_tool_1, test_tool_2], memory = memory, bot_description=bot_description)

def test_chat(open_ai_chat_service: OpenAIChatService):
    query = 'Hello'
    mock_response = Mock()
    mock_response.response = 'How can I help you?'

    with patch.object(open_ai_chat_service.chat_agent, 'chat', return_value=mock_response) as mock_chat:
        response = open_ai_chat_service.chat(query)

    mock_chat.assert_called_once_with(query)
    assert response == 'How can I help you?'

def test_chat_exception(open_ai_chat_service: OpenAIChatService):
    query = 'Hello'
    mock_exception_text = 'Test exception'

    with patch.object(open_ai_chat_service.chat_agent, 'chat', side_effect=Exception(mock_exception_text)) as mock_chat:
        with pytest.raises(HTTPException) as exception:
            open_ai_chat_service.chat(query)
        
    assert exception.value.detail == f"Failed to fetch bot response: {mock_exception_text}"
    assert exception.value.status_code == 500