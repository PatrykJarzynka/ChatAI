import { Component, output } from '@angular/core';
import { GOOGLE_CLIENT_ID } from '@api/apiConfig';
import { MatButton } from '@angular/material/button';


declare const google: any;

interface GoogleAuthResponse {
  authuser: string;
  code: string;
  prompt: string;
  scope: string;
}

@Component({
  selector: 'login-google-button',
  imports: [
    MatButton
  ],
  templateUrl: './login-google-button.component.html',
  styleUrl: './login-google-button.component.scss'
})


export class LoginGoogleButtonComponent {
  client: any;

  googleLogin = output<string>();

  ngOnInit() {
    this.client = google.accounts.oauth2.initCodeClient({
      client_id: GOOGLE_CLIENT_ID,
      scope: 'openid email profile',
      ux_mode: 'popup',
      redirect_uri: 'postmessage',
      access_type: 'offline',
      callback: (response: GoogleAuthResponse) => {
        this.googleLogin.emit(response.code);
      }
    });
  }
}
