import pytest
from services.auth.google_service import GoogleService
from unittest.mock import patch
from google.oauth2 import id_token
from unittest.mock import MagicMock
from config import get_settings
from starlette import requests


@pytest.fixture(autouse=True)
def mock_google_setup(monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID',"mockedId")
    monkeypatch.setenv('GOOGLE_SECRET',"mockedSecret")
    get_settings.cache_clear()

@pytest.fixture
def google_service():
    return GoogleService()

def test_verify_token(google_service: GoogleService):
    mock_token = 'MockToken'
    expected_response = {"email": 'test@test.com', "name": "Test User"}

    with patch.object(id_token,'verify_oauth2_token', return_value = expected_response) as mock_verify:
    
        assert google_service.verify_and_decode_token(mock_token) == expected_response
        args, kwargs  = mock_verify.call_args

        mock_verify.assert_called_once
        assert args[0] == mock_token
        assert kwargs["audience"] == 'mockedId'


def test_fetch_tokens(google_service: GoogleService, monkeypatch):
    mockedCode = 'mockedCode'
    monkeypatch.setenv('REDIRECT_URL', 'redirect')

    mocked_data = {
        "code": mockedCode,
        "client_id": 'mockedId',
        "client_secret": 'mockedSecret',
        "redirect_uri": 'redirect',
        "grant_type": 'authorization_code'
    }

    with patch('requests.post') as mock_post:
        google_service.fetch_tokens(mockedCode)

        mock_post.assert_called_with('https://oauth2.googleapis.com/token', data=mocked_data)

def test_refresh_token(google_service: GoogleService):
    mockedRefreshToken = 'xyz'

    mocked_data = {
        "client_id": "mockedId",
        "client_secret": "mockedSecret",
        "refresh_token": mockedRefreshToken,
        "grant_type": 'refresh_token'
        }
    
    with patch('requests.post') as mock_post:
        google_service.refresh_id_token(mockedRefreshToken)

        mock_post.assert_called_with('https://oauth2.googleapis.com/token', data=mocked_data)


