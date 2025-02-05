import { Injectable, signal } from '@angular/core';
import { Chat } from '../types/Chat';

@Injectable({
  providedIn: 'root'
})
export class ChatHistoryService {
  private chatHistoriesMap = signal<Map<string, Chat>>(new Map());

  constructor() {}

  getAllChatHistories(): Map<string, Chat> {
    return this.chatHistoriesMap();
  }

  getChatHistoryByChatId(chatId: string) {
    if (this.chatHistoriesMap().has(chatId)) {
      return this.chatHistoriesMap().get(chatId);
    } else {
      throw new Error('No chat history found.');
    }
  }

  setChatHistoryMapItem(chatReference: Chat) {
    this.chatHistoriesMap().set(chatReference.id, chatReference);
  }

  updateChatHistory(chat: Chat) {
    try {
      const chatHistory = this.getChatHistoryByChatId(chat.id);
      if (chatHistory) {
        this.setChatHistoryMapItem(chat)
      }
    } catch (error) {
      console.error(error);
    }
  }
}
