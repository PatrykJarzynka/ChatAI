import pytest
from unittest.mock import patch, Mock
from clients.serper_api_search_engine import SerperApiSearchEngine
from config import get_settings

@pytest.fixture
def serper_api():
    return SerperApiSearchEngine(api_key=get_settings().SERPER_API_KEY)

def test_search_web(serper_api: SerperApiSearchEngine):
    mocked_response = Mock()
    mocked_response.json.return_value = 'Test value'

    mocked_query = 'Current date'

    expected_url = "https://google.serper.dev/search"

    expected_payload = {
            "q": mocked_query,
            "gl": "pl",
    }

    expected_headers = {"X-API-KEY": get_settings().SERPER_API_KEY}

    with patch('requests.post', return_value=mocked_response) as mock_post:
            response = serper_api.search_web(mocked_query)

    mock_post.assert_called_once_with(url=expected_url, json = expected_payload, headers=expected_headers)
    assert response == 'Test value'

