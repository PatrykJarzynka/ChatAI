from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session
from services.user_service import UserService
from services.open_ai_chat_service import OpenAIChatService
from services.web_service import WebService
from dependencies import hash_service_dependency, verify_token_dependency
from starlette.requests import Request
from config import get_settings
from clients.serper_api_manager import SerperApiManager
from clients.serper_response_parser import SerperResponseParser
from utilities.tool_manager import ToolManager

session_dependency = Annotated[Session, Depends(get_session)]


def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
    return UserService(session, hash_service)

def get_bot_service(request: Request, decoded_token: verify_token_dependency, user_service: UserService = Depends(get_user_service)) -> OpenAIChatService:
        tenant_id = decoded_token['sub']
        user_id = user_service.get_user_by_tenant_id(tenant_id).id

        SERPER_API_KEY = get_settings().SERPER_API_KEY
        web_service = WebService(SerperApiManager(api_key=SERPER_API_KEY), SerperResponseParser())
        tools_manager = ToolManager()
        web_search_tool = tools_manager.create_tool(callback=web_service.provide_documents, description='Search web')

        memory_buffer = request.app.state.memory_service[user_id]

        return OpenAIChatService(tools=[web_search_tool],memory=memory_buffer.get_memory(), bot_description="Test")

