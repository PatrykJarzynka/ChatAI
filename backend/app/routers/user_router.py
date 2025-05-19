from fastapi import APIRouter, Depends

from models.user_response_dto import UserResponseDTO
from enums.tenant import Tenant
from containers import user_service_dependency, auth_none, role_service_dependency
from tables.user import User

router = APIRouter()

@router.get("/user/me", response_model=UserResponseDTO)
def get_user_by_external_user_id(user_service: user_service_dependency, decoded_token = Depends(auth_none)):
    external_user_id = decoded_token['sub']
    return user_service.get_user_by_external_user_id(external_user_id)

@router.post('/user/microsoft')
def create_or_update_microsoft_user(user_service: user_service_dependency, role_service: role_service_dependency, decoded_token = Depends(auth_none)) -> None:
    user_email = decoded_token['email']
    microsoft_id = decoded_token['sub']

    if user_service.is_tenant_user_in_db(microsoft_id): #TODO: Handle case when user with the same tenant id is already in the db
        return
    elif user_service.is_user_with_provided_email_in_db(user_email): #TODO: Handle case when local user with the same email as google email is already in the db
        return
    else:
        user_full_name = decoded_token['name']

        new_user = User(email=user_email, password=None, full_name=user_full_name, tenant=Tenant.MICROSOFT, external_user_id=microsoft_id)
        user_service.save_user(new_user)
        role_service.save_user_default_role(new_user.id)
        return


@router.post('/user/google')
def create_or_update_google_user(user_service: user_service_dependency, role_service: role_service_dependency, decoded_token = Depends(auth_none)) -> None:
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
        
        new_user = User(email=user_email, password=None, full_name=user_full_name, tenant=Tenant.GOOGLE, external_user_id=google_id)
        user_service.save_user(new_user)
        role_service.save_user_default_role(new_user.id)
        return
