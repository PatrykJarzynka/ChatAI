from pydantic import BaseModel, EmailStr
from models.tenant import Tenant
from typing import List
from tables.chat import Chat

class InsertTenantUserDTO(BaseModel):
    email: EmailStr
    password: str | None
    tenant_id: str 
    full_name: str
    tenant: Tenant
    chats: List[Chat]

class InsertLocalUserDTO(BaseModel):
    email: EmailStr
    password: str | None
    full_name: str
    tenant: Tenant
    chats: List[Chat]