from db_models.chat_item_model import ChatItem
from llama_index.core.base.llms.types import ChatMessage
from typing import List
from itertools import chain

class ChatItemsParser:

    def parse_to_chat_messages(self, chat_items: List[ChatItem]) -> List[ChatMessage]:
        def convert_chat_item_to_chat_messages(item: ChatItem) -> list[ChatMessage]:
            return [
                ChatMessage(content=f"{item.user_message}", role='user'),
                ChatMessage(content=f"{item.bot_message}", role='assistant')
            ]
        return list(chain.from_iterable(map(convert_chat_item_to_chat_messages, chat_items)))