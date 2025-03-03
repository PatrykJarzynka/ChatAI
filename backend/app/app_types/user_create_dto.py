from pydantic import BaseModel, EmailStr
from app_types.auth_provider import AuthProvider


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str | None
    full_name: str
    provider: AuthProvider
