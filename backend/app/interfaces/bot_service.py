from abc import ABC, abstractmethod
from typing import List
from llama_index.core.tools import FunctionTool
from llama_index.core.memory import ChatMemoryBuffer

class BotService(ABC):

    @abstractmethod
    def __init__(self, tools: List["FunctionTool"], bot_description: str, memory: "ChatMemoryBuffer"):
        pass

    @abstractmethod
    def chat(self, user_query:str):
        pass