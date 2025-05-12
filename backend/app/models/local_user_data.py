from pydantic import BaseModel, EmailStr
from enums.tenant import Tenant


class LocalUserData(BaseModel):
    email: EmailStr
    password: str
    full_name: str
