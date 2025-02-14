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
import { MatButton, MatMiniFabButton } from '@angular/material/button';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
})
export class AppComponent {
  constructor() {
  }
}
