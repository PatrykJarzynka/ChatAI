from unittest.mock import patch, MagicMock
from utilities.open_ai_helper import OpenAIHelper

def test_get_state_assigned_to_city():
    states = ['Silesia', 'GreaterPoland', 'Lubelskie']
    city = 'Gliwice'

    mock_llm_response = MagicMock()
    mock_llm_response.text = 'mockedResponse'

    with patch('utilities.open_ai_helper.OpenAI') as MockOpenAI:
        mock_llm = MockOpenAI.return_value
        mock_llm.complete.return_value = mock_llm_response

        helper = OpenAIHelper()
        result = helper.get_state_assigned_to_city(city, states)

        prompt = f"""Pick only one state from the list: {','.join(states)}, that is in your opinion assigned to the given city: {city}. Answer with just the name of the state, one word."""
        
        mock_llm.complete.assert_called_once_with(prompt)
        assert result == 'mockedResponse'