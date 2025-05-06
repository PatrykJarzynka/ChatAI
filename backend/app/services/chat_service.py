from sqlmodel import Session, select

from models.user_chat_data import UserChatData
from tables.chat_item import ChatItem
from tables.chat import Chat

class ChatService:

    def __init__(self, session: Session):
        self.session = session

    def delete_chat(self, chat_id: int):
        chat = self.get_chat_by_id(chat_id)
        self.session.delete(chat)
        self.session.commit()

    def get_chat_by_id(self, chat_id: int) -> Chat | None:
        statement = select(Chat).where(Chat.id == chat_id)
        return self.session.exec(statement).first()

    def save_chat(self, chat: Chat) -> None:
        self.session.add(chat)
        self.session.commit()
        self.session.refresh(chat)

    def get_chat_items(self, chat_id: int) -> list[ChatItem]: #TODO: Add tests for new
        chat = self.get_chat_by_id(chat_id)
        if chat:
            return chat.chat_items
        return []

    def add_chat_item_to_chat(self, chat_item: ChatItem, chat_id: int) -> None:
        current_chat = self.get_chat_by_id(chat_id)

        if current_chat:
            current_chat.chat_items.append(chat_item)
            self.session.commit()
            self.session.refresh(current_chat)
            self.session.refresh(chat_item)

        return

    @staticmethod
    def create_chat_item(user_chat_data: UserChatData) -> ChatItem:
        return ChatItem(user_message=user_chat_data.message,
                        chat_id=user_chat_data.chat_id)

    @staticmethod
    def create_new_chat(user_id: int) -> Chat:
        return Chat(user_id=user_id)
