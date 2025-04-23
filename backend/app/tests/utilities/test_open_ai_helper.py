import pytest
from unittest.mock import patch, Mock
from utilities.open_ai_helper import OpenAIHelper

mock_llm = Mock()

@pytest.fixture
def open_ai_helper():
    return OpenAIHelper()

def test_get_state_assigned_to_city(open_ai_helper: OpenAIHelper):
    states = ['Silesia', 'GreaterPoland', 'Lubelskie']
    city = 'Gliwice'
    mock_response_text = 'mockResponse'
    mock_response = Mock()
    mock_response.text = mock_response_text

    mock_llm.complete.return_value = mock_response
    open_ai_helper.support_llm = mock_llm

    prompt = f"""Pick only one state from the list: {','.join(states)}, that is in your opinion assigned to the given city: {city}. Answer with just the name of the state, one word."""

    result = open_ai_helper.get_state_assigned_to_city(city, states)

    mock_llm.complete.assert_called_with(prompt)
    assert result == mock_response_text