from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from models.tenant import Tenant

if TYPE_CHECKING:
    from app.tables.chat import Chat

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False)
    password: str | None = Field(nullable=True) # password can be null when user is registered through Google or Microsoft Account
    tenant_id: str = Field(unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    tenant: Tenant = Field(unique=False)
    chats: list["Chat"] = Relationship(back_populates="user")
