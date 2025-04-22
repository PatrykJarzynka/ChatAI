from pydantic import BaseModel

class TokenServiceConfig(BaseModel):
    client_id: str
    secret: str
    redirect_url: str
    auth_url: str