from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.mysql import LONGTEXT
from tables.user import User


class File(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    text: str = Field(sa_column=Column(LONGTEXT))
    name: str = Field(nullable=False)
    extension: str = Field(nullable=False)
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="files")