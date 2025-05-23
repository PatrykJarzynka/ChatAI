from typing import Annotated, Callable, Optional
from fastapi import Depends, HTTPException, Header, status
from sqlmodel import Session
from app.services.file_service import FileService
from enums.role import Role
from services.role_service import RoleService
from database import get_session
from config import get_settings
from utilities.chat_items_parser import ChatItemsParser
from utilities.file_decoder import FileDecoder
from starlette.requests import Request

from utilities.token_validator import TokenValidator

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
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool

session_dependency = Annotated[Session, Depends(get_session)]
jwt_service_dependency = Annotated[JWTService, Depends(JWTService)]
hash_service_dependency = Annotated[HashService, Depends(HashService)]
microsoft_service_dependency = Annotated[MicrosoftService, Depends(MicrosoftService)]
google_service_dependency = Annotated[GoogleService, Depends(GoogleService)]
role_service_dependency = Annotated[RoleService, Depends(RoleService)]
file_decoder_dependency = Annotated[FileDecoder, Depends(FileDecoder)]

def get_file_service(session: session_dependency):
     return FileService(session)

def get_chat_service(session: session_dependency):
    return ChatService(session)

def get_user_service(session: session_dependency, hash_service: hash_service_dependency):
     return UserService(session, hash_service)

def get_chat_history_service(session: session_dependency):
    return ChatHistoryService(session)

def get_token_validator(jwt: jwt_service_dependency, google: google_service_dependency, microsoft: microsoft_service_dependency):
     return TokenValidator(jwt_service=jwt, google_service=google, microsoft_service=microsoft)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]
chat_service_dependency = Annotated[ChatService, Depends(get_chat_service)]
chat_history_dependency = Annotated[ChatHistoryService, Depends(get_chat_history_service)]
token_validator_dependency = Annotated[TokenValidator, Depends(get_token_validator)]
file_service_dependency = Annotated[FileService, Depends(get_file_service)]

async def get_bot_service(request: Request, chat_service: chat_service_dependency, file_service: file_service_dependency) -> OpenAIChatService:

        SERPER_API_KEY = get_settings().SERPER_API_KEY
        web_service = WebService(SerperApiSearchEngine(api_key=SERPER_API_KEY), SerperResponseParser())
        weather_service = WeatherService()
        request_data = await request.json()

        chat_items = chat_service.get_chat_items(request_data.get('chat_id'))
        chat_messages = ChatItemsParser().parse_to_chat_messages(chat_items)

        memory = ChatMemoryBuffer.from_defaults(chat_history=chat_messages)
        
        files = file_service.get_user_files_by_ids(request_data.get('user_id'), request_data.get('selected_files_ids'))
        print(files)
        documents = []

        for file in files:
             documents.append(Document(text=file.text))

        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()

        document_reader_tool = QueryEngineTool.from_defaults(
             query_engine=query_engine,
             description="Useful for getting different information from user's documents"
        )

        web_search_tool = FunctionTool.from_defaults(
            web_service.provide_documents, description='Useful for getting current web data.'
        )
        weather_search_tool = FunctionTool.from_defaults(
            weather_service.get_city_weather_data, description='Useful for getting the data about current weather and air pollution in given location. Use all of the parameters in English translation.'
        )

        return OpenAIChatService(tools=[web_search_tool, weather_search_tool, document_reader_tool],memory=memory, bot_description=" \
        You are an AI assistant that answers user queries. \
        Always try answer the question with user's documents first. \
        If you cannot find relevant information in those documents, determine, \
        whether the query is about current events that need to include the current date. \
        If so,search for the current date and answer the user's query taking that date into account.\
        If the query is not about current events, answer the question without considering the date.")

bot_service_dependency = Annotated[OpenAIChatService, Depends(get_bot_service)]

def authorize(role: Optional[Role]) -> Callable:
        async def dependency(
                authorization: Annotated[str, Header()],
                role_service: role_service_dependency,
                token_validator: token_validator_dependency,
                user_service: user_service_dependency
                ) -> dict:
            
            if not authorization:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
            
            decoded_token = token_validator.validate_token(authorization)
            
            if role:
                external_user_id = decoded_token['sub']
                user = user_service.get_user_by_external_user_id(external_user_id) 

                try:
                    isAuthorized = role_service.autorize_role(user_id=user.id, role=role)
                    
                    if not isAuthorized:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Permission role restricted.')
                except HTTPException as http_exec:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=http_exec.detail)
                
            return decoded_token
            
        return dependency

authorize_no_role = authorize(role=None)
authorize_admin_role = authorize(role=Role.ADMIN)
authorize_user_role = authorize(role=Role.USER)

        