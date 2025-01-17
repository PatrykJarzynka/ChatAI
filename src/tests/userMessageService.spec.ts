import { beforeEach, describe, test, expect } from '@jest/globals';
import { UserMessageData, UserMessageService } from '../services/UserMessageService';
import { UserService } from '../services/UserService';

describe ('userMessageService', () => {
  let userService: UserService;
  let userMessageService: UserMessageService;

  beforeEach(() => {
    userService = new UserService();
    userMessageService = new UserMessageService(userService);
  })

  test('should create user message data', () => {
    const USER_QUERY = 'Test query'

    const expected: UserMessageData = {
      userId: userService.getUserId(),
      text: USER_QUERY,
    }

    const createdData = userMessageService.createMessageData(USER_QUERY);
    expect(createdData).toEqual(expected);
  })
});
