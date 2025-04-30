import pytest
from unittest.mock import Mock
from main import app
from utilities.token_extractor import TokenExtractor
from services.auth.google_service import GoogleService
from services.auth.microsoft_service import MicrosoftService
from services.auth.jwt_service import JWTService
from containers import decode_token
from fastapi import Request, HTTPException

mock_token = 'mockToken'

@pytest.fixture
def request_mock():
    mock = Mock(spec=Request)
    return mock

@pytest.fixture
def override_jwt_service():
    mock = Mock()
    mock.decode_local_token.return_value = mock_token
    app.dependency_overrides[JWTService] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def override_google_service():
    mock = Mock()
    mock.decode_token.return_value = mock_token
    app.dependency_overrides[GoogleService] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def override_microsoft_service():
    mock = Mock()
    mock.decode_token.return_value = mock_token
    app.dependency_overrides[MicrosoftService] = mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def override_token_extractor():
    mock = Mock()
    mock.get_token_from_header.return_value = mock_token
    app.dependency_overrides[TokenExtractor] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.mark.parametrize('issuer',['accounts.google.com','login.microsoftonline.com','local'])
def test_decode_token(issuer:str, request_mock, override_jwt_service, override_google_service, override_microsoft_service, override_token_extractor):
    override_jwt_service.get_token_issuer.return_value=issuer

    result = decode_token(
        request_mock,
        token_extractor=override_token_extractor,
        microsoft_service=override_microsoft_service,
        google_service=override_google_service,
        jwt_service=override_jwt_service,
    )
    
    override_token_extractor.get_token_from_header.assert_called_once_with(request_mock)
    override_jwt_service.get_token_issuer.assert_called_once_with(mock_token)

    if (issuer == 'accounts.google.com'): 
        assert result == mock_token
        override_google_service.decode_token.assert_called_once_with(mock_token)
        override_microsoft_service.decode_token.assert_not_called()
        override_jwt_service.decode_local_token.assert_not_called()
    elif (issuer == 'login.microsoftonline.com'): 
        assert result == mock_token
        override_microsoft_service.decode_token.assert_called_once_with(mock_token)
        override_google_service.decode_token.assert_not_called()
        override_jwt_service.decode_local_token.assert_not_called()
    elif (issuer == 'local'):
        assert result == mock_token
        override_jwt_service.decode_local_token.assert_called_once_with(mock_token)
        override_microsoft_service.decode_token.assert_not_called()
        override_google_service.decode_token.assert_not_called()

def test_decode_token_wrong_issuer(request_mock, override_jwt_service, override_google_service, override_microsoft_service, override_token_extractor):
        override_jwt_service.get_token_issuer.return_value='customIssuer'

        with pytest.raises(HTTPException) as exception:
            decode_token(
                request_mock,
                token_extractor=override_token_extractor,
                microsoft_service=override_microsoft_service,
                google_service=override_google_service,
                jwt_service=override_jwt_service,
            )

        assert exception.value.detail == 'Unknown provider'
        assert exception.value.status_code == 400
    
    
    






