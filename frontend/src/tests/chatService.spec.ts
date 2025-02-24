import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ChatService } from '@services/ChatService';
import { UserService } from '@services/UserService';
import { ApiService } from '@services/ApiService';
import { StatusType } from '@enums/StatusType';
import { BotMessageData, BotMessageService } from '@services/BotMessageService';
import { ChatHistoryService } from '@services/ChatHistoryService';
import {
  MOCK_CHAT_ID,
  MOCK_CHAT_ITEM,
  MOCK_CHAT_WITH_ITEMS,
  MOCK_ERROR,
  MOCK_QUERY,
  MOCKED_BOT_MESSAGE_DATA,
  MOCKED_CHAT_RESPONSE,
  MOCKED_INITIAL_CHAT,
} from '@utils/mockedData';
import { ChatItem } from 'appTypes/ChatItem';
import { CHAT_ENDPOINT } from '../constants';


jest.mock('@services/ApiService');

describe('chatService', () => {
  let apiServiceMock: jest.Mocked<ApiService>;
  let chatService: ChatService;
  let botMessageService: BotMessageService;
  let userService: UserService;
  let chatHistoryService: ChatHistoryService;

  beforeEach(() => {
    apiServiceMock = new ApiService() as jest.Mocked<ApiService>;
    userService = new UserService(apiServiceMock);
    chatHistoryService = new ChatHistoryService(apiServiceMock);
    botMessageService = new BotMessageService(apiServiceMock, userService);

    chatService = new ChatService(botMessageService, chatHistoryService, apiServiceMock);
  });

  describe('startNewChat', () => {
    test('should fetch a new chat and set it as current', async () => {
      jest.spyOn(chatService, 'fetchNewChat').mockReturnValue(Promise.resolve(MOCKED_INITIAL_CHAT));
      jest.spyOn(chatService, 'setCurrentChat');

      await chatService.startNewChat();

      expect(chatService.fetchNewChat).toHaveBeenCalledTimes(1);
      expect(chatService.setCurrentChat).toHaveBeenCalledWith(MOCKED_INITIAL_CHAT);
    });

    test('should log an error if fetchNewChat fails', async () => {
      jest.spyOn(chatService, 'fetchNewChat').mockReturnValue(Promise.reject(MOCK_ERROR));
      jest.spyOn(chatService, 'setCurrentChat');

      await chatService.startNewChat();

      await expect(chatService.fetchNewChat).rejects.toEqual(MOCK_ERROR);
      expect(chatService.setCurrentChat).not.toHaveBeenCalled();
    });
  });

  describe('fetchNewChat', () => {
    test('should fetch a new chat from API', async () => {
      apiServiceMock.get.mockResolvedValue(MOCKED_INITIAL_CHAT);

      const result = await chatService.fetchNewChat();

      expect(result).toEqual(MOCKED_INITIAL_CHAT);
      expect(apiServiceMock.get).toHaveBeenCalled();
    });
  });

  describe('fetchChatByChatId', () => {
    test('should fetch chat by chat id', async () => {
      apiServiceMock.get.mockResolvedValue(MOCKED_CHAT_RESPONSE);

      const result = await chatService.fetchChatByChatId(MOCK_CHAT_ID);

      expect(result).toEqual(MOCKED_CHAT_RESPONSE);
      expect(apiServiceMock.get).toHaveBeenCalledWith(`${ CHAT_ENDPOINT }/${ MOCK_CHAT_ID }`);
    });
  });

  describe('createChatItemTemplate', () => {
    test('should create chat item template', () => {
      jest.spyOn(botMessageService, 'createMessageData').mockReturnValue(MOCKED_BOT_MESSAGE_DATA);

      const expected: ChatItem = {
        userMessage: MOCK_QUERY,
        botMessageData: MOCKED_BOT_MESSAGE_DATA,
      };

      const result = chatService.createChatItemTemplate(MOCK_QUERY);
      expect(result).toEqual(expected);
    });
  });

  describe('addChatItem', () => {
    test('should add a new chat item when currentChat is defined', () => {
      chatService.setCurrentChat(MOCKED_INITIAL_CHAT);

      chatService.addChatItem(MOCK_CHAT_ITEM);
      const currentChat = chatService.getCurrentChat();

      expect(currentChat?.chatItems.length).toBe(1);
      expect(currentChat?.chatItems[0]).toEqual(MOCK_CHAT_ITEM);
    });

    test('should throw an error when currentChat is not defined', () => {
      const currentChat = chatService.getCurrentChat();

      expect(currentChat).toEqual(null);
      expect(() => chatService.addChatItem(MOCK_CHAT_ITEM)).toThrowError('Chat is not defined!');
    });
  });

  describe('updateLatestBotMessageDataProperty', () => {
    test('should update latest bot message text and status', () => {
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      const expectedStatus = StatusType.Failed;
      const expectedText = 'Updated text!';

      const updatePropertyTest = <T extends keyof BotMessageData>(property: T, value: BotMessageData[T]) => {
        chatService.updateLatestBotMessageDataProperty(property, value);
        let updatedChat = chatService.getCurrentChat();
        const lastItemInChat = updatedChat?.chatItems.at(-1);

        expect(lastItemInChat).toBeDefined();
        expect(lastItemInChat?.botMessageData[property]).toEqual(value);
      };

      updatePropertyTest('status', expectedStatus);
      updatePropertyTest('text', expectedText);
    });

    test('should throw error on update bot message property when chat is not defined', () => {
      const expectedStatus = StatusType.Failed;

      expect(() => chatService.updateLatestBotMessageDataProperty('status', expectedStatus)).toThrowError('Chat is not defined!');
    });
  });

  describe('createAndAddChatItem', () => {
    test('should create and add a chat item template to chat', () => {
      jest.spyOn(chatService, 'createChatItemTemplate').mockReturnValue(MOCK_CHAT_ITEM);
      jest.spyOn(chatService, 'addChatItem');

      chatService.setCurrentChat(MOCKED_INITIAL_CHAT);

      chatService.createAndAddChatItemTemplate(MOCK_QUERY);

      expect(chatService.createChatItemTemplate).toHaveBeenCalledWith(MOCK_QUERY);
      expect(chatService.addChatItem).toHaveBeenCalledWith(MOCK_CHAT_ITEM);

      const currentChat = chatService.getCurrentChat();

      expect(currentChat?.chatItems).toContainEqual(MOCK_CHAT_ITEM);
    });
  });

  describe('updateChatHistory', () => {
    test('should update chat history', () => {
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      const currentChat = chatService.getCurrentChat();

      chatService.updateChatHistory();

      const selectedChatHistory = chatHistoryService.getChatHistoryByChatId(MOCK_CHAT_WITH_ITEMS.id);

      expect(currentChat).toBeDefined();
      expect(selectedChatHistory).toBeDefined();
      expect(selectedChatHistory).toEqual({ id: currentChat?.id, title: currentChat?.chatItems[0].userMessage });
    });
  });
});


