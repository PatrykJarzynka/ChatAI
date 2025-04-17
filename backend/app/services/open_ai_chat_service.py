from fastapi import HTTPException
from llama_index.core import Settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from db_models.chat_item_model import ChatItem
from llama_index.core.tools import FunctionTool
from typing import List
from interfaces.bot_service import BotService


class OpenAIChatService(BotService):

    def __init__(self, tools: List["FunctionTool"], bot_description: str, memory: ChatMemoryBuffer):
        self.chat_agent = OpenAIAgent.from_tools(
            tools,
            memory=memory,
            llm=OpenAI(temperature=0.2, model="gpt-4o-mini"),
            system_prompt=(bot_description),
            verbose=True
        )

    def chat(self, user_query: str) -> str:
        try: 
            data = self.chat_agent.chat(user_query)

            return data.response
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch bot response: {e}")
