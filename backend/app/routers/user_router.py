from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app_types.user_response_dto import UserResponseDTO
from database import get_session
from dependencies import hash_service_dependency
from services.auth.jwt_service import JWTService
from services.user_service import UserService

router = APIRouter()
session_dependency = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
    return UserService(session, hash_service)


def get_jwt_service():
    return JWTService()


user_service_dependency = Annotated[UserService, Depends(get_user_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]


@router.get("/user/me", response_model=UserResponseDTO)
def get_user_by_id(user_service: user_service_dependency, jwt_service: jwt_service_dependency,
                   token: Annotated[str, Depends(oauth2_scheme)]):
    dekodedToken = jwt_service.decode_access_token(token)
    user_id = int(dekodedToken['sub'])
    return user_service.get_user_by_id(user_id)
