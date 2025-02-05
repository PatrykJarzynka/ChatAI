from dataclasses import dataclass


@dataclass
class UserChatData:
    message: str
    user_id: str
    chat_id: int
