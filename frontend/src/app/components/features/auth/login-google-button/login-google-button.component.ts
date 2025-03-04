import { Component, output } from '@angular/core';
import { GoogleToken } from '@appTypes/GoogleToken';
import { GOOGLE_CLIENT_ID } from '@api/apiConfig';


@Component({
  selector: 'login-google-button',
  imports: [],
  templateUrl: './login-google-button.component.html',
  styleUrl: './login-google-button.component.scss'
})
export class LoginGoogleButtonComponent {

  googleLogin = output<GoogleToken>();

  ngOnInit() {
    ( window as any ).google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: (data: GoogleToken) => {
        this.googleLogin.emit(data);
      }
    });

    ( window as any ).google.accounts.id.renderButton(
      document.getElementById('google-button'),
      {
        theme: 'outline',
        size: 'large',
        shape: 'pill',
        type: 'standard',
        text: 'signin_with',
        'data-logo-alignment': 'left'
      }
    );
  }
}
