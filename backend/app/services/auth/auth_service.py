import jwt
from starlette.requests import Request
from fastapi import HTTPException, status

class AuthService:

    def __init__(self):
        self.token_prefix='Bearer'

    def get_token_from_header(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
        
        header, _, token = authorization.partition(' ')

        if header != self.token_prefix:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        
        return token
    
    def handle_token_exceptions(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except jwt.InvalidSignatureError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid signature.')
            except jwt.InvalidIssuerError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid issuer')
            except jwt.ExpiredSignatureError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return wrapper

