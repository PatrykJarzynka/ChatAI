from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError

from app.app_types.token import Token


class JWTService:
    SECRET_KEY = '289f3f1a609ae21ab96fa79538363c33c9f7e2a3c959634eecefac2d31aab296'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict,
                            expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return Token(access_token=encoded_jwt, token_type="bearer")

    def decode_access_token(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except InvalidTokenError:
            raise credentials_exception
