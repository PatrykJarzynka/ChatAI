from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session

from models.token import Token
from models.auth_code_request import AuthCodeRequest
from models.google_refresh_token_request import GoogleRefreshTokenRequest
from models.local_user_data import LocalUserData
from enums.tenant import Tenant
from models.api_tokens import ApiTokens
from database import get_session
from containers import jwt_service_dependency, google_service_dependency, microsoft_service_dependency, user_service_dependency, role_service_dependency, auth_none
from tables.user import User


router = APIRouter()

session_dependency = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post('/auth/login')
async def login_for_access_token(
        user_service: user_service_dependency,
        jwt_service: jwt_service_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = user_service.authenticate_local_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return jwt_service.create_access_token({"sub": str(user.id)})


@router.post('/auth/register')
def register(user_data: LocalUserData, user_service: user_service_dependency, jwt_service: jwt_service_dependency, role_service: role_service_dependency) -> Token:
    already_exist = user_service.is_user_with_provided_email_in_db(user_data.email)

    if already_exist:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_user = user_service.hash_user_password(user_data)
    new_user = User(email=hashed_user.email, password=hashed_user.password,full_name=hashed_user.full_name, tenant=Tenant.LOCAL)
    user_service.save_user(new_user)
    
    new_user.external_user_id = str(new_user.id)
    user_service.save_user(new_user)

    role_service.save_user_default_role(new_user.id)
   
    access_token = jwt_service.create_access_token({"sub": str(new_user.id)})
    return access_token

@router.post('/auth/refresh')
def refresh(jwt_service: jwt_service_dependency, user_service: user_service_dependency, google_service: google_service_dependency, microsoft_service: microsoft_service_dependency, body: GoogleRefreshTokenRequest, decoded_token = Depends(auth_none)) -> str:
    if not body.refresh_token:
        raise HTTPException(
            detail='No refresh token provided!',
            status_code=400
        )
    

    external_user_id = decoded_token['sub']
    user = user_service.get_user_by_external_user_id(external_user_id)

    match user.tenant:
        case Tenant.LOCAL: new_access_token = jwt_service.create_access_token({"sub": str(user.id)}).access_token
        case Tenant.GOOGLE: new_access_token = google_service.refresh_tokens(body.refresh_token)["id_token"]
        case Tenant.MICROSOFT: new_access_token = microsoft_service.refresh_tokens(body.refresh_token)["id_token"]
    
    return new_access_token

@router.get('/auth/verify', dependencies=[Depends(auth_none)])
def verify_token() -> dict[str, bool]:
    return {"isValid": True}

@router.post('/auth/microsoft')
async def get_microsoft_tokens(body: AuthCodeRequest, microsoft_service: microsoft_service_dependency) -> ApiTokens:
    data = microsoft_service.fetch_tokens(body.code)
    return ApiTokens(refresh_token=data['refresh_token'], access_token=data['id_token']) # data contains access_token and id_token, but access_token is required to be passed when using google api, while id_token is simple google jwt that we can validate.

@router.post('/auth/google')
async def get_google_tokens(body: AuthCodeRequest, google_service: google_service_dependency) -> ApiTokens:
    data = google_service.fetch_tokens(body.code)
    return ApiTokens(refresh_token=data['refresh_token'], access_token=data['id_token']) # data contains access_token and id_token, but access_token is required to be passed when using google api, while id_token is simple google jwt that we can validate.