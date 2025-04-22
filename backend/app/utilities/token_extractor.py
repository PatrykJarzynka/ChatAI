from starlette.requests import Request
from fastapi import HTTPException, status

class TokenExtractor:

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
    


