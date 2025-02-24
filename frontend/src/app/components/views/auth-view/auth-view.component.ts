import { Component, signal } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { LoginForm } from '@components/features/auth/login-form/login-form.component';
import { RegisterForm } from '@components/features/auth/register-form/register-form.component';
import { MatIconButton } from '@angular/material/button';


@Component({
  selector: 'auth-view-view',
  imports: [MatCardModule, MatIconModule, MatTabsModule, LoginForm, RegisterForm, MatIconButton],
  templateUrl: './auth-view.component.html',
  styleUrl: './auth-view.component.scss'
})
export class AuthView {
  constructor() {
  }


  onIconBackClick(): void {
    this.selectedTabIndex.set(0);
  }

  selectedTabIndex = signal<number>(0);
}
