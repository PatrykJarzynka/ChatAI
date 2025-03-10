from typing import TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from app_types.tenant import Tenant

if TYPE_CHECKING:
    from db_models.chat_model import Chat


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(nullable=True) # password can be null when user is registered through Google Account
    tenant_id: str = Field(unique=True, nullable=True)
    full_name: str = Field(nullable=False)
    tenant: str = Tenant

    chats: list["Chat"] = Relationship(back_populates="user")
