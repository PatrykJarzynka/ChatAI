import { Component, computed, model, signal } from '@angular/core';
import { MatIcon } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';
import { FormsModule } from '@angular/forms';
import { MatSidenavModule } from '@angular/material/sidenav';
import { AppSidebar } from '../../core/app-sidebar/app-sidebar.component';
import { NgClass, NgStyle } from '@angular/common';
import { MatButton, MatFabButton, MatMiniFabButton } from '@angular/material/button';
import { ChatService } from '@services/ChatService';
import { Router } from '@angular/router';
import { MatMenu, MatMenuItem, MatMenuTrigger } from '@angular/material/menu';
import useChatActions from '@composables/useChatActions';
import { UserService } from '@services/UserService';
import { StatusType } from '@enums/StatusType';
import { ChatHistory } from '@components/features/chat/chat-history/chat-history.component';
import { ChatWindow } from '@components/features/chat/chat-window/chat-window.component';
import { ChatActions } from '@components/features/chat/chat-actions/chat-actions.component';
import { AuthService } from '@services/AuthService';
import { ChatHistoryService } from '@services/ChatHistoryService';
import { MatTab, MatTabGroup, MatTabLabel } from '@angular/material/tabs';
import { MatDivider } from '@angular/material/divider';
import { FileManager } from '@services/FileMananger';
import { MatListOption, MatSelectionList } from '@angular/material/list';
import { MatProgressSpinner } from '@angular/material/progress-spinner';
import { MatCheckbox } from '@angular/material/checkbox';
import { UploadedFile } from '@appTypes/UploadedFile';


@Component({
  selector: 'chat-view',
  imports: [ChatWindow, ChatActions, MatIcon, MatTooltip, FormsModule, MatSidenavModule, AppSidebar, NgStyle, MatButton, ChatHistory, MatMiniFabButton, MatMenuTrigger, MatMenu, MatMenuItem, MatTabGroup, MatTab, MatTabLabel, MatDivider, MatIcon, NgClass, MatSelectionList, MatListOption, MatProgressSpinner, MatCheckbox],
  templateUrl: './chat-view.component.html',
  styleUrl: './chat-view.component.scss'
})
export class ChatView {
  title = 'chatAI';
  panelVisibility = model<boolean>(true);

  private readonly handleFetchingBotMessage: (userQuery: string) => Promise<void>;
  currentUser = computed(() => this.userService.getCurrentUser()());
  isDragging = signal<boolean>(false);
  files = signal<UploadedFile[]>([]);

  constructor(
    private chatService: ChatService,
    private userService: UserService,
    private chatHistoryService: ChatHistoryService,
    private router: Router,
    private authService: AuthService,
    private fileManager: FileManager
  ) {
    const { handleFetchingBotMessage } = useChatActions(this.chatService, this.userService, this.fileManager);
    this.handleFetchingBotMessage = handleFetchingBotMessage;
  }

  onSelectionChange(fileId: number) {
    this.fileManager.updateSelectedFiles(fileId);
  }

  async ngOnInit() {
    const token = localStorage.getItem('token');
    let validToken = false;

    if (token) {
      try {
        const response = await this.authService.verifyToken();
        validToken = response.isValid;
      } catch (error) {
        await this.router.navigate(['/']);
      }

      if (validToken) {
        const user = await this.userService.fetchUser();
        this.userService.setCurrentUser(user);
        this.authService.handleSettingRefreshTokenInterval(token);

        await this.initUserChatHistory(user.id);
        this.files = this.fileManager.getFiles();
      }
    } else {
      await this.router.navigate(['/']);
    }
  }

  async initUserChatHistory(userId: number) {
    const chatHistories = await this.chatHistoryService.fetchUserChatHistory(userId);
    this.chatHistoryService.setChatHistories(chatHistories);
  }

  async startNewChat() {
    const currentChat = this.chatService.getCurrentChat();
    if (currentChat?.chatItems.length) {
      await this.chatService.startNewChat();
    }
  }

  async onLogoutButtonClick() {
    this.clearUserState();

    await this.router.navigate(['/']);
  }

  clearUserState() {
    this.chatService.clearCurrentChat();
    this.chatHistoryService.clearChatHistory();

    localStorage.removeItem('token');
    localStorage.removeItem('refresh');

    if (this.authService.refreshTokenCallInterval) {
      clearInterval(this.authService.refreshTokenCallInterval);
    }
  }

  async onUserQuerySend(userQuery: string) {
    if (!this.chatService.getCurrentChat()) {
      await this.chatService.startNewChat();
    }

    this.chatService.createAndAddChatItemTemplate(userQuery);
    await this.handleFetchingBotMessage(userQuery);
  }

  async refetchBotMessage(userQuery: string): Promise<void> {
    this.chatService.updateLatestBotMessageDataProperty('status', StatusType.Pending);

    await this.handleFetchingBotMessage(userQuery);
  }

  async onFileButtonClick(event: Event) {
    event.stopPropagation();
    event.preventDefault();

    const element = event.currentTarget as HTMLInputElement;
    const fileList = element.files;

    if (fileList) {
      await this.fileManager.onFilesUpload(Array.from(fileList));
    }
  }

  onDragOver(event: DragEvent): void {
    event.stopPropagation();
    event.preventDefault();

    this.isDragging.set(true);
  }

  onDragLeave(event: DragEvent): void {
    event.stopPropagation();
    event.preventDefault();

    this.isDragging.set(false);
  }

  async onDrop(event: DragEvent): Promise<void> {
    event.stopPropagation();
    event.preventDefault();

    if (event.dataTransfer) {
      await this.fileManager.onFilesUpload(Array.from(event.dataTransfer.files));
    }
  }

  protected readonly StatusType = StatusType;
}
