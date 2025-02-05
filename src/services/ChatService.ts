import { Injectable, signal } from '@angular/core';
import { BotMessageData, BotMessageService } from '../services/BotMessageService';
import { StatusType } from '../enums/StatusType';
import { ChatHistoryService } from '../services/ChatHistoryService';
import { Chat } from '../types/Chat';
import { ChatItem } from '../types/ChatItem';
import { UserMessageService } from '../services/UserMessageService';
import { v4 as uuidv4 } from 'uuid';


@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private currentChat = signal<Chat | null>(null);

  constructor(
    private botMessageService: BotMessageService,
    private chatHistoryService: ChatHistoryService,
    private userMessageService: UserMessageService,
  ) {}

  startNewChat() {
    const newChat: Chat = {
      id: uuidv4(),
      chatItems: []
    }

    this.currentChat.set(newChat);
    this.chatHistoryService.setChatHistoryMapItem(newChat);
  }

  createChatItem(userQuery: string): ChatItem {
    return {
      id: uuidv4(),
      userMessageData: this.userMessageService.createMessageData(userQuery),
      botMessageData: this.botMessageService.createMessageData(),
    }
  }

  addChatItem(chatItem: ChatItem) {
    this.currentChat.update(chat => {
      if (chat) {
        return { ...chat, chatItems: [...chat.chatItems, chatItem] };
      } else {
        throw new Error('Chat is not defined!')
      }
    })
  }

  updateBotMessageDataProperty<T extends keyof BotMessageData>(property: T, value: BotMessageData[T], chatItemId: string): void {
    this.currentChat.update(chat => {
      if (chat) {
        const chatItemExist = chat.chatItems.find((chatItem) => chatItem.id === chatItemId);

        if (!chatItemExist) {
          throw new Error('Chat item with the specified id was not found in the list.');
        }

        return {
          ...chat,
          chatItems: chat.chatItems.map(chatItem =>
            chatItem.id === chatItemId ? {
              ...chatItem,
              botMessageData: {
                ...chatItem.botMessageData,
                [property]: value
              }
            } : chatItem
          )
        }
      } else {
        throw new Error('Chat is not defined!')
      }
    })
  }

  createAndAddChatItem(userQuery: string): ChatItem | null {
    try {
      const chatItem = this.createChatItem(userQuery);
      this.addChatItem(chatItem);
      this.updateChatHistory()
      return chatItem;
    } catch (error) {
      console.error(error)
      return null;
    }
  }

  async fetchBotResponse(userQuery: string, shouldFail: boolean): Promise<string | null> {
    try {
      return await this.botMessageService.simulateFetchResponse(userQuery, shouldFail);
    } catch (fetchError) {
      console.error(fetchError);
      return null;
    }
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
      this.chatHistoryService.updateChatHistory(currentChat)
    }
  }
}
