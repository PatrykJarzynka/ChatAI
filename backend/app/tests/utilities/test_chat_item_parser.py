# import pytest
# from utilities.chat_items_parser import ChatItemsParser
# from tables.chat_item import ChatItem
# from llama_index.core.base.llms.types import ChatMessage

# @pytest.fixture
# def chat_items_parser():
#     return ChatItemsParser()


# def test_parse_to_chat_messages(chat_items_parser: ChatItemsParser):
#     mocked_chat_items = [ChatItem(user_message='Hello.', bot_message='Hello, how are you?'), 
#                          ChatItem(user_message='Hello2.', bot_message='Hello, how are you2?')]
    
#     expected_chat_messages = [ChatMessage(content='Hello.', role='user'),ChatMessage(content='Hello, how are you?', role='assistant'),
#                               ChatMessage(content='Hello2.', role='user'),ChatMessage(content='Hello, how are you2?', role='assistant'),]

#     chat_messages = chat_items_parser.parse_to_chat_messages(mocked_chat_items)

#     assert chat_messages == expected_chat_messages




