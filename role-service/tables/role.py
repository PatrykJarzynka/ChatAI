from sqlmodel import SQLModel, Field, Relationship
from enums.role import RoleEnum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from tables.user_role import UserRole

class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    role: RoleEnum = Field(unique=False)

    users: List["UserRole"] = Relationship(back_populates="role")

from tables.user_role import UserRole