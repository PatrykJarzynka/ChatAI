from typing import Annotated

from fastapi import Depends

from services.auth.hash_service import HashService
from services.auth.jwt_service import JWTService
from services.auth.google_service import GoogleService
from services.auth.microsoft_service import MicrosoftService
from services.auth.auth_service import AuthService
from services.open_ai_chat_service import OpenAIChatService
from services.memory_buffer_service import MemoryBufferService
from starlette.requests import Request


def get_jwt_service():
    return JWTService()

def get_hash_service():
    return HashService()

def get_google_service():
    return GoogleService()

def get_microsoft_service():
    return MicrosoftService()

def get_auth_service():
    return AuthService()

def get_memory():
    return MemoryBufferService()



microsoft_service_dependency = Annotated[MicrosoftService, Depends(get_microsoft_service)]
google_service_dependency = Annotated[GoogleService, Depends(get_google_service)]
hash_service_dependency = Annotated[HashService, Depends(get_hash_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]
memory_buffer_dependency = Annotated[MemoryBufferService, Depends(get_memory)]

def verify_token(
                    request: Request,
                    auth_service: AuthService = Depends(get_auth_service),
                    microsoft_service: MicrosoftService = Depends(get_microsoft_service),
                    google_service: GoogleService = Depends(get_google_service), 
                    jwt_service: JWTService = Depends(get_jwt_service)):

    @auth_service.handle_token_exceptions
    def verify(
            request: Request,
            microsoft_service: MicrosoftService,
            google_service: GoogleService,
            jwt_service: JWTService,
    ):
        token = auth_service.get_token_from_header(request)
        decoded_token = jwt_service.decode_token(token)
        issuer = decoded_token['iss']

        if 'accounts.google.com' in issuer:
            return google_service.verify_and_decode_token(token)
        elif 'login.microsoftonline.com' in issuer:
            return microsoft_service.validate_token(token)
        elif issuer == 'local':
            return jwt_service.decode_local_token(token)
        else:
            raise ValueError('Unknown provider')
        
    return verify(request, microsoft_service, google_service, jwt_service)

verify_token_dependency = Annotated[dict, Depends(verify_token)]


