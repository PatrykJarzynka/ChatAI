import { Component, model, output } from '@angular/core';
import { MatIcon } from '@angular/material/icon';
import { MatIconButton } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatFormField, MatLabel, MatPrefix, MatSuffix } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';


@Component({
  selector: 'chat-actions',
  imports: [
    MatIcon,
    MatIconButton,
    FormsModule,
    MatFormField,
    MatInput,
    MatLabel,
    MatPrefix,
    MatSuffix,
  ],
  templateUrl: './chat-actions.component.html',
  styleUrl: './chat-actions.component.scss',
  standalone: true,
})
export class ChatActions {
  message = model<string>('');
  querySend = output<string>();

  constructor() {
  }

  async onUserQuerySend(userQuery: string) {
    if (userQuery.trim() === '') {
      return;
    }

    this.querySend.emit(userQuery);

    this.message.set('');
  }
}
