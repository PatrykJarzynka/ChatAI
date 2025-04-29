from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session
from config import get_settings
from utilities.chat_items_parser import ChatItemsParser
from starlette.requests import Request

from utilities.token_extractor import TokenExtractor
from utilities.token_exception_handler import TokenExceptionHandler

from services.chat_service import ChatService
from services.open_ai_chat_service import OpenAIChatService
from services.web_service import WebService
from services.auth.jwt_service import JWTService
from services.auth.hash_service import HashService
from services.auth.google_service import GoogleService
from services.auth.microsoft_service import MicrosoftService
from services.user_service import UserService
from services.chat_history_service import ChatHistoryService

from clients.serper_api_search_engine import SerperApiSearchEngine
from clients.serper_response_parser import SerperResponseParser
from clients.weather_service import WeatherService

from llama_index.core.tools import FunctionTool
from llama_index.core.memory import ChatMemoryBuffer




session_dependency = Annotated[Session, Depends(get_session)]
jwt_service_dependency = Annotated[JWTService, Depends(JWTService)]
hash_service_dependency = Annotated[HashService, Depends(HashService)]
microsoft_service_dependency = Annotated[MicrosoftService, Depends(MicrosoftService)]
google_service_dependency = Annotated[GoogleService, Depends(GoogleService)]

def get_chat_service(session: session_dependency):
    return ChatService(session)

def get_chat_history_service(session: session_dependency):
    return ChatHistoryService(session)

def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
     return UserService(session, hash_service)

def get_chat_history_service(session: session_dependency):
    return ChatHistoryService(session)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]
token_extractor_dependency = Annotated[TokenExtractor, Depends(TokenExtractor)]
chat_service_dependency = Annotated[ChatService, Depends(get_chat_service)]
chat_history_dependency = Annotated[ChatHistoryService, Depends(get_chat_history_service)]


@TokenExceptionHandler().handle_token_exceptions
def decode_token(
                    request: Request,
                    token_extractor: token_extractor_dependency,
                    microsoft_service:microsoft_service_dependency,
                    google_service: google_service_dependency, 
                    jwt_service: jwt_service_dependency
                ):
    token = token_extractor.get_token_from_header(request)
    issuer = jwt_service.get_token_issuer(token)

    if 'accounts.google.com' in issuer:
        return google_service.decode_token(token)
    elif 'login.microsoftonline.com' in issuer:
        return microsoft_service.decode_token(token)
    elif issuer == 'local':
        return jwt_service.decode_local_token(token)
    else:
        raise ValueError('Unknown provider')


token_decoder = Annotated[dict, Depends(decode_token)]

async def get_bot_service(request: Request, chat_service: chat_service_dependency, _: token_decoder) -> OpenAIChatService:

        SERPER_API_KEY = get_settings().SERPER_API_KEY
        web_service = WebService(SerperApiSearchEngine(api_key=SERPER_API_KEY), SerperResponseParser())
        weather_service = WeatherService()

        chat_items = chat_service.get_chat_items((await request.json()).get('chat_id'))
        chat_messages = ChatItemsParser().parse_to_chat_messages(chat_items)

        memory = ChatMemoryBuffer.from_defaults(chat_history=chat_messages)

        web_search_tool = FunctionTool.from_defaults(
            web_service.provide_documents, description='Useful for getting current web data.'
        )
        weather_search_tool = FunctionTool.from_defaults(
            weather_service.get_city_weather_data, description='Useful for getting the data about current weather and air pollution in given location. Use all of the parameters in English translation.'
        )

        return OpenAIChatService(tools=[web_search_tool, weather_search_tool],memory=memory, bot_description="You are intelligent assistant who is responsible for answering user's questions.")

bot_service_dependency = Annotated[OpenAIChatService, Depends(get_bot_service)]

        