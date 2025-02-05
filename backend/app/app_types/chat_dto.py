from pydantic import BaseModel
from sqlmodel import Field

from app.app_types.chat_item_dto import ChatItemDTO


class ChatDto(BaseModel):
    id: int
    chat_items: list[ChatItemDTO] = Field(default_factory=list)
