import { Component, input, output, signal } from '@angular/core';
import { AppButton } from '../../components/app-button/app-button.component';
import { QueryInput } from '../../components/query-input/query-input.component';

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
  message = signal<string> ('');
  shouldFail = input.required<boolean> ();
  querySend = output<string> ();

  constructor() {
  }

  async onUserQuerySend(userQuery: string) {
    if (userQuery.trim () === '') {
      return;
    }

    this.message.set ('');

    this.querySend.emit (userQuery);
  }
}
