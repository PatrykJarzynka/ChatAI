from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.app_types.chat_dto import ChatDto
from app.app_types.chat_history import ChatHistory
from app.app_types.user_chat_data import UserChatData
from app.database import get_session
from app.db_models.chat_model import Chat
from app.services.bot_service import BotService
from app.services.chat_history_service import ChatHistoryService
from app.services.chat_service import ChatService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

session_dependency = Annotated[Session, Depends(get_session)]


def get_bot_service():
    return BotService()


def get_chat_service(session: session_dependency):
    return ChatService(session)


def get_chat_history_service(session: session_dependency):
    return ChatHistoryService(session)


bot_service_dependency = Annotated[BotService, Depends(get_bot_service)]
chat_service_dependency = Annotated[ChatService, Depends(get_chat_service)]
chat_history_service_dependency = Annotated[ChatHistoryService, Depends(get_chat_history_service)]


@router.get('/chat', response_model=ChatDto)
def get_new_chat(chat_service: chat_service_dependency) -> Chat:
    new_chat = chat_service.create_new_chat()
    chat_service.save_chat(new_chat)
    return new_chat


@router.get('/chat/history')
async def get_all_chats_history(chat_history_service: chat_history_service_dependency) -> list[ChatHistory]:
    return chat_history_service.get_all_chats_history_data()


@router.get('/chat/{chat_id}', response_model=ChatDto)
def get_chat_by_id(chat_id: int, chat_service: chat_service_dependency) -> Chat:
    return chat_service.get_chat_by_id(chat_id)


@router.post('/chat')
def on_user_query_send(user_chat_data: UserChatData, chat_service: chat_service_dependency,
                       bot_service: bot_service_dependency) -> str:
    try:
        new_chat_item = chat_service.create_chat_item(user_chat_data)
        current_chat_items = chat_service.get_chat_items(user_chat_data.chat_id)
        new_chat_item.bot_message = bot_service.fetch_bot_response(user_chat_data.message, current_chat_items)

        chat_service.add_chat_item_to_chat(new_chat_item, user_chat_data.chat_id)

        return new_chat_item.bot_message
    except Exception as e:
        chat_service.delete_chat(user_chat_data.chat_id)
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
