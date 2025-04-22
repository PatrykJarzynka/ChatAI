import pytest
import jwt
from fastapi import status, HTTPException
from utilities.token_exception_manager import TokenExceptionManager


@pytest.fixture
def get_token_exception_manager() -> TokenExceptionManager:
    return TokenExceptionManager()

@pytest.mark.parametrize('exception, expected_status, expected_message',
                            [
                                (jwt.InvalidSignatureError, status.HTTP_401_UNAUTHORIZED, 'Invalid signature.'),
                                (jwt.InvalidIssuerError, status.HTTP_401_UNAUTHORIZED, 'Invalid issuer'),
                                (jwt.ExpiredSignatureError, status.HTTP_401_UNAUTHORIZED, 'Token expired'),
                                (ValueError, status.HTTP_400_BAD_REQUEST, 'Value error'),
                                (Exception, status.HTTP_500_INTERNAL_SERVER_ERROR, 'Unexpected error')
                            ]
                        )
def test_exception_handler(get_token_exception_manager: TokenExceptionManager, exception, expected_status, expected_message):

    def raise_exception():
        if exception == ValueError:
            raise ValueError("Value error")
        elif exception == Exception:
            raise Exception("Unexpected error")
        else:
            raise exception()
        
    with pytest.raises(HTTPException) as expected_exception:
        get_token_exception_manager.handle_token_exceptions(raise_exception)()
        
    assert expected_exception.value.detail == expected_message, f'Exception message should be equal {expected_message}'
    assert expected_exception.value.status_code == expected_status, f'Status code should be {expected_status}'