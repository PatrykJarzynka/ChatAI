import { Component, output } from '@angular/core';
import { MatButton } from '@angular/material/button';
import { MatCardActions, MatCardContent, MatCardHeader, MatCardSubtitle, MatCardTitle } from '@angular/material/card';
import { QueryInput } from '../../../core/query-input/query-input.component';
import { Router } from '@angular/router';


@Component({
  selector: 'login-form',
  imports: [
    MatButton,
    MatCardActions,
    MatCardContent,
    MatCardHeader,
    MatCardSubtitle,
    MatCardTitle,
    QueryInput,
  ],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss'
})
export class LoginForm {

  constructor(private router: Router) {
  }

  newAccountClick = output<void>();

  onNewAccountClick(): void {
    this.newAccountClick.emit();
  }

  async onSignInClick(): Promise<void> {
    await this.router.navigate(['/chat']);
  }
}
