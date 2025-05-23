from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from enums.tenant import Tenant

if TYPE_CHECKING:
    from tables.chat import Chat
    from tables.file import File

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False)
    password: str | None = Field(nullable=True) # password can be null when user is registered through Google or Microsoft Account
    external_user_id: str | None = Field(default=None, unique=True)
    full_name: str = Field(nullable=False)
    tenant: Tenant = Field(unique=False)

    chats: List["Chat"] = Relationship(back_populates="user")
    files: List["File"] = Relationship(back_populates="user")
