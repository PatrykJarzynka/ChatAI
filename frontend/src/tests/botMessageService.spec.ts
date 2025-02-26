import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { BotMessageData, BotMessageService } from '@services/BotMessageService';
import { CHAT_ENDPOINT } from '../constants';
import { MOCK_USER, MOCK_USER_CHAT_DATA } from '@utils/mockedData';
import { ApiService } from '@services/ApiService';
import { UserService } from '@services/UserService';
import { StatusType } from '@enums/StatusType';
import { UserChatData } from 'appTypes/UserChatData';


jest.mock('@services/ApiService');

describe('botMessageService', () => {
  let apiServiceMock: jest.Mocked<ApiService>;
  let userService: UserService;
  let botService: BotMessageService;

  beforeEach(() => {
    apiServiceMock = new ApiService() as jest.Mocked<ApiService>;
    userService = new UserService(apiServiceMock);
    botService = new BotMessageService(apiServiceMock, userService);
  });

  describe('createMessageData', () => {
    test('should create message data', () => {
      const result = botService.createMessageData();
      const expected: BotMessageData = {
        status: StatusType.Pending,
        text: null
      };

      expect(result).toEqual(expected);
    });
  });

  describe('fetchBotResponse', () => {
    test('should fetch bot response', async () => {
      const RESPONSE = 'Test bot response';
      apiServiceMock.post.mockResolvedValue(RESPONSE);
      jest.spyOn(botService, 'createUserChatData').mockReturnValue(MOCK_USER_CHAT_DATA);

      const result = await botService.fetchBotResponse(MOCK_USER_CHAT_DATA.chatId, MOCK_USER_CHAT_DATA.message);

      expect(apiServiceMock.post).toBeCalledWith(CHAT_ENDPOINT, MOCK_USER_CHAT_DATA);
      expect(result).toEqual(RESPONSE);
    });
  });

  describe('createUserChatData', () => {
    test('should create user chat data with current user id', async () => {
      const result = botService.createUserChatData(MOCK_USER_CHAT_DATA.chatId, MOCK_USER_CHAT_DATA.message);

      const expected: UserChatData = {
        chatId: MOCK_USER_CHAT_DATA.chatId,
        message: MOCK_USER_CHAT_DATA.message
      };

      expect(result).toEqual(expected);
    });
  });
});


