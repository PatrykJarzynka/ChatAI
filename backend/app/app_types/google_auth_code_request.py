from pydantic import BaseModel

class GoogleAuthCodeRequest(BaseModel):
    code: str