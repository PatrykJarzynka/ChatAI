import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ApiService } from '../services/ApiService';
import { UserService } from '../services/UserService';
import { ChatHistoryService } from '../services/ChatHistoryService';
import { BotMessageService } from '../services/BotMessageService';
import { ChatService } from '../services/ChatService';
import useChatActions from '../composables/useChatActions';
import { MOCK_CHAT_WITH_ITEMS, MOCK_QUERY } from '../utils/mockedData';
import { StatusType } from '../enums/StatusType';


describe('useChatActions', () => {
  let apiServiceMock: jest.Mocked<ApiService>;
  let chatService: ChatService;
  let botMessageService: BotMessageService;
  let userService: UserService;
  let chatHistoryService: ChatHistoryService;
  let handleFetchingBotMessageFn: (userQuery: string, shouldFail: boolean) => Promise<void>;

  beforeEach(() => {
    apiServiceMock = new ApiService() as jest.Mocked<ApiService>;
    userService = new UserService();
    chatHistoryService = new ChatHistoryService(apiServiceMock);
    botMessageService = new BotMessageService(apiServiceMock, userService);

    chatService = new ChatService(botMessageService, chatHistoryService, apiServiceMock);
    const { handleFetchingBotMessage } = useChatActions(chatService);
    handleFetchingBotMessageFn = handleFetchingBotMessage;
  });

  describe('handleFetchingBotMessage', () => {
    test('should throw error if chat is not defined', () => {
      expect(() => handleFetchingBotMessageFn(MOCK_QUERY, false)).rejects.toThrowError('Chat is not defined!');
    });

    test('should update bot message status to failed', async () => {
      jest.spyOn(chatService, 'fetchBotResponse').mockRejectedValue(new Error('Failed to fetch bot message'));
      jest.spyOn(chatService, 'updateLatestBotMessageDataProperty');
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      await handleFetchingBotMessageFn(MOCK_QUERY,false);

      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledWith('status', StatusType.Failed);
      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledTimes(1);
    });

    test('should update bot message status to failed when bot fail state is enabled', async () => {
      jest.spyOn(chatService, 'fetchBotResponse')
      jest.spyOn(chatService, 'updateLatestBotMessageDataProperty');
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      await handleFetchingBotMessageFn(MOCK_QUERY,true);

      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledWith('status', StatusType.Failed);
      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledTimes(1);
    });

    test('should update bot message to success and update chat history', async () => {
      const botResponse = 'Hello World!';
      const shouldFail = false
      jest.spyOn(chatService, 'fetchBotResponse').mockResolvedValue(botResponse);
      jest.spyOn(chatService, 'updateLatestBotMessageDataProperty');
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      await handleFetchingBotMessageFn(MOCK_QUERY, shouldFail);

      const chatHistories = chatHistoryService.getAllChatHistories();

      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledTimes(2);
      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledWith('status', StatusType.Success);
      expect(chatService.updateLatestBotMessageDataProperty).toBeCalledWith('text', botResponse);
      expect(!!chatHistories.get(MOCK_CHAT_WITH_ITEMS.id)).toBe(true);
    });
  });
});
