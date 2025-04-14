from pydantic import BaseModel
from sqlmodel import Field

from models.chat_item_dto import ChatItemDTO


class ChatDto(BaseModel):
    id: int
    chat_items: list[ChatItemDTO] = Field(default_factory=list)
