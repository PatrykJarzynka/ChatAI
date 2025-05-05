from pydantic import BaseModel
from sqlmodel import Field
from typing import List

from models.chat_item_dto import ChatItemDTO


class ChatDto(BaseModel):
    id: int
    chat_items: List[ChatItemDTO] = Field(default_factory=list)
