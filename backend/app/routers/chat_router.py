from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlmodel import Session

from models.chat_dto import ChatDto
from models.chat_history import ChatHistory
from models.user_chat_data import UserChatData
from database import get_session
from db_models.chat_model import Chat
from services.chat_history_service import ChatHistoryService
from services.open_ai_chat_service import OpenAIChatService
from services.chat_service import ChatService
from services.auth.jwt_service import JWTService
from services.auth.google_service import GoogleService
from services.user_service import UserService
from services.memory_buffer_service import MemoryBufferService
from utilities.chat_items_parser import ChatItemsParser
from dependencies import verify_token_dependency
from starlette.requests import Request
from containers import session_dependency, get_user_service, get_bot_service

router = APIRouter()


def get_chat_service(session: session_dependency):
    return ChatService(session)

def get_chat_history_service(session: session_dependency):
    return ChatHistoryService(session)

def get_jwt_service():
    return JWTService()

def get_google_service():
    return GoogleService()

chat_service_dependency = Annotated[ChatService, Depends(get_chat_service)]
chat_history_service_dependency = Annotated[ChatHistoryService, Depends(get_chat_history_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]
user_service_dependency = Annotated[UserService, Depends(get_user_service)]


@router.get('/chat', response_model=ChatDto)
def get_new_chat(request: Request, chat_service: chat_service_dependency, user_service: user_service_dependency, decoded_token: verify_token_dependency) -> Chat:
    tenant_id = decoded_token['sub']
    user_id = user_service.get_user_by_tenant_id(tenant_id).id
    
    request.app.state.memory_service[user_id] = MemoryBufferService()
   
    new_chat = chat_service.create_new_chat(user_id)
    chat_service.save_chat(new_chat)

    return new_chat


@router.get('/chat/history')
async def get_chat_histories(userId: int, chat_history_service: chat_history_service_dependency, decoded_token: verify_token_dependency) -> list[ChatHistory]:
    return chat_history_service.get_chats_history_data_by_user_id(userId)


@router.get('/chat/{chat_id}', response_model=ChatDto)
def get_chat_by_id(request: Request, chat_id: int, chat_service: chat_service_dependency, user_service: user_service_dependency, decoded_token: verify_token_dependency) -> Chat:
    tenant_id = decoded_token['sub']
    user_id = user_service.get_user_by_tenant_id(tenant_id).id

    chat = chat_service.get_chat_by_id(chat_id)
    parsed_items = ChatItemsParser().parse_to_chat_messages(chat.chat_items)

    request.app.state.memory_service[user_id] = MemoryBufferService(parsed_items)

    return chat


@router.post('/chat')
def on_user_query_send(request: Request, user_chat_data: UserChatData, chat_service: chat_service_dependency, user_service: user_service_dependency, decoded_token: verify_token_dependency, bot_service: OpenAIChatService = Depends(get_bot_service)) -> str:
    try:
        tenant_id = decoded_token['sub']
        user_id = user_service.get_user_by_tenant_id(tenant_id).id

        new_chat_item = chat_service.create_chat_item(user_chat_data)
        current_chat_items = chat_service.get_chat_items(user_chat_data.chat_id)
        new_chat_item.bot_message = bot_service.chat(user_chat_data.message, current_chat_items)

        chat_service.add_chat_item_to_chat(new_chat_item, user_chat_data.chat_id)

        parsed_items = ChatItemsParser().parse_to_chat_messages([new_chat_item])

        memory_buffer = request.app.state.memory_service[user_id]
        memory_buffer.add_messages_to_memory(parsed_items)

        return new_chat_item.bot_message
    except Exception as e:
        chat_service.delete_chat(user_chat_data.chat_id)
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
