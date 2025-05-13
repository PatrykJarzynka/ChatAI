from fastapi import HTTPException, status
import pytest
from unittest.mock import Mock
from app.services.auth.google_service import GoogleService
from app.services.auth.microsoft_service import MicrosoftService
from services.auth.jwt_service import JWTService
from utilities.token_validator import TokenValidator
from main import app

mock_decode = {'sub': 'testToken'}

@pytest.fixture
def jwt_service():
    mock = Mock()
    mock.decode_local_token.return_value = mock_decode
    app.dependency_overrides[JWTService] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def google_fixture():
    mock = Mock()
    mock.decode_token.return_value = mock_decode
    app.dependency_overrides[GoogleService] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def microsoft_service():
    mock = Mock()
    mock.decode_token.return_value = mock_decode
    app.dependency_overrides[MicrosoftService] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def token_validator(jwt_service: JWTService, google_fixture: GoogleService, microsoft_service: MicrosoftService) -> TokenValidator:
    return TokenValidator(jwt_service=jwt_service, google_service=google_fixture, microsoft_service=microsoft_service)

@pytest.mark.parametrize('issuer',['accounts.google.com','login.microsoftonline.com','local', 'customIssuer'])
def test_validate_token(issuer: str, token_validator: TokenValidator, google_fixture, microsoft_service, jwt_service):
    token = 'mockToken'
    authorization = f'Bearer {token}'

    jwt_service.get_token_issuer.return_value = issuer

    if issuer == 'accounts.google.com':
        result = token_validator.validate_token(authorization)

        google_fixture.decode_token.assert_called_once_with(token)
        assert result == mock_decode
    elif issuer == 'login.microsoftonline.com':
        result = token_validator.validate_token(authorization)

        microsoft_service.decode_token.assert_called_once_with(token)
        assert result == mock_decode
    elif issuer == 'local':
        result = token_validator.validate_token(authorization)

        jwt_service.decode_local_token.assert_called_once_with(token)
        assert result == mock_decode
    elif issuer == 'customIssuer':
        with pytest.raises(HTTPException) as http_exec:
            result = token_validator.validate_token(authorization)

        assert http_exec.value.detail == 'Unknown provider'
        assert http_exec.value.status_code == status.HTTP_400_BAD_REQUEST

    jwt_service.get_token_issuer.assert_called_once_with(token)

def test_authorization_invalid_token_type(token_validator: TokenValidator):
    with pytest.raises(HTTPException) as http_exec:
        token_validator.validate_token('mockToken')

    assert http_exec.value.detail == 'Invalid token type'
    assert http_exec.value.status_code == status.HTTP_401_UNAUTHORIZED


    



