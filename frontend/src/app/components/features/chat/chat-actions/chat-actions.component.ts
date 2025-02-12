import { Component, output, signal } from '@angular/core';
import { QueryInput } from '../../../core/query-input/query-input.component';
import { MatIcon } from '@angular/material/icon';
import { MatIconButton } from '@angular/material/button';


@Component({
  selector: 'chat-actions',
  imports: [
    QueryInput,
    MatIcon,
    MatIconButton,
  ],
  templateUrl: './chat-actions.component.html',
  styleUrl: './chat-actions.component.scss',
  standalone: true,
})
export class ChatActions {
  message = signal<string | null>(null);
  querySend = output<string>();

  constructor() {
  }

  async onUserQuerySend(userQuery: string | null) {
    if (userQuery === null) {
      return;
    }

    this.message.set(null);

    this.querySend.emit(userQuery);
  }
}
