import { beforeEach, describe, test, expect } from '@jest/globals';
import { BotMessageData, BotMessageService } from '../services/BotMessageService';
import { StatusType } from '../enums/StatusType';
import { BOT_MOCK_ANSWER } from '../constants';


describe('botMessageService', () => {
  let botService: BotMessageService;

  beforeEach(() => {
    botService = new BotMessageService();
  })

  test('should create bot message data', () => {
    const expectedMessageData: BotMessageData = {
      status: StatusType.Pending,
      text: null,
      refetch: botService.simulateFetchResponse
    }

    const createdData = botService.createMessageData();
    expect(createdData).toEqual(expectedMessageData);
  })

  test('should resolve promise with string', async () => {
    const TEST_QUERY = 'Test query'

    await expect(botService.simulateFetchResponse(TEST_QUERY, false)).resolves.toEqual(BOT_MOCK_ANSWER)
  })

  test('should reject promise with string', async () => {
    const TEST_QUERY = 'Test query'

    await expect(botService.simulateFetchResponse(TEST_QUERY, true)).rejects.toEqual('Failed to get bot response')
  })
})


