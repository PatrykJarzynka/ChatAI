import pytest
from config import get_settings
from services.auth.microsoft_service import MicrosoftService
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_google_setup(monkeypatch):
    monkeypatch.setenv('MICROSOFT_CLIENT_ID',"mockedId")
    monkeypatch.setenv('MICROSOFT_SECRET',"mockedSecret")
    monkeypatch.setenv('REDIRECT_URL', 'redirect')
    get_settings.cache_clear()

@pytest.fixture
def microsoft_service():
    return MicrosoftService()

def test_decode_token(microsoft_service: MicrosoftService):
    mock_token='mockToken'
    mock_rsa_key={"issuer": "mockRsaKey"}
    mock_public_key="mockPublicKey"
    expected_decoded_token = {"sub": "test_user", "aud": "client_id_123"}

    with patch.object(microsoft_service.public_keys_provider,'get_rsa_key', return_value=mock_rsa_key) as mock_get_rsa, \
        patch('jwt.algorithms.RSAAlgorithm.from_jwk', return_value=mock_public_key) as mock_get_public_key, \
        patch("jwt.decode", return_value=expected_decoded_token) as mock_jwt_decode:

        decoded = microsoft_service.decode_token(mock_token)

        assert decoded == expected_decoded_token
        mock_get_rsa.assert_called_once_with(mock_token)
        mock_get_public_key.assert_called_once_with(mock_rsa_key)
        mock_jwt_decode.assert_called_once_with(
            mock_token,
            key=mock_public_key,
            algorithms=["RS256"],
            audience='mockedId',
            issuer=mock_rsa_key["issuer"],
        )

def test_fetch_tokens(microsoft_service: MicrosoftService):
    mockedCode = 'mockedCode'

    mocked_data = {
        "code": mockedCode,
        "client_id": 'mockedId',
        "client_secret": 'mockedSecret',
        "scope": 'openid profile email',
        "redirect_uri": 'redirect',
        "grant_type": 'authorization_code'
    }

    with patch('requests.post') as mock_post:
        microsoft_service.fetch_tokens(mockedCode)

        mock_post.assert_called_with('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=mocked_data)

def test_refresh_token(microsoft_service: MicrosoftService):
    mockedRefreshToken = 'xyz'

    mocked_data = {
        "client_id": "mockedId",
        "client_secret": "mockedSecret",
        "refresh_token": mockedRefreshToken,
        "grant_type": 'refresh_token'
        }
    
    with patch('requests.post') as mock_post:
        microsoft_service.refresh_tokens(mockedRefreshToken)

        mock_post.assert_called_with('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=mocked_data)




