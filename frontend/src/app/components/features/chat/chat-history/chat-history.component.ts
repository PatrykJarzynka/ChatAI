import { Component } from '@angular/core';
import { ChatHistoryService } from '../../../../../services/ChatHistoryService';
import { ChatService } from '../../../../../services/ChatService';
import useParser from '../../../../../composables/useParser';

import { MatButton } from '@angular/material/button';
import { MatDivider } from '@angular/material/divider';
import { AppTitlebar } from '../../../core/app-titlebar/app-titlebar.component';
import { MatIcon } from '@angular/material/icon';
import { ChatHistory as ChatHistoryType } from '../../../../../types/ChatHistory';
import { MatList, MatListItem, MatListItemIcon } from '@angular/material/list';


const { parseChatResponseToChat } = useParser;

@Component({
  selector: 'chat-history',
  imports: [
    MatButton,
    MatDivider,
    AppTitlebar,
    AppTitlebar,
    MatIcon,
    MatList,
    MatListItem,
    MatListItemIcon
  ],
  templateUrl: './chat-history.component.html',
  styleUrl: './chat-history.component.scss',
})
export class ChatHistory {

  protected readonly Array = Array;

  constructor(
    private chatHistoryService: ChatHistoryService,
    private chatService: ChatService
  ) {
  }

  mockHistories = new Map<number, ChatHistoryType>([[1, { id: 1, title: 'Test' }],
    [2, { id: 2, title: 'Test' }],
    [3, { id: 3, title: 'Test' }],
    [4, { id: 4, title: 'Test' }],
    [5, { id: 5, title: 'Test' }],
    [6, { id: 6, title: 'Test' }],
    [7, { id: 7, title: 'Test' }],
    [8, { id: 8, title: 'Test' }],
    [9, { id: 9, title: 'Test' }],
    [10, { id: 10, title: 'Test' }],
    [11, { id: 11, title: 'Test' }],
    [12, { id: 12, title: 'Test' }],
    [13, { id: 13, title: 'Test' }],
    [14, { id: 14, title: 'Test' }],
    [15, { id: 15, title: 'Test' }],
    [16, { id: 16, title: 'Test' }],
    [17, { id: 17, title: 'Test' }],
    [18, { id: 18, title: 'Test' }],]
  );


  // chatHistories = () => this.mockHistories.values();
  chatHistories = () => this.chatHistoryService.getAllChatHistories().values();
  selectedChatId = () => this.chatService.getCurrentChat()?.id;

  async ngOnInit() {
    const chatHistories = await this.chatHistoryService.fetchChatHistories();
    this.chatHistoryService.setChatHistories(chatHistories);
  }

  async updateCurrentChat(chatId: number) {
    if (this.chatService.getCurrentChat()?.id === chatId) {
      return;
    }

    const chatResponse = await this.chatService.fetchChatByChatId(chatId);

    const chat = parseChatResponseToChat(chatResponse);

    if (chat) {
      this.chatService.setCurrentChat(chat);
    }
  }
}
