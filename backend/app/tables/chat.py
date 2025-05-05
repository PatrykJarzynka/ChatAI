from sqlmodel import SQLModel, Field, Relationship
from app.tables.user import User

from app.tables.chat_item import ChatItem


class Chat(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chat_items: list[ChatItem] = Relationship(back_populates="chat")

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="chats")

