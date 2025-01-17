import { Injectable } from '@angular/core';
import { BOT_MOCK_ANSWER, MOCK_MESSAGE_DELAY } from '../constants';
import { StatusType } from '../enums/StatusType';
import { test } from '@jest/globals';
export interface BotMessageData {
  text: string | null;
  status: StatusType;
  refetch: (userQuery: string, shouldFail: boolean) => Promise<string>
}

@Injectable({
  providedIn: 'root'
})
export class BotMessageService {

  mockMessage = BOT_MOCK_ANSWER;
  constructor() {}

  createMessageData(): BotMessageData {
    return {
      status: StatusType.Pending,
      text: null,
      refetch: this.simulateFetchResponse
    }
  }

  async simulateFetchResponse(userQuery: string, shouldFail: boolean): Promise<string> { //userQuery will be needed when backend is connected
    return new Promise((resolve,reject) => {
      setTimeout(() => {
        if (shouldFail) {
          reject('Failed to get bot response');
        } else {
          resolve(this.mockMessage);
        }
      }, MOCK_MESSAGE_DELAY)
    })
  }
}
