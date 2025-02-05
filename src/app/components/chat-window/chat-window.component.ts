import { Component, output } from '@angular/core';
import { ChatService } from '../../../services/ChatService';
import { MatIconModule } from '@angular/material/icon';
import { StatusType } from '../../../enums/StatusType';
import { AppLoader } from '../../components/app-loader/app-loader.component';
import { AppButton } from '../../components/app-button/app-button.component';

@Component({
  selector: 'chat-window',
  imports: [MatIconModule, AppLoader, AppButton, AppButton],
  templateUrl: './chat-window.component.html',
  styleUrl: './chat-window.component.scss',
  standalone: true,
})
export class ChatWindow {

  chat = () => this.chatService.getCurrentChat();
  refreshButtonClick = output<{chatItemId: string, userQuery: string}>();

  constructor(
    private chatService: ChatService,
) {}

  ngOnInit() {
    this.chatService.startNewChat();
  }

  protected readonly StatusType = StatusType;
}
