from pydantic import BaseModel

class GoogleTokens(BaseModel):
    access_token: str
    refresh_token: str