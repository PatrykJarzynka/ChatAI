from typing import TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from db_models.chat_model import Chat


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
    chats: list["Chat"] = Relationship(back_populates="user")
