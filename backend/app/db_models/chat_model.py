from sqlmodel import SQLModel, Field, Relationship
from db_models.user_model import User

from db_models.chat_item_model import ChatItem


class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chat_items: list[ChatItem] = Relationship(back_populates="chat")

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="chats")

