import { Component, model } from '@angular/core';
import { ChatWindow } from '../../features/chat/chat-window/chat-window.component';
import { ChatActions } from '../../features/chat/chat-actions/chat-actions.component';
import { MatIcon } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';
import { MatCheckbox } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { MatSidenavModule } from '@angular/material/sidenav';
import { AppSidebar } from '../../core/app-sidebar/app-sidebar.component';
import { NgStyle } from '@angular/common';
import { MatButton, MatMiniFabButton } from '@angular/material/button';
import { ChatHistory } from '../../features/chat/chat-history/chat-history.component';
import { ChatService } from '../../../../services/ChatService';
import useChatActions from '../../../../composables/useChatActions';
import { StatusType } from '../../../../enums/StatusType';


@Component({
  selector: 'chat-view',
  imports: [ChatWindow, ChatActions, MatIcon, MatTooltip, MatCheckbox, FormsModule, MatSidenavModule, AppSidebar, NgStyle, MatButton, ChatHistory, MatMiniFabButton,],
  templateUrl: './chat-view.component.html',
  styleUrl: './chat-view.component.scss'
})
export class ChatView {
  title = 'chatAI';
  panelVisibility = model<boolean>(true);
  shouldFail = model<boolean>(false);

  private readonly handleFetchingBotMessage: (userQuery: string, shouldFail: boolean) => Promise<void>;

  constructor(private chatService: ChatService) {
    const { handleFetchingBotMessage } = useChatActions(this.chatService);
    this.handleFetchingBotMessage = handleFetchingBotMessage;
  }

  async startNewChat() {
    const currentChat = this.chatService.getCurrentChat();
    if (currentChat?.chatItems.length) {
      await this.chatService.startNewChat();
    }
  }

  async onUserQuerySend(userQuery: string) {
    if (!this.chatService.getCurrentChat()) {
      await this.chatService.startNewChat();
    }

    this.chatService.createAndAddChatItemTemplate(userQuery);
    await this.handleFetchingBotMessage(userQuery, this.shouldFail());
  }

  async refetchBotMessage(userQuery: string): Promise<void> {
    const { handleFetchingBotMessage } = useChatActions(this.chatService);
    this.chatService.updateLatestBotMessageDataProperty('status', StatusType.Pending);

    await handleFetchingBotMessage(userQuery, false);
  }
}
