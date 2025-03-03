import pytest
from services.auth.google_service import GoogleService
from unittest.mock import patch
from google.oauth2 import id_token
import google.auth.transport.requests
import time


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

def test_validate_iss_successfully(google_service: GoogleService):
    mocked_id_info = {"iss": 'https://accounts.google.com'}

    result = google_service.validate_iss(mocked_id_info)
    assert result == True

def test_validate_iss_failed(google_service: GoogleService):
    mocked_id_info = {"iss": 'mock_iss'}
    
    with pytest.raises(ValueError) as validate_iss_error:
        google_service.validate_iss(mocked_id_info)
    
    assert str(validate_iss_error.value) == "Invalid issuer token!"

def test_validate_exp_time_successfully(google_service: GoogleService):
    current_time = time.time() + 86400
    mocked_id_info = {"exp": current_time}

    result = google_service.validate_exp_time(mocked_id_info)
    assert result == True

def test_validate_exp_time_failed(google_service: GoogleService):
    current_time = time.time() - 86400
    mocked_id_info = {"exp": current_time}

    with pytest.raises(ValueError) as validate_exp_time_error:
        google_service.validate_exp_time(mocked_id_info)

    assert str(validate_exp_time_error.value) == "Google token expired!"
                