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

def test_get_jwks_by_config(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    mock_url = 'https://login.microsoftonline.com'
    mock_keys = [{"mock_key": "mock_value"}, {"mock_key2": "mock_value2"}]

    mock_openid_config = {"jwks_uri": mock_url}
    mock_json = {"keys": mock_keys}

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_json
        mock_get.return_value = mock_response

        response = microsoft_public_keys_provider.get_jwks_by_config(mock_openid_config)
    
    mock_get.assert_called_once_with(mock_url)
    assert response == mock_keys, 'Wrong response'
