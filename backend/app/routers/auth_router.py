from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session

from app_types.token import Token
from app_types.user_create_dto import UserCreateDTO
from database import get_session
from dependencies import hash_service_dependency, jwt_service_dependency
from services.user_service import UserService
from services.auth.jwt_service import JWTService

router = APIRouter()

session_dependency = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
    return UserService(session, hash_service)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]

def get_verify_token_function(jwt_service: jwt_service_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    return jwt_service.decode_access_token(token)

verify_token_dependency = Annotated[dict,Depends(get_verify_token_function)]


@router.post('/auth/login')
async def login_for_access_token(
        user_service: user_service_dependency,
        jwt_service: jwt_service_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = user_service.authenticate_user(form_data.username, form_data.password)

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

    access_token = jwt_service.create_access_token({"sub": str(new_user.id)})
    return access_token

@router.get('/auth/refresh')
def refresh(jwt_service: jwt_service_dependency, token: Annotated[str, Depends(oauth2_scheme)], decoded_token: verify_token_dependency) -> Token:
    user_id = int(decoded_token['sub'])
    new_access_token = jwt_service.create_access_token({"sub": str(user_id)})
    return new_access_token

@router.get('/auth/verify')
def verify_token(jwt_service: jwt_service_dependency, token: Annotated[str, Depends(oauth2_scheme)], decoded_token: verify_token_dependency):
    if (decoded_token):
        return token



