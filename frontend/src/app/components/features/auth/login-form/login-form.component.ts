import { Component, effect, input, output } from '@angular/core';
import { MatButton, MatFabButton } from '@angular/material/button';
import { MatCardActions, MatCardContent, MatCardHeader, MatCardSubtitle, MatCardTitle } from '@angular/material/card';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MatError, MatFormField } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import useParser from '@composables/useParser';
import { UserLoginData } from 'appTypes/UserLoginData';
import { ErrorMessage } from '@enums/ErrorMessage';
import {
  LoginGoogleButtonComponent
} from '@components/features/auth/login-google-button/login-google-button.component';
import { MatIconModule } from '@angular/material/icon';
import {
  LoginMicrosoftButton
} from '@components/features/auth/login-microsoft-button/login-microsoft-button.component';


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
    LoginGoogleButtonComponent,
    MatIconModule,
    LoginMicrosoftButton
  ],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss'
})
export class LoginForm {
  form: FormGroup;
  parseErrors: (errors: ValidationErrors | null) => string | null;

  newAccountClick = output<void>();
  loginSubmit = output<UserLoginData>();
  googleLogin = output<void>();
  microsoftLogin = output<void>();
  authErrors = input<ErrorMessage | null>(null);

  constructor() {
    const { parseValidationErrorToString } = useParser;

    this.form = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
    });

    this.parseErrors = parseValidationErrorToString;

    effect(() => {
      this.setErrors(this.authErrors());
    });
  }

  setErrors(error: ErrorMessage | null) {
    if (error === ErrorMessage.WrongCredentials) {
      this.form.controls['email'].setErrors({ credentials: true });
      this.form.controls['password'].setErrors({ credentials: true });
    } else {
      this.form.controls['email'].setErrors(null);
      this.form.controls['password'].setErrors(null);
    }
  }

  onSubmit(): void {
    if (this.form.invalid) {
      return;
    }

    const loginData: UserLoginData = {
      email: this.form.controls['email'].value,
      password: this.form.controls['password'].value
    };

    this.loginSubmit.emit(loginData);
  }

  onNewAccountClick(): void {
    this.newAccountClick.emit();
  }
}
