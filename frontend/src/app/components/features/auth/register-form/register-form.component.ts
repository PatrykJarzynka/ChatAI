import { Component, effect, input, output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButton } from '@angular/material/button';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import useValidators from '@composables/useValidators';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardHeader, MatCardSubtitle, MatCardTitle } from '@angular/material/card';
import { UserRegisterData } from 'appTypes/UserRegisterData';
import { ErrorMessage } from '@enums/ErrorMessage';
import useParser from '@composables/useParser';
import { AuthProvider } from '@appTypes/AuthProvider';


@Component({
  selector: 'register-form',
  imports: [FormsModule, MatFormFieldModule, MatInputModule, MatIconModule, ReactiveFormsModule, ReactiveFormsModule, MatCardHeader, MatCardSubtitle, MatCardTitle, MatButton],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.scss',
  standalone: true
})
export class RegisterForm {
  form: FormGroup;
  parseErrors: (errors: ValidationErrors | null) => string | null;
  registerSubmit = output<UserRegisterData>();
  authErrors = input<ErrorMessage | null>(null);

  constructor() {
    const { validateSamePassword } = useValidators;
    const { parseValidationErrorToString } = useParser;

    this.form = new FormGroup({
      fullName: new FormControl('', Validators.required),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
      confirmPassword: new FormControl('', Validators.required),
    }, {
      validators: validateSamePassword,
    });

    this.parseErrors = parseValidationErrorToString;

    effect(() => {
      this.setErrors(this.authErrors());
    });
  }

  setErrors(error: ErrorMessage | null) {
    if (error === ErrorMessage.EmailRegistered) {
      this.form.controls['email'].setErrors({ emailExists: true });
    } else {
      this.form.controls['email'].setErrors(null);
    }
  }

  onSubmit() {
    if (this.form.invalid) {
      return;
    }

    const registerData: UserRegisterData = {
      email: this.form.controls['email'].value,
      password: this.form.controls['password'].value,
      fullName: this.form.controls['fullName'].value,
      tenant: AuthProvider.LOCAL
    };

    this.registerSubmit.emit(registerData);

    // try {
    //   const response = await this.authService.register(registerData);
    //   if (response) {
    //     localStorage.setItem('token', response.accessToken);
    //     await this.router.navigate(['/chat']);
    //   }
    //
    // } catch (error) {
    //   if (error instanceof AxiosError) {
    //     if (error.response?.data.detail === ErrorMessage.EmailRegistered) {
    //       this.form.controls['email'].setErrors({ emailExists: true });
    //     }
    //   }
    // }
  }
}
