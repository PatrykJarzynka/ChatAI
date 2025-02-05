import { Component, input, output, signal } from '@angular/core';
import { AppButton } from '../../../core/app-button/app-button.component';
import { QueryInput } from '../../../core/query-input/query-input.component';


@Component({
  selector: 'chat-actions',
  imports: [
    AppButton,
    QueryInput
  ],
  templateUrl: './chat-actions.component.html',
  styleUrl: './chat-actions.component.scss',
  standalone: true,
})
export class ChatActions {
  message = signal<string>('');
  querySend = output<string>();

  constructor() {
  }

  async onUserQuerySend(userQuery: string) {
    if (userQuery.trim() === '') {
      return;
    }

    this.message.set('');

    this.querySend.emit(userQuery);
  }
}
