from itertools import chain

from fastapi import HTTPException
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI

from db_models.chat_item_model import ChatItem

Settings.llm = OpenAI(temperature=0.2, model="gpt-4")


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
        try:
            memory = ChatMemoryBuffer.from_defaults(chat_history=self.prepare_chat_memory(chat_items))

            chat_engine = SimpleChatEngine.from_defaults(
                memory=memory,
                llm=Settings.llm
            )

            response = chat_engine.chat(userQuery)
            return response.response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch bot response: {e}")
