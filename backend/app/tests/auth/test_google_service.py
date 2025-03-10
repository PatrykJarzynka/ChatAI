import pytest
from services.auth.google_service import GoogleService
from unittest.mock import patch
from google.oauth2 import id_token
import google.auth.transport.requests
from unittest.mock import MagicMock


@pytest.fixture
def google_service():
    return GoogleService()

def test_verify_and_decode_token_successfully(google_service: GoogleService):
    mockGoogleKeys = ['mock_google_key']
    mockClientId = 'CLIENT_ID'

    with patch('os.getenv', return_value = mockClientId):
        with patch.object(id_token, 'verify_oauth2_token', return_value={"email": 'test@test.com', "name": "Test User"}) as mock_verify:
            with patch.object(google.auth.transport.requests, 'Request', return_value = mockGoogleKeys):
                mock_token = "mock_token"
            
                result = google_service.verify_and_decode_token(mock_token)
                mock_verify.assert_called_once_with(mock_token, mockGoogleKeys, audience = mockClientId)
                assert result == {"email": "test@test.com", "name": "Test User"}

def test_verify_and_decode_token_failed(google_service: GoogleService):
    mockClientId = 'CLIENT_ID'

    with patch('os.getenv', return_value = mockClientId):
        with patch.object(id_token, 'verify_oauth2_token', side_effect = ValueError('Error')) as mock_verify:
            mock_token = "mock_token"
            
            with pytest.raises(ValueError) as verify_error:
                google_service.verify_and_decode_token(mock_token)

            assert str(verify_error.value) == "Not authenicated!"

def test_fetch_tokens(google_service: GoogleService, monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID',"mockedId")
    monkeypatch.setenv('GOOGLE_SECRET',"mockedSecret")
    mockedCode = 'mockedCode'

    mock_response = MagicMock()
    mock_response.json.return_value={'id_token': 'aaa', 'refresh_token': 'bbb'}

    expected_data = {
        "code": mockedCode,
        "client_id": 'mockedId',
        "client_secret": 'mockedSecret',
        "redirect_uri": 'postmessage',
        "grant_type": 'authorization_code'
    }

    with patch('requests.post', return_value = mock_response) as mock_post:
        google_service.fetch_tokens(mockedCode)

        mock_post.assert_called_with('https://oauth2.googleapis.com/token', data=expected_data)

def test_refresh_token(google_service: GoogleService, monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID',"mockedId")
    monkeypatch.setenv('GOOGLE_SECRET',"mockedSecret")
    mockedRefreshToken = 'xyz'

    mock_response = MagicMock()
    mock_response.json.return_value={'id_token': 'aaa', 'refresh_token': 'bbb'}

    expected_data = {
        "client_id": "mockedId",
        "client_secret": "mockedSecret",
        "refresh_token": mockedRefreshToken,
        "grant_type": 'refresh_token'
        }
    
    with patch('requests.post', return_value = mock_response) as mock_post:
        google_service.refresh_id_token(mockedRefreshToken)

        mock_post.assert_called_with('https://oauth2.googleapis.com/token', data=expected_data)


