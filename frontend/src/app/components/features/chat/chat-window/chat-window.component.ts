import { Component, output } from '@angular/core';
import { ChatService } from '../../../../../services/ChatService';
import { MatIconModule } from '@angular/material/icon';
import { StatusType } from '../../../../../enums/StatusType';
import { AppLoader } from '../../../core/app-loader/app-loader.component';
import { AppButton } from '../../../core/app-button/app-button.component';


@Component({
  selector: 'chat-window',
  imports: [MatIconModule, AppLoader, AppButton, AppButton],
  templateUrl: './chat-window.component.html',
  styleUrl: './chat-window.component.scss',
  standalone: true,
})
export class ChatWindow {

  refreshButtonClick = output<string>();
  protected readonly StatusType = StatusType;

  constructor(
    private chatService: ChatService,
  ) {
  }

  chat = () => this.chatService.getCurrentChat();
}
