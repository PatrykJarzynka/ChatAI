from sqlmodel import select, Session

from app.app_types.chat_history import ChatHistory
from app.db_models.chat_model import Chat


class ChatHistoryService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_chats_history_data(self) -> list[ChatHistory]:
        statement = select(Chat)
        allChats = self.session.exec(statement).all()

        return list(filter(lambda x: x.title != '', map(self.convert_chat_to_history_data, allChats)))

    @staticmethod
    def convert_chat_to_history_data(chat: Chat) -> ChatHistory:
        if len(chat.chat_items):
            return ChatHistory(id=chat.id, title=chat.chat_items[0].user_message)
        else:
            return ChatHistory(id=chat.id, title='')
