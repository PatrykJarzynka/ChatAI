import pytest
from utilities.microsoft_public_keys_provider import MicrosoftPublicKeysProvider
from unittest.mock import patch, Mock
from config import get_settings

@pytest.fixture
def microsoft_public_keys_provider():
    return MicrosoftPublicKeysProvider()


def test_get_openid_config(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    expected_url = get_settings().MICROSOFT_OPENID_CONFIG_URL
    mock_json = {"issuer": "https://login.microsoftonline.com/common"}

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_json
        mock_get.return_value = mock_response

        response = microsoft_public_keys_provider.get_openid_config()

    mock_get.assert_called_once_with(expected_url)
    assert response == mock_json, 'Wrong response'
