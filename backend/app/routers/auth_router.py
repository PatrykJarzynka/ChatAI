from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session

from app_types.token import Token
from app_types.google_token_dto import GoogleTokenDTO
from app_types.user_create_dto import UserCreateDTO
from app_types.auth_provider import AuthProvider
from database import get_session
from dependencies import hash_service_dependency, jwt_service_dependency
from services.user_service import UserService
from services.auth.google_service import GoogleService

router = APIRouter()

session_dependency = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
    return UserService(session, hash_service)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]

def get_verify_token_function(jwt_service: jwt_service_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    return jwt_service.decode_access_token(token)

verify_token_dependency = Annotated[dict,Depends(get_verify_token_function)]

def get_google_service():
    return GoogleService()

google_service_dependency = Annotated[GoogleService, Depends(get_google_service)]


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

    access_token = jwt_service.create_access_token({"sub": str(new_user.id)})
    return access_token

@router.get('/auth/refresh')
def refresh(jwt_service: jwt_service_dependency, decoded_token: verify_token_dependency) -> Token:
    user_id = int(decoded_token['sub'])
    new_access_token = jwt_service.create_access_token({"sub": str(user_id)})
    return new_access_token

@router.get('/auth/verify')
def verify_token(jwt_service: jwt_service_dependency, token: Annotated[str, Depends(oauth2_scheme)], decoded_token: verify_token_dependency):
    if (decoded_token):
        return token
    
@router.post('/auth/google')
def verify_token(token_data: GoogleTokenDTO, google_service: google_service_dependency, user_service: user_service_dependency, jwt_service: jwt_service_dependency) -> Token:
    decoded_token = None

    try:
        decoded_token = google_service.verify_and_decode_token(token_data.google_token)
        google_service.validate_iss(decoded_token)
        google_service.validate_exp_time(decoded_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to validate token: {e}")
    
    user_email = decoded_token['email']
    user_already_exist = user_service.is_user_with_provided_email_in_db(user_email)

    if user_already_exist:
        existing_user = user_service.get_user_by_email(user_email)
        return jwt_service.create_access_token({"sub": existing_user.id})
    else:
        user_name = decoded_token['given_name']
        user_surname = decoded_token['family_name']
        user_full_name = f"{user_name} {user_surname}"
    
        new_user_data = UserCreateDTO(email=user_email, password=None, full_name=user_full_name, provider=AuthProvider.GOOGLE)
        return register(new_user_data, user_service, jwt_service)
   