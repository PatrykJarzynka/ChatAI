from pydantic import BaseModel

class GoogleRefreshTokenRequest(BaseModel):
    refresh_token: str | None