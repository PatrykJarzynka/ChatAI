from sqlmodel import SQLModel, Field, Relationship
from tables.user import User

from tables.chat_item import ChatItem


class Chat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_items: list[ChatItem] = Relationship(back_populates="chat")

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="chats")

