import os
import requests
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session

from app_types.token import Token
from app_types.auth_code_request import AuthCodeRequest
from app_types.google_refresh_token_request import GoogleRefreshTokenRequest
from app_types.user_create_dto import UserCreateDTO
from app_types.tenant import Tenant
from app_types.google_tokens import GoogleTokens
from database import get_session
from dependencies import hash_service_dependency, jwt_service_dependency, verify_token_dependency, google_service_dependency, microsoft_service_dependency
from services.user_service import UserService


router = APIRouter()

session_dependency = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
    return UserService(session, hash_service)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]

@router.post('/auth/login')
async def login_for_access_token(
        user_service: user_service_dependency,
        jwt_service: jwt_service_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = user_service.authenticate_local_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return jwt_service.create_access_token({"sub": str(user.id)})


@router.post('/auth/register')
def register(user: UserCreateDTO, user_service: user_service_dependency, jwt_service: jwt_service_dependency) -> Token:
    new_user = user_service.create_user(user)
    user_service.save_user(new_user)
    new_user.tenant_id = new_user.id
    user_service.save_user(new_user)

    access_token = jwt_service.create_access_token({"sub": str(new_user.id)})
    return access_token

@router.post('/auth/refresh')
def refresh(jwt_service: jwt_service_dependency, user_service: user_service_dependency, google_service: google_service_dependency, microsoft_service: microsoft_service_dependency, decoded_token: verify_token_dependency, body: GoogleRefreshTokenRequest) -> str:
    tenant_id = decoded_token['sub']
    user = user_service.get_user_by_tenant_id(tenant_id)

    if user.tenant == Tenant.LOCAL:
        new_access_token = jwt_service.create_access_token({"sub": str(user.id)}).access_token
    elif user.tenant == Tenant.GOOGLE:
        if body.refresh_token:
            new_access_token = google_service.refresh_id_token(body.refresh_token)["id_token"]
        else:
            raise HTTPException(
                detail='No refresh token provided!',
                status_code=400
            )
    elif user.tenant == Tenant.MICROSOFT:
        if body.refresh_token:
            new_access_token = microsoft_service.refresh_id_token(body.refresh_token)["id_token"]
        else:
            raise HTTPException(
                detail='No refresh token provided!',
                status_code=400
            )
    else:
        raise HTTPException(
            detail='Tenant not supported',
            status_code=400
        )

    
    return new_access_token

@router.get('/auth/verify')
def verify_token(decoded_token: verify_token_dependency):
    return {"isValid": True}

@router.post('/auth/microsoft')
async def get_tokens(body: AuthCodeRequest, microsoft_service: microsoft_service_dependency):
    data = microsoft_service.fetch_tokens(body.code)
    return {
        'refresh_token': data['refresh_token'],
        'access_token': data['id_token']
    }

@router.post('/auth/google')
async def get_tokens(body: AuthCodeRequest, google_service: google_service_dependency) -> GoogleTokens:
    
    data = google_service.fetch_tokens(body.code)
    return {
        'refresh_token': data['refresh_token'],
        'access_token': data['id_token'] # data contains access_token and id_token, but access_token is required to be passed when using google api, while id_token is simple google jwt that we can validate.
    } 