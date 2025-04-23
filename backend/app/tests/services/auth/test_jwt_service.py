from datetime import timedelta, datetime, timezone

import pytest
from fastapi import HTTPException

from models.token import Token
from services.auth.jwt_service import JWTService

import jwt


@pytest.fixture()
def jwt_service():
    return JWTService()


def test_create_access_token(jwt_service: JWTService):
    data = {"sub": "test@test.pl"}

    token = jwt_service.create_access_token(data)

    assert isinstance(token, Token), 'Token needs to be instance of class Token'
    assert token.access_token is not None, 'Token cannot be empty'
    assert token.token_type == "bearer", 'Token type should be bearer'


def test_create_access_token_with_expiry(jwt_service: JWTService):
    data = {"sub": "user@example.com"}
    expiry_time = timedelta(minutes=10)

    token = jwt_service.create_access_token(data=data, expires_delta=expiry_time)

    decoded_payload = jwt_service.decode_local_token(token.access_token)

    expire_time = decoded_payload["exp"]
    assert datetime.fromtimestamp(expire_time, tz=timezone.utc) > datetime.now(timezone.utc), "Token shouldn't be expired"


def test_decode_local_token_valid(jwt_service: JWTService):
    data = {"sub": "test@test.pl"}
    token = jwt_service.create_access_token(data)

    decoded_payload = jwt_service.decode_local_token(token.access_token)

    assert decoded_payload["sub"] == "test@test.pl", "Token content should be equal to test@test.pl"


def test_decode_local_token_invalid(jwt_service: JWTService):
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"

    with pytest.raises(jwt.InvalidSignatureError):
        jwt_service.decode_local_token(invalid_token)
        

def test_decode_local_token_expired(jwt_service: JWTService):
    expired_token = jwt_service.create_access_token(data={"sub": "test_user"}, expires_delta=timedelta(minutes=-10))

    with pytest.raises(jwt.ExpiredSignatureError):
        jwt_service.decode_local_token(expired_token.access_token)
