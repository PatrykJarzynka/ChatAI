import pytest
from services.auth.auth_service import AuthService
from fastapi import HTTPException, status
import jwt

@pytest.fixture
def get_auth_service():
    return AuthService()

@pytest.fixture
def header_request():
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": 'Bearer XYZ'}

    return MockRequest()

@pytest.fixture
def no_header_request():
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": ''}

    return MockRequest()

@pytest.fixture
def wrong_type_request():
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": 'XYZ'}

    return MockRequest()

def test_get_token_from_header(get_auth_service: AuthService, header_request):
    assert get_auth_service.get_token_from_header(header_request) == 'XYZ', 'Tokens are not the same'

def test_lack_of_token(get_auth_service: AuthService, no_header_request):
    with pytest.raises(HTTPException) as no_token_exception:
        get_auth_service.get_token_from_header(no_header_request)
        assert no_token_exception.value.status_code == status.HTTP_401_UNAUTHORIZED, 'Status code should be 401'
        assert no_token_exception.value.detail == 'Authorization header missing', 'Exception message should be equal "Authorization header missing"'

def test_wrong_token_type(get_auth_service: AuthService, wrong_type_request):
    with pytest.raises(HTTPException) as no_token_exception:
        get_auth_service.get_token_from_header(wrong_type_request)
        assert no_token_exception.value.status_code == status.HTTP_401_UNAUTHORIZED,'Status code should be 401'
        assert no_token_exception.value.detail == 'Invalid token type', 'Exception message should be equal "Invalid token type"'



@pytest.mark.parametrize('exception, expected_status, expected_message',
                            [
                                (jwt.InvalidSignatureError, status.HTTP_401_UNAUTHORIZED, 'Invalid signature.'),
                                (jwt.InvalidIssuerError, status.HTTP_401_UNAUTHORIZED, 'Invalid issuer'),
                                (jwt.ExpiredSignatureError, status.HTTP_401_UNAUTHORIZED, 'Token expired'),
                                (ValueError, status.HTTP_400_BAD_REQUEST, 'Value error'),
                                (Exception, status.HTTP_500_INTERNAL_SERVER_ERROR, 'Unexpected error')
                            ]
                        )
def test_exception_handler(get_auth_service: AuthService, exception, expected_status, expected_message):

    def raise_exception():
        if exception == ValueError:
            raise ValueError("Value error")
        elif exception == Exception:
            raise Exception("Unexpected error")
        else:
            raise exception()
        
    with pytest.raises(HTTPException) as expected_exception:
        get_auth_service.handle_token_exceptions(raise_exception)()
        
    assert expected_exception.value.detail == expected_message, f'Exception message should be equal {expected_message}'
    assert expected_exception.value.status_code == expected_status, f'Status code should be {expected_status}'