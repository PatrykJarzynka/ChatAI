from pydantic import BaseModel, EmailStr
from models.tenant import Tenant


class LocalUserData(BaseModel):
    email: EmailStr
    password: str
    full_name: str
