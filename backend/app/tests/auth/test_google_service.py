import pytest
from services.auth.google_service import GoogleService
from unittest.mock import patch
from config import get_settings


@pytest.fixture(autouse=True)
def mock_google_setup(monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID',"mockedId")
    monkeypatch.setenv('GOOGLE_SECRET',"mockedSecret")
    monkeypatch.setenv('REDIRECT_URL', 'redirect')
    get_settings.cache_clear()

@pytest.fixture
def google_service():
    return GoogleService()

def test_fetch_tokens(google_service: GoogleService):
    mockedCode = 'mockedCode'

    mocked_data = {
        "code": mockedCode,
        "client_id": 'mockedId',
        "client_secret": 'mockedSecret',
        "redirect_uri": 'redirect',
        "grant_type": 'authorization_code'
    }

    with patch('requests.post') as mock_post:
        google_service.fetch_tokens(mockedCode)

        mock_post.assert_called_with('https://oauth2.googleapis.com/token', data=mocked_data), "Api call's parameters are not as expected"

def test_refresh_token(google_service: GoogleService):
    mockedRefreshToken = 'xyz'

    mocked_data = {
        "client_id": "mockedId",
        "client_secret": "mockedSecret",
        "refresh_token": mockedRefreshToken,
        "grant_type": 'refresh_token'
        }
    
    with patch('requests.post') as mock_post:
        google_service.refresh_tokens(mockedRefreshToken)

        mock_post.assert_called_with('https://oauth2.googleapis.com/token', data=mocked_data), "Api call's parameters are not as expected"


