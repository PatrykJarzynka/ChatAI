import { Component, output } from '@angular/core';
import { MatButton } from '@angular/material/button';
import { MatCardActions, MatCardContent, MatCardHeader, MatCardSubtitle, MatCardTitle } from '@angular/material/card';
import { Router } from '@angular/router';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MatError, MatFormField } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import useParser from '../../../../../composables/useParser';
import { AuthService } from '../../../../../services/AuthService';
import { UserLoginData } from '../../../../../types/UserLoginData';
import { AxiosError } from 'axios';
import { ErrorMessage } from '../../../../../enums/ErrorMessage';


@Component({
  selector: 'login-form',
  imports: [
    MatButton,
    MatCardActions,
    MatCardContent,
    MatCardHeader,
    MatCardSubtitle,
    MatCardTitle,
    FormsModule,
    MatError,
    MatFormField,
    MatInput,
    ReactiveFormsModule,
  ],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss'
})
export class LoginForm {
  form: FormGroup;
  parseErrors: (errors: ValidationErrors | null) => string | null;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {
    const { parseValidationErrorToString } = useParser;

    this.form = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
    });

    this.parseErrors = parseValidationErrorToString;
  }

  newAccountClick = output<void>();

  async onSubmit(): Promise<void> {
    if (this.form.invalid) {
      return;
    }

    const loginData: UserLoginData = {
      email: this.form.controls['email'].value,
      password: this.form.controls['password'].value
    };

    try {
      const response = await this.authService.login(loginData);
      localStorage.setItem('token', response.accessToken);
      await this.router.navigate(['/chat']);
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.data.detail === ErrorMessage.WrongCredentials) {
          this.form.controls['email'].setErrors({ credentials: true });
          this.form.controls['password'].setErrors({ credentials: true });
        }
      }
    }
  }

  onNewAccountClick(): void {
    this.newAccountClick.emit();
  }
}
