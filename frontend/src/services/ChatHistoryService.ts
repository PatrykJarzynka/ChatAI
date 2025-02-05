import { Injectable, signal } from '@angular/core';
import { ChatHistory } from '../types/ChatHistory';
import { ApiService } from '../services/ApiService';
import { Chat } from '../types/Chat';
import { CHAT_ENDPOINT } from '../constants';
import useParser from '../composables/useParser';


const { parseArrayOfObjectsIntoMap } = useParser();

@Injectable({
  providedIn: 'root'
})
export class ChatHistoryService {
  private chatHistoriesMap = signal<Map<number, ChatHistory>>(new Map());

  constructor(
    private apiService: ApiService,
  ) {
  }

  async fetchChatHistories() {
    return await this.apiService.get<ChatHistory[]>(`${ CHAT_ENDPOINT }/history`);
  }

  getAllChatHistories(): Map<number, ChatHistory> {
    return this.chatHistoriesMap();
  }

  getChatHistoryByChatId(chatId: number) {
    if (this.chatHistoriesMap().has(chatId)) {
      return this.chatHistoriesMap().get(chatId);
    } else {
      throw new Error('No chat history found.');
    }
  }

  setChatHistories(chatHistories: ChatHistory[]) {
    const chatHistoriesMap = parseArrayOfObjectsIntoMap(chatHistories, 'id');
    this.chatHistoriesMap.set(chatHistoriesMap);
  }

  setChatHistoryMapItem(chatHistory: ChatHistory) {
    this.chatHistoriesMap().set(chatHistory.id, chatHistory);
  }

  updateChatHistory(chatHistory: ChatHistory) {
    this.setChatHistoryMapItem(chatHistory);
  }

  createChatHistory(chat: Chat): ChatHistory {
    return {
      id: chat.id,
      title: chat.chatItems[0].userMessage
    };
  }
}
