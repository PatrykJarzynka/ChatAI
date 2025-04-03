from itertools import chain

from fastapi import HTTPException
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import SummaryIndex
from db_models.chat_item_model import ChatItem
from llama_index.core.tools import FunctionTool
import os
import requests
from llama_index.core import Document


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
        SERPER_API_KEY = os.getenv('SERPER_API_KEY')

        def search_web(query: str):
            request_data = {
                "q": query,
                "gl": "pl",
            }

            search_results = requests.post(
                "https://google.serper.dev/search",
                json=request_data,
                headers={"X-API-KEY": SERPER_API_KEY},
            )
            
            data = search_results.json()

            if "answerBox" in data:
                return data["answerBox"].get("answer", "Nie znaleziono bezpośredniej odpowiedzi.")

            documents = [Document(text=item["snippet"], metadata={"url": item["link"]}) for item in data["organic"]]
            
            return documents
        
        search_web_tool = FunctionTool.from_defaults(
            search_web
        )

        try:
            memory = ChatMemoryBuffer.from_defaults(chat_history=self.prepare_chat_memory(chat_items))
            
            chat_agent = OpenAIAgent.from_tools(
                [search_web_tool], 
                memory=memory, 
                llm=Settings.llm, 
                verbose=True,
                system_prompt="""
                You are an intelligent assistant. If there is a question about time or latest events, 
                you need to use search_web_tool to retrieve the latest information.
                Never give outdated answers if there is an opportunity to get fresh data.
                """)
            
            response = chat_agent.chat(userQuery)
            return response
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch bot response: {e}")
