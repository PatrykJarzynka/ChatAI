import { Injectable, signal } from '@angular/core';
import { BotMessageData, BotMessageService } from '../services/BotMessageService';
import { ChatHistoryService } from '../services/ChatHistoryService';
import { Chat } from '../types/Chat';
import { ChatItem } from '../types/ChatItem';
import { ApiService } from '../services/ApiService';
import { ChatResponse } from '../models/ChatResponse';
import { CHAT_ENDPOINT } from '../constants';


@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private currentChat = signal<Chat | null>(null);

  constructor(
    private botMessageService: BotMessageService,
    private chatHistoryService: ChatHistoryService,
    private apiService: ApiService
  ) {
  }

  async startNewChat() {
    try {
      const newChat = await this.fetchNewChat();
      this.setCurrentChat(newChat);
    } catch (e) {
      console.error(e);
    }
  }

  async fetchNewChat(): Promise<Chat> {
    return await this.apiService.get<Chat>(CHAT_ENDPOINT);
  }

  async fetchChatByChatId(chatId: number) {
    try {
      return await this.apiService.get<ChatResponse>(`${ CHAT_ENDPOINT }/${ chatId }`);
    } catch (e) {
      console.error(e);
      return;
    }
  }

  createChatItemTemplate(userQuery: string): ChatItem {
    return {
      userMessage: userQuery,
      botMessageData: this.botMessageService.createMessageData(),
    };
  }

  addChatItem(chatItem: ChatItem) {
    const currentChat = this.currentChat();

    if (!currentChat) {
      throw new Error('Chat is not defined!');
    } else {
      this.currentChat.set({
        ...currentChat,
        chatItems: [...currentChat.chatItems, chatItem]
      });
    }
  }

  updateLatestBotMessageDataProperty<T extends keyof BotMessageData>(property: T, value: BotMessageData[T]): void {
    this.currentChat.update(chat => {
      if (chat) {
        return {
          ...chat,
          chatItems: chat.chatItems.map((chatItem, chatItemIndex) =>
            chatItemIndex === chat.chatItems.length - 1
              ? {
                ...chatItem,
                botMessageData: {
                  ...chatItem.botMessageData,
                  [property]: value
                }
              }
              : chatItem
          )
        };
      } else {
        throw new Error('Chat is not defined!');
      }
    });
  }

  createAndAddChatItemTemplate(userQuery: string): void {
    const chatItemTemplate = this.createChatItemTemplate(userQuery);
    this.addChatItem(chatItemTemplate);
  }

  async fetchBotResponse(userQuery: string, chatId: number, shouldFail: boolean): Promise<string | null> {
    if (shouldFail) {
      return new Promise((resolve, reject) => {
        reject('Unknown error');
      });
    }

    return await this.botMessageService.fetchBotResponse(chatId, userQuery);
  }

  getCurrentChat(): Chat | null {
    return this.currentChat();
  }

  setCurrentChat(chat: Chat) {
    this.currentChat.set(chat);
  }

  updateChatHistory() {
    const currentChat = this.getCurrentChat();

    if (currentChat) {
      const chatHistory = this.chatHistoryService.createChatHistory(currentChat);
      this.chatHistoryService.updateChatHistory(chatHistory);
    }
  }
}
