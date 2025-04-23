import jwt
from fastapi import HTTPException, status
from functools import wraps

class TokenExceptionHandler:
    def handle_token_exceptions(self, func):
        @wraps(func)
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