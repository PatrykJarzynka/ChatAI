import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ChatHistoryService } from '@services/ChatHistoryService';
import { MOCK_CHAT_HISTORY, MOCK_CHAT_WITH_ITEMS, MOCK_USER } from '@utils/mockedData';
import { ApiService } from '@services/ApiService';
import { CHAT_ENDPOINT } from '../constants';
import useParser from '@composables/useParser';
import { ChatHistory } from '@appTypes/ChatHistory';


jest.mock('@services/ApiService');
const { parseArrayOfObjectsIntoMap } = useParser;

describe('chatHistoryService', () => {
  let apiServiceMock: jest.Mocked<ApiService>;
  let chatHistoryService: ChatHistoryService;

  beforeEach(() => {
    apiServiceMock = new ApiService() as jest.Mocked<ApiService>;
    chatHistoryService = new ChatHistoryService(apiServiceMock);
  });

  describe('fetchChatHistories', () => {
    test('should fetch chat histories', async () => {
      apiServiceMock.get.mockResolvedValue(Promise.resolve([MOCK_CHAT_HISTORY]));

      const result = await chatHistoryService.fetchUserChatHistory(MOCK_USER.id);

      expect(apiServiceMock.get).toHaveBeenCalledWith(`${ CHAT_ENDPOINT }/history?userId=${ MOCK_USER.id }`);
      expect(result).toEqual([MOCK_CHAT_HISTORY]);
    });
  });

  describe('getChatHistoryByChatId', () => {
    test('should return chat history by id', () => {
      chatHistoryService.setChatHistories([MOCK_CHAT_HISTORY]);

      const foundChatHistory = chatHistoryService.getChatHistoryByChatId(MOCK_CHAT_HISTORY.id);
      expect(foundChatHistory).toEqual(MOCK_CHAT_HISTORY);
    });

    test('should return error when no chat is found', () => {
      expect(() => chatHistoryService.getChatHistoryByChatId(MOCK_CHAT_HISTORY.id)).toThrowError('No chat history found.');
    });
  });

  describe('setChatHistories', () => {
    test('should convert chat histories array into map of chat histories and set in state', () => {
      chatHistoryService.setChatHistories([MOCK_CHAT_HISTORY]);

      const chatHistories = chatHistoryService.getAllChatHistories();

      expect(chatHistories).toEqual(parseArrayOfObjectsIntoMap([MOCK_CHAT_HISTORY], 'id'));
    });
  });

  describe('createChatHistory', () => {
    test('should convert chat into chat history', () => {
      const result = chatHistoryService.createChatHistory(MOCK_CHAT_WITH_ITEMS);
      const expected: ChatHistory = {
        id: MOCK_CHAT_WITH_ITEMS.id,
        title: MOCK_CHAT_WITH_ITEMS.chatItems[0].userMessage
      };

      expect(result).toEqual(expected);
    });
  });

  describe('clearChatHistory', () => {
    test('should clear the chat history', async () => {
      chatHistoryService.setChatHistories([MOCK_CHAT_HISTORY]);
      chatHistoryService.clearChatHistory();

      const currentChatHistories = chatHistoryService.getAllChatHistories();

      expect(currentChatHistories.size).toEqual(0);
    });
  });
});
