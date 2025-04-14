from datetime import timedelta, datetime, timezone

import pytest
from fastapi import HTTPException

from models.token import Token
from services.auth.jwt_service import JWTService


@pytest.fixture()
def jwt_service():
    return JWTService()


def test_create_access_token(jwt_service):
    data = {"sub": "test@test.pl"}

    token = jwt_service.create_access_token(data)

    assert isinstance(token, Token)
    assert token.access_token is not None
    assert token.token_type == "bearer"


def test_create_access_token_with_expiry(jwt_service):
    data = {"sub": "user@example.com"}
    expiry_time = timedelta(minutes=10)

    token = jwt_service.create_access_token(data=data, expires_delta=expiry_time)

    decoded_payload = jwt_service.decode_local_token(token.access_token)

    expire_time = decoded_payload["exp"]
    assert datetime.fromtimestamp(expire_time, tz=timezone.utc) > datetime.now(timezone.utc)
    assert datetime.fromtimestamp(expire_time, tz=timezone.utc) < datetime.now(timezone.utc) + expiry_time


def test_decode_local_token_valid(jwt_service):
    data = {"sub": "test@test.pl"}
    token = jwt_service.create_access_token(data)

    decoded_payload = jwt_service.decode_local_token(token.access_token)

    assert decoded_payload["sub"] == "test@test.pl"


def test_decode_local_token_invalid(jwt_service):
    invalid_token = "invalid.token.string"

    with pytest.raises(HTTPException) as exc_info:
        jwt_service.decode_local_token(invalid_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Could not validate credentials'

def test_decode_local_token_expired(jwt_service: JWTService):
    expired_token = jwt_service.create_access_token(data={"sub": "test_user"}, expires_delta=timedelta(minutes=-10))

    with pytest.raises(HTTPException) as exc_info:
        jwt_service.decode_local_token(expired_token)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == 'Token expired'
