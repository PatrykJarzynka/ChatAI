from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session
from services.chat_service import ChatService
from services.open_ai_chat_service import OpenAIChatService
from services.memory_buffer_service import MemoryBufferService
from services.web_service import WebService
from dependencies import token_decoder
from config import get_settings
from clients.serper_api_manager import SerperApiManager
from clients.serper_response_parser import SerperResponseParser
from utilities.chat_items_parser import ChatItemsParser
from services.weather_service import WeatherService
from starlette.requests import Request
from llama_index.core.tools import FunctionTool

session_dependency = Annotated[Session, Depends(get_session)]

def get_chat_service(session: session_dependency):
      return ChatService(session)

async def get_bot_service(request: Request, decoded_token: token_decoder, chat_service: ChatService = Depends(get_chat_service)) -> OpenAIChatService:

        SERPER_API_KEY = get_settings().SERPER_API_KEY
        web_service = WebService(SerperApiManager(api_key=SERPER_API_KEY), SerperResponseParser())
        weather_service = WeatherService()

        chat_items = chat_service.get_chat_items((await request.json()).get('chat_id'))
        chat_messages = ChatItemsParser().parse_to_chat_messages(chat_items)

        memory = MemoryBufferService(chat_messages) 

        web_search_tool = FunctionTool.from_defaults(
            web_service.provide_documents, description='Useful for getting current web data.'
        )
        weather_search_tool = FunctionTool.from_defaults(
            weather_service.get_city_weather_data, description='Useful for getting the data about current weather and air pollution in given location. Use all of the parameters in English translation.'
        )

        return OpenAIChatService(tools=[web_search_tool, weather_search_tool],memory=memory.get_memory(), bot_description="You are intelligent assistant who is responsible for answering user's questions.")

