from fastapi import HTTPException, status
from services.auth.google_service import GoogleService
from services.auth.jwt_service import JWTService
from services.auth.microsoft_service import MicrosoftService
from utilities.token_exception_handler import TokenExceptionHandler


class TokenValidator:
    def __init__(self, jwt_service: JWTService, google_service: GoogleService, microsoft_service: MicrosoftService) -> None:
        self.jwt_service = jwt_service
        self.google_service = google_service
        self.microsoft_service = microsoft_service

    @TokenExceptionHandler().handle_token_exceptions
    def validate_token(self, authorization: str) -> dict:
        header, _, token = authorization.partition(' ')
        
        if header != 'Bearer':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        
        issuer = self.jwt_service.get_token_issuer(token)
        
        if 'accounts.google.com' in issuer:
            return self.google_service.decode_token(token)
        elif 'login.microsoftonline.com' in issuer:
            return self.microsoft_service.decode_token(token)
        elif issuer == 'local':
            return self.jwt_service.decode_local_token(token)
        else:
            raise ValueError('Unknown provider')