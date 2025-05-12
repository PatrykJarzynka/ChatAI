
from sqlmodel import Relationship, SQLModel, Field 
from tables.role import Role


class UserRole(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True)
    role_id: int = Field(foreign_key='role.id')

    role: Role = Relationship(back_populates="users")
