from pydantic import BaseModel

class ApiTokens(BaseModel):
    access_token: str
    refresh_token: str