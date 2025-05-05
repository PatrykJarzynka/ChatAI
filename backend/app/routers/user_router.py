from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from models.user_response_dto import UserResponseDTO
from models.user_create_dto import UserCreateDTO
from models.tenant import Tenant
from containers import user_service_dependency, token_decoder

router = APIRouter()

@router.get("/user/me", response_model=UserResponseDTO)
def get_user_by_tenant_id(user_service: user_service_dependency, decoded_token: token_decoder):
    user_id = decoded_token['sub']
    return user_service.get_user_by_tenant_id(user_id)

@router.post('/user/microsoft')
def create_or_update_microsoft_user(user_service: user_service_dependency, decoded_token: token_decoder) -> None:
    user_email = decoded_token['email']
    microsoft_id = decoded_token['sub']

    if user_service.is_tenant_user_in_db(microsoft_id): #TODO: Handle case when user with the same tenant id is already in the db
        return
    elif user_service.is_user_with_provided_email_in_db(user_email): #TODO: Handle case when local user with the same email as google email is already in the db
        return
    else:
        user_full_name = decoded_token['name']

        new_user_data = UserCreateDTO(tenant_id=microsoft_id, email=user_email, password=None, full_name=user_full_name, tenant=Tenant.MICROSOFT)
        new_user = user_service.create_user(new_user_data)
        user_service.save_user(new_user)
        return


@router.post('/user/google')
def create_or_update_google_user(user_service: user_service_dependency, decoded_token: token_decoder) -> None:
    user_email = decoded_token['email']
    google_id = decoded_token['sub']

    if user_service.is_tenant_user_in_db(google_id): #TODO: Handle case when user with the same tenant id is already in the db
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
