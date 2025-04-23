from typing import Annotated

from fastapi import Depends

from services.auth.hash_service import HashService
from services.auth.jwt_service import JWTService
from services.auth.google_service import GoogleService
from services.auth.microsoft_service import MicrosoftService
from utilities.token_extractor import TokenExtractor
from utilities.token_exception_handler import TokenExceptionHandler
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

def get_token_extractor():
    return TokenExtractor()

def get_token_exception_handler():
    return TokenExceptionHandler()

def get_memory():
    return MemoryBufferService()



microsoft_service_dependency = Annotated[MicrosoftService, Depends(get_microsoft_service)]
google_service_dependency = Annotated[GoogleService, Depends(get_google_service)]
hash_service_dependency = Annotated[HashService, Depends(get_hash_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]
memory_buffer_dependency = Annotated[MemoryBufferService, Depends(get_memory)]

@TokenExceptionHandler().handle_token_exceptions
def decode_token(
                    request: Request,
                    token_extractor: TokenExtractor = Depends(get_token_extractor),
                    microsoft_service: MicrosoftService = Depends(get_microsoft_service),
                    google_service: GoogleService = Depends(get_google_service), 
                    jwt_service: JWTService = Depends(get_jwt_service)):
    token = token_extractor.get_token_from_header(request)
    issuer = jwt_service.get_token_issuer(token)

    if 'accounts.google.com' in issuer:
        return google_service.decode_token(token)
    elif 'login.microsoftonline.com' in issuer:
        return microsoft_service.decode_token(token)
    elif issuer == 'local':
        return jwt_service.decode_local_token(token)
    else:
        raise ValueError('Unknown provider')
        
    

token_decoder = Annotated[dict, Depends(decode_token)]


