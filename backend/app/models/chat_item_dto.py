from pydantic import BaseModel


class ChatItemDTO(BaseModel):
    user_message: str
    bot_message: str
