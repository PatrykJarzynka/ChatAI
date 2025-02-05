import { Chat } from '../types/Chat';
import { BotMessageData } from '../services/BotMessageService';
import { StatusType } from '../enums/StatusType';
import { ChatItem } from '../types/ChatItem';
import { ChatResponse } from '../models/ChatResponse';
import { ChatHistory } from '../types/ChatHistory';
import { UserChatData } from '../types/UserChatData';


const MOCK_USER_ID = 'testUserId';
const MOCK_CHAT_ID = 123;
const MOCK_QUERY = 'mockQuery';

const MOCKED_INITIAL_CHAT: Chat = {
  chatItems: [],
  id: MOCK_CHAT_ID,
};

const MOCKED_CHAT_RESPONSE: ChatResponse = {
  id: MOCK_CHAT_ID,
  chatItems: [
    {
      userMessage: 'Test user text',
      botMessage: 'Test bot text'
    }
  ]
};

const MOCKED_BOT_MESSAGE_DATA: BotMessageData = {
  status: StatusType.Pending,
  text: null
};

const MOCK_CHAT_ITEM: ChatItem = {
  userMessage: MOCK_QUERY,
  botMessageData: MOCKED_BOT_MESSAGE_DATA
};

const MOCK_CHAT_WITH_ITEMS: Chat = {
  ...MOCKED_INITIAL_CHAT,
  chatItems: [MOCK_CHAT_ITEM]
};

const MOCK_CHAT_HISTORY: ChatHistory = {
  id: MOCK_CHAT_WITH_ITEMS.id,
  title: MOCK_CHAT_WITH_ITEMS.chatItems[0].userMessage
};

const MOCK_USER_CHAT_DATA: UserChatData = {
  userId: MOCK_USER_ID,
  chatId: MOCK_CHAT_ID,
  message: MOCK_QUERY
};

const MOCK_ERROR = 'Network Error';

export {
  MOCK_CHAT_ID,
  MOCK_QUERY,
  MOCKED_BOT_MESSAGE_DATA,
  MOCK_CHAT_ITEM,
  MOCK_CHAT_WITH_ITEMS,
  MOCKED_INITIAL_CHAT,
  MOCK_ERROR,
  MOCKED_CHAT_RESPONSE,
  MOCK_CHAT_HISTORY,
  MOCK_USER_CHAT_DATA
};
