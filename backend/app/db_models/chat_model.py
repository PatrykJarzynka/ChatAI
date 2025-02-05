from sqlmodel import SQLModel, Field, Relationship

from .chat_item_model import ChatItem


class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chat_items: list[ChatItem] = Relationship(back_populates="chat")
