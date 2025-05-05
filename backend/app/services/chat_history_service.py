from sqlmodel import select, Session

from models.chat_history import ChatHistory
from app.tables.chat import Chat


class ChatHistoryService:
    def __init__(self, session: Session):
        self.session = session

    def get_chats_by_user_id(self, user_id: int) -> list[Chat]: 
        statement = select(Chat).where(Chat.user_id == user_id)
        return self.session.exec(statement).all()

    def get_chats_history_data_by_user_id(self, user_id: int) -> list[ChatHistory]:
        chats_by_user_id=self.get_chats_by_user_id(user_id)

        return list(filter(lambda x: x.title != '', map(self.convert_chat_to_history_data, chats_by_user_id)))

    @staticmethod
    def convert_chat_to_history_data(chat: Chat) -> ChatHistory:
        if len(chat.chat_items):
            return ChatHistory(id=chat.id, title=chat.chat_items[0].user_message)
        else:
            return ChatHistory(id=chat.id, title='')
