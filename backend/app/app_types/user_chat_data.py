from dataclasses import dataclass


@dataclass
class UserChatData:
    message: str
    user_id: int
    chat_id: int
