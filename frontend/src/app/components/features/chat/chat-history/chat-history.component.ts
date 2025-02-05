import { Component } from '@angular/core';
import { ChatHistoryService } from '../../../../../services/ChatHistoryService';
import { ChatService } from '../../../../../services/ChatService';
import useParser from '../../../../../composables/useParser';


const { parseChatResponseToChat } = useParser();

@Component({
  selector: 'chat-history',
  imports: [],
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

  chatHistories = () => this.chatHistoryService.getAllChatHistories().values();

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
