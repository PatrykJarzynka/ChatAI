from utilities.chat_items_parser import ChatItemsParser
from typing import List
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer

class MemoryBufferService():

    def __init__(self, chat_messages: List[ChatMessage] = None):
        if chat_messages:
            self.memory_buffer = ChatMemoryBuffer.from_defaults(chat_history=chat_messages)
        else:
            self.memory_buffer = ChatMemoryBuffer.from_defaults()
    
    def get_memory(self):
        return self.memory_buffer