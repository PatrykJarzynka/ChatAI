from dataclasses import dataclass


@dataclass
class UserChatData:
    message: str
    chat_id: int
