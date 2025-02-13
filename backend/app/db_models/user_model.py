from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
