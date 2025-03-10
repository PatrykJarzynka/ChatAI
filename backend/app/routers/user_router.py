from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app_types.user_response_dto import UserResponseDTO
from app_types.user_create_dto import UserCreateDTO
from app_types.tenant import Tenant
from dependencies import verify_token_dependency
from database import get_session
from dependencies import hash_service_dependency
from services.auth.jwt_service import JWTService
from services.user_service import UserService

router = APIRouter()
session_dependency = Annotated[Session, Depends(get_session)]


def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
    return UserService(session, hash_service)


def get_jwt_service():
    return JWTService()


user_service_dependency = Annotated[UserService, Depends(get_user_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]

@router.get("/user/me", response_model=UserResponseDTO)
def get_user_by_tenant_id(user_service: user_service_dependency, decoded_token: verify_token_dependency):
    user_id = decoded_token['sub']
    return user_service.get_user_by_tenant_id(user_id)


@router.post('/user/google')
def create_or_update_user(user_service: user_service_dependency, decoded_token: verify_token_dependency) -> None:
    user_email = decoded_token['email']
    google_id = decoded_token['sub']

    if user_service.is_google_user_in_db(google_id): #TODO: Handle case when user with the same tenant id is already in the db
        return
    elif user_service.is_user_with_provided_email_in_db(user_email): #TODO: Handle case when local user with the same email as google email is already in the db
        return
    else:
        user_name = decoded_token['given_name']
        user_surname = decoded_token['family_name']
        user_full_name = f"{user_name} {user_surname}"
        

        new_user_data = UserCreateDTO(tenant_id=google_id, email=user_email, password=None, full_name=user_full_name, tenant=Tenant.GOOGLE)
        new_user = user_service.create_user(new_user_data)
        user_service.save_user(new_user)
        return
