from pydantic import BaseModel

class GoogleTokenDTO(BaseModel):
    google_token: str