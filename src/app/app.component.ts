import { Component, effect, model, signal } from '@angular/core';
import { ChatWindow } from './components/chat-window/chat-window.component';
import { ChatActions } from './components/chat-actions/chat-actions.component';
import { ChatHistory } from './components/chat-history/chat-history.component';
import { ResizablePanel } from './components/resizable-panel/resizable-panel.component';
import { AppButton } from './components/app-button/app-button.component';
import { MatIcon } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';
import { ChatService } from '../services/ChatService';
import { MatCheckbox } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import useChatActions from '../composables/useChatActions';
import { StatusType } from '../enums/StatusType';

@Component({
  selector: 'app-root',
  imports: [ChatWindow, ChatActions, ChatHistory, ResizablePanel, AppButton, MatIcon, MatTooltip, MatCheckbox, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
})
export class AppComponent {
  title = 'chatAI';
  panelVisibility = signal<boolean>(true);
  shouldFail = model<boolean>(false);

  private readonly handleFetchingBotMessage: (userQuery: string, chatItemId: string, shouldFail: boolean) => Promise<void>;

  constructor(private chatService: ChatService)
  {
    const { handleFetchingBotMessage } = useChatActions(this.chatService);
    this.handleFetchingBotMessage = handleFetchingBotMessage
  }

  togglePanelVisibility() {
    this.panelVisibility.set(!this.panelVisibility());
  }

  startNewChat() {
    const currentChat = this.chatService.getCurrentChat();
    if (currentChat?.chatItems.length) {
      this.chatService.startNewChat();
    }
  }

  async onUserQuerySend(userQuery: string) {
    const chatItem = this.chatService.createAndAddChatItem(userQuery);

    if (chatItem) {
      await this.handleFetchingBotMessage(userQuery, chatItem.id, this.shouldFail());
    }
  }

  async refetchBotMessage(chatItemId: string, userQuery: string): Promise<void> {
    const { handleFetchingBotMessage } = useChatActions(this.chatService);
    this.chatService.updateBotMessageDataProperty('status', StatusType.Pending, chatItemId);

    await handleFetchingBotMessage(userQuery, chatItemId, false)
  }
}
