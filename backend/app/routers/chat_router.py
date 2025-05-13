from fastapi import APIRouter, HTTPException, Depends
from enums.role import Role
from models.chat_dto import ChatDto
from models.chat_history import ChatHistory
from models.user_chat_data import UserChatData
from tables.chat import Chat
from containers import user_service_dependency, bot_service_dependency, chat_service_dependency, chat_history_dependency, authorize, auth_none

router = APIRouter()


@router.get('/chat', response_model=ChatDto)
def get_new_chat(chat_service: chat_service_dependency, user_service: user_service_dependency, decoded_token = Depends(auth_none)) -> Chat:
    tenant_id = decoded_token['sub']
    user_id = user_service.get_user_by_tenant_id(tenant_id).id
    
    new_chat = chat_service.create_new_chat(user_id)
    chat_service.save_chat(new_chat)

    return new_chat

@router.get('/chat/history', dependencies=[Depends(auth_none)])
async def get_chat_histories(userId: int, chat_history_service: chat_history_dependency) -> list[ChatHistory]:
    return chat_history_service.get_chats_history_data_by_user_id(userId)


@router.get('/chat/{chat_id}', dependencies=[Depends(auth_none)], response_model=ChatDto)
def get_chat_by_id(chat_id: int, chat_service: chat_service_dependency) -> Chat | None:
    return chat_service.get_chat_by_id(chat_id)

@router.post('/chat', dependencies=[Depends(auth_none)])
def on_user_query_send(user_chat_data: UserChatData, chat_service: chat_service_dependency, bot_service: bot_service_dependency) -> str:
    try:
        new_chat_item = chat_service.create_chat_item(user_chat_data)
        new_chat_item.bot_message = bot_service.chat(user_chat_data.message)

        chat_service.add_chat_item_to_chat(new_chat_item, user_chat_data.chat_id)

        return new_chat_item.bot_message
    except Exception as e:
        chat_service.delete_chat(user_chat_data.chat_id)
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
