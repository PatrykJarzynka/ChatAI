from itertools import chain

from fastapi import HTTPException
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_hub.tools.google_search.base import GoogleSearchToolSpec
from llama_index.agent.openai import OpenAIAgent
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import SummaryIndex
from db_models.chat_item_model import ChatItem
from llama_index.core.tools import FunctionTool
import os

Settings.llm = OpenAI(temperature=0.2, model="gpt-4o")


class BotService:

    @staticmethod
    def prepare_chat_memory(chat_items: list[ChatItem]) -> list[ChatMessage]:
        def convert_chat_item_to_chat_messages(item: ChatItem) -> list[ChatMessage]:
            return [
                ChatMessage(content=f"{item.user_message}", role='user'),
                ChatMessage(content=f"{item.bot_message}", role='assistant')
            ]

        return list(chain.from_iterable(map(convert_chat_item_to_chat_messages, chat_items)))

    def fetch_bot_response(self, userQuery: str, chat_items: list[ChatItem]) -> str:
        GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
        GOOGLE_ENGINE_KEY = os.getenv('GOOGLE_ENGINE_KEY')

        try:
            memory = ChatMemoryBuffer.from_defaults(chat_history=self.prepare_chat_memory(chat_items))

            google_search_tool = GoogleSearchToolSpec(key=GOOGLE_SEARCH_API_KEY, engine=GOOGLE_ENGINE_KEY)
            
            chat_agent = OpenAIAgent.from_tools(google_search_tool.to_tool_list(), memory=memory, llm=Settings.llm, verbose=True)
            
            response = chat_agent.chat(userQuery)
        
            return response.response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch bot response: {e}")
