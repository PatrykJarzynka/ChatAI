import { Injectable } from '@angular/core';
import { CHAT_ENDPOINT } from '../constants';
import { StatusType } from '@enums/StatusType';
import { ApiService } from '@services/ApiService';
import { UserChatData } from 'appTypes/UserChatData';
import { UserService } from '@services/UserService';


export interface BotMessageData {
  text: string | null;
  status: StatusType;
}

@Injectable({
  providedIn: 'root'
})
export class BotMessageService {

  constructor(
    private apiService: ApiService,
    private userService: UserService,
  ) {
  }

  createMessageData(): BotMessageData {
    return {
      status: StatusType.Pending,
      text: null,
    };
  }

  createUserChatData(chatId: number, userQuery: string): UserChatData {
    const user = this.userService.getCurrentUser();

    if (!user()) {
      throw new Error('User chat data cannot be created, because user is not initialized!');
    } else {
      return {
        userId: user()!.id,
        chatId,
        message: userQuery,
      };
    }
  }

  async fetchBotResponse(chatId: number, userQuery: string): Promise<string> {
    const userChatData = this.createUserChatData(chatId, userQuery);
    return await this.apiService.post<string, UserChatData>(CHAT_ENDPOINT, userChatData);
  }
}
