import pytest
from utilities.microsoft_public_keys_provider import MicrosoftPublicKeysProvider
from unittest.mock import patch, Mock
from config import get_settings
from typing import List, Dict
from jwt.types import JWKDict

@pytest.fixture
def microsoft_public_keys_provider():
    return MicrosoftPublicKeysProvider()

def run_get_rsa_key_test(
    provider: MicrosoftPublicKeysProvider,
    mock_jwks: List[Dict[str, str]],
    mock_rsa_key: JWKDict | None,
    expected_exception = None,
):
    mock_openid_config = {"jwks_uri": 'https://login.microsoftonline.com'}
    mock_token = 'mockToken'

    with patch.object(provider, 'get_openid_config', return_value=mock_openid_config) as mock_get_openid_config, \
         patch.object(provider, 'get_jwks_by_config', return_value=mock_jwks) as mock_get_jwks, \
         patch.object(provider, 'get_rsa_key_from_jwks', return_value=mock_rsa_key) as mock_get_rsa_key:

        if expected_exception:
            with pytest.raises(expected_exception) as exc_info:
                provider.get_rsa_key(mock_token)
            return exc_info
        else:
            result = provider.get_rsa_key(mock_token)

    mock_get_openid_config.assert_called_once()
    mock_get_jwks.assert_called_once_with(mock_openid_config)
    mock_get_rsa_key.assert_called_once_with(mock_token, mock_jwks)

    return result

def run_test_get_rsa_key_from_jwks(provider: MicrosoftPublicKeysProvider,mock_jwks: List[Dict[str,str]]) -> Dict[str,str] | None:
    mock_token = 'mockToken'
    mock_header_response = {"kid":'mock_kid'}

    with patch('jwt.get_unverified_header', return_value=mock_header_response) as mock_get_unverified_header:
        result = provider.get_rsa_key_from_jwks(mock_token,mock_jwks)
    
    mock_get_unverified_header.assert_called_once_with(mock_token)
    
    return result


def test_get_openid_config(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    expected_url = get_settings().MICROSOFT_OPENID_CONFIG_URL
    mock_json = {"issuer": "https://login.microsoftonline.com/common"}

    mock_response = Mock()
    mock_response.json.return_value = mock_json

    with patch('requests.get', return_value=mock_response) as mock_get:
        response = microsoft_public_keys_provider.get_openid_config()

    mock_get.assert_called_once_with(expected_url)
    assert response == mock_json, 'Wrong response'

def test_get_jwks_by_config(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    mock_url = 'https://login.microsoftonline.com'
    mock_keys = [{"mock_key": "mock_value"}, {"mock_key2": "mock_value2"}]

    mock_openid_config = {"jwks_uri": mock_url}
    mock_json = {"keys": mock_keys}

    mock_response = Mock()
    mock_response.json.return_value = mock_json

    with patch('requests.get', return_value=mock_response) as mock_get:
        response = microsoft_public_keys_provider.get_jwks_by_config(mock_openid_config)
    
    mock_get.assert_called_once_with(mock_url)
    assert response == mock_keys, 'Wrong response'

def test_get_rsa_key_from_jwks(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    mock_header_response = {"kid":'mock_kid'}
    mock_jwks = [mock_header_response]

    result = run_test_get_rsa_key_from_jwks(microsoft_public_keys_provider, mock_jwks)
    assert result == mock_header_response, "Key not found"

def test_key_in_jwks_not_found(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    result = run_test_get_rsa_key_from_jwks(microsoft_public_keys_provider, [{"kid":'test_kid'}])
    assert result == None

def test_get_rsa_key(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    mock_jwks = [{"kid":'mock_kid'}]
    mock_rsa_key = {"kid":'mock_kid'}

    result = run_get_rsa_key_test(
        provider=microsoft_public_keys_provider,
        mock_jwks=mock_jwks,
        mock_rsa_key=mock_rsa_key,
    )

    assert result == mock_rsa_key

def test_invalid_public_key(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):
    mock_jwks = [{"kid":'test_kid'}]
    mock_rsa_key = None

    exc_info = run_get_rsa_key_test(
        provider=microsoft_public_keys_provider,
        mock_jwks=mock_jwks,
        mock_rsa_key=mock_rsa_key,
        expected_exception=ValueError,
    )

    assert str(exc_info.value) == "Invalid public key!"

