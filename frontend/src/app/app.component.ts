import { Component, model } from '@angular/core';
import { ChatWindow } from './components/features/chat/chat-window/chat-window.component';
import { ChatActions } from './components/features/chat/chat-actions/chat-actions.component';
import { ChatHistory } from './components/features/chat/chat-history/chat-history.component';
import { AppSidebar } from '../app/components/core/app-sidebar/app-sidebar.component';
import { MatIcon } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';
import { ChatService } from '../services/ChatService';
import { MatCheckbox } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import useChatActions from '../composables/useChatActions';
import { StatusType } from '../enums/StatusType';
import { MatSidenavModule } from '@angular/material/sidenav';
import { NgStyle } from '@angular/common';
import { MatButton, MatIconButton, MatMiniFabButton } from '@angular/material/button';


@Component({
  selector: 'app-root',
  imports: [ChatWindow, ChatActions, MatIcon, MatTooltip, MatCheckbox, FormsModule, MatSidenavModule, AppSidebar, NgStyle, MatButton, ChatHistory, MatMiniFabButton],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
})
export class AppComponent {
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
