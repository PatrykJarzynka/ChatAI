import { beforeEach, describe, test, expect } from '@jest/globals';
import { ChatHistoryService } from '../services/ChatHistoryService';
import { Chat } from '../types/Chat';
import { ChatItem } from '../types/ChatItem';
import { StatusType } from '../enums/StatusType';

const MOCK_CHAT_ID = 'mockChatId';
const MOCK_CHAT_ITEM_ID = 'mockChatItemId';

const MOCK_CHAT: Chat = {
  id: MOCK_CHAT_ID,
  chatItems: []
}

const MOCK_CHAT_ITEM: ChatItem = {
  id: MOCK_CHAT_ITEM_ID,
  botMessageData: {
    text: 'testBotText',
    refetch: () => new Promise<string>(resolve => resolve('test')),
    status: StatusType.Success
  },
  userMessageData: {
    userId: 'testUserId',
    text: 'testUserText',
  }
}

const MOCK_CHAT_WITH_ITEMS: Chat = {
  ...MOCK_CHAT,
  chatItems: [MOCK_CHAT_ITEM]
}

describe('chatHistoryService', () => {
  let chatHistoryService: ChatHistoryService;

  beforeEach(() => {
    chatHistoryService = new ChatHistoryService();
  })

  test('should add chat history to the list', () => {
    const allChatHistories = chatHistoryService.getAllChatHistories();

    expect([...allChatHistories.values()]).toEqual([]);

    chatHistoryService.setChatHistoryMapItem(MOCK_CHAT_WITH_ITEMS);

    const updatedChatHistories = chatHistoryService.getAllChatHistories();

    expect(updatedChatHistories.get(MOCK_CHAT_ID)).toEqual(MOCK_CHAT_WITH_ITEMS);
  })

  test('should update chat history item', () => {
    chatHistoryService.setChatHistoryMapItem(MOCK_CHAT_WITH_ITEMS);

    const allChatHistories = chatHistoryService.getAllChatHistories();

    expect([...allChatHistories.values()]).toEqual([MOCK_CHAT_WITH_ITEMS]);

    const mockChatUpdated: Chat = {
      ...MOCK_CHAT_WITH_ITEMS,
      chatItems: [
        ...MOCK_CHAT_WITH_ITEMS.chatItems,
        {
          id: 'Test id',
          userMessageData: {
            userId: 'Test user id',
            text: 'Test user text'
          },
          botMessageData: {
            text: 'Test bot text',
            refetch: () => new Promise<string>(resolve => resolve('test')),
            status: StatusType.Success
          }
        }
      ]
    }

    chatHistoryService.updateChatHistory(mockChatUpdated);

    const updatedChatHistories = chatHistoryService.getAllChatHistories();

    expect(updatedChatHistories.get(MOCK_CHAT_ID)?.chatItems).toEqual(mockChatUpdated.chatItems);
  })

  test('should return chat history by chat id', () =>{
    chatHistoryService.setChatHistoryMapItem(MOCK_CHAT_WITH_ITEMS);

    const chatHistory = chatHistoryService.getChatHistoryByChatId(MOCK_CHAT_ID);

    expect(chatHistory).toBeDefined();
    expect(chatHistory).toEqual(MOCK_CHAT_WITH_ITEMS);
  })

  test('should throw error on getting chat history by chat id', () =>{
    chatHistoryService.setChatHistoryMapItem(MOCK_CHAT_WITH_ITEMS);

    const mockId = 'New test id';

    expect(() => chatHistoryService.getChatHistoryByChatId(mockId)).toThrowError('No chat history found.');
  })
})
