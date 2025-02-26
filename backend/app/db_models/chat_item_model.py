from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship, Column, Text

if TYPE_CHECKING:
    from db_models.chat_model import Chat


class ChatItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_message: str = Field(sa_column=Column(Text))
    bot_message: str | None = Field(sa_column=Column(Text), default=None)

    chat_id: int | None = Field(default=None, foreign_key='chat.id')
    chat: Optional["Chat"] = Relationship(back_populates='chat_items')
