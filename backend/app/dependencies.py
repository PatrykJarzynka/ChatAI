from typing import Annotated

from fastapi import Depends, HTTPException

from services.auth.hash_service import HashService
from services.auth.jwt_service import JWTService
from services.auth.google_service import GoogleService
from starlette.requests import Request
from app_types.tenant import Tenant

def get_jwt_service():
    return JWTService()

def get_hash_service():
    return HashService()

def get_google_service():
    return GoogleService()


google_service_dependency = Annotated[GoogleService, Depends(get_google_service)]
hash_service_dependency = Annotated[HashService, Depends(get_hash_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]


def get_token_from_header(request: Request) -> str:
    token_prefix = "Bearer"
    authorization: str = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    header, _, token = authorization.partition(' ')

    if header != token_prefix:
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    return token


def verify_google_token(token: str, google_service: GoogleService):
    return google_service.verify_and_decode_token(token)

def verify_local_token(token: str, jwt_service: JWTService):
    return jwt_service.decode_access_token(token)

def verify_token(token: str | None = Depends(get_token_from_header),
                 tenant: Tenant | None = None, 
                 google_service: GoogleService = Depends(get_google_service), 
                 jwt_service: JWTService = Depends(get_jwt_service)):
                 
    try:
        return verify_google_token(token, google_service)
    except ValueError as exception:
        pass

    try:
        return verify_local_token(token, jwt_service)
    except HTTPException as exception:
        pass
    
    raise HTTPException(
        status_code=401,
        detail='Not authenticated!'
    )

verify_token_dependency = Annotated[dict, Depends(verify_token)]
