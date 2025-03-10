from pydantic import BaseModel, EmailStr
from app_types.tenant import Tenant


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str | None
    full_name: str
    tenant: Tenant
    tenant_id: str | None = None
