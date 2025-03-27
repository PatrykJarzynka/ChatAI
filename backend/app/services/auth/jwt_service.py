import os
from datetime import timedelta, datetime, timezone

import jwt
from dotenv import load_dotenv

from app_types.token import Token

env_file = ".env.production" if os.getenv("DOCKER_ENV") == "production" else ".env.development"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(base_dir, env_file)

load_dotenv(env_path)

class JWTService:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def decode_token(self, jwt_token:str) -> dict:
        return jwt.decode(jwt_token, options={"verify_signature": False})

    def create_access_token(self, data: dict,
                            expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(tz=timezone.utc) + expires_delta
        else:
            expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire, "iss": 'local'})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")
        

    def decode_local_token(self, token: str):
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        return payload
    