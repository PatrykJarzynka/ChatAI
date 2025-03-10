from pydantic import BaseModel

class GoogleRefreshTokenRequest(BaseModel):
    refreshToken: str | None