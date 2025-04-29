import { Component, signal } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { LoginForm } from '@components/features/auth/login-form/login-form.component';
import { RegisterForm } from '@components/features/auth/register-form/register-form.component';
import { MatIconButton } from '@angular/material/button';
import { GoogleToken } from '@appTypes/GoogleToken';
import { AuthService } from '@services/AuthService';
import { UserLoginData } from '@appTypes/UserLoginData';
import { AxiosError } from 'axios';
import { ErrorMessage } from '@enums/ErrorMessage';
import { Router } from '@angular/router';
import { UserRegisterData } from '@appTypes/UserRegisterData';
import { UserService } from '@services/UserService';
import { ConfigService } from '@services/ConfigService';


interface ExtendedWindow extends Window {
  onGoogleLogin: (token: GoogleToken) => void;
}

@Component({
  selector: 'auth-view-view',
  imports: [MatCardModule, MatIconModule, MatTabsModule, LoginForm, RegisterForm, MatIconButton],
  templateUrl: './auth-view.component.html',
  styleUrl: './auth-view.component.scss'
})


export class AuthView {
  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
    private configService: ConfigService,
  ) {
  }

  onIconBackClick(): void {
    this.selectedTabIndex.set(0);
  }

  selectedTabIndex = signal<number>(0);
  loginFormError = signal<ErrorMessage | null>(null);
  registerFormError = signal<ErrorMessage | null>(null);

  async onRegisterFormSubmit(registerData: UserRegisterData): Promise<void> {
    try {
      this.registerFormError.set(null);

      const response = await this.authService.register(registerData);
      localStorage.setItem('token', response.accessToken);
      await this.router.navigate(['/chat']);
    } catch (error) {
      if (error instanceof AxiosError) {
        this.registerFormError.set(error.response?.data.detail);
      }
    }
  }


  async onLoginFormSubmit(userLoginData: UserLoginData): Promise<void> {
    try {
      this.loginFormError.set(null);

      const response = await this.authService.login(userLoginData);
      localStorage.setItem('token', response.accessToken);
      await this.router.navigate(['/chat']);
    } catch (error) {
      if (error instanceof AxiosError) {
        this.loginFormError.set(error.response?.data.detail);
      }
    }
  }

  async onMicrosoftLogin(): Promise<void> {
    window.location.href = this.configService.getMicrosoftPath();
  }

  async onGoogleLogin(): Promise<void> {
    window.location.href = this.configService.getGooglePath();
  }
}
