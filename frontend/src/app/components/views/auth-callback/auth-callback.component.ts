import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '@services/AuthService';
import { UserService } from '@services/UserService';


@Component({
  selector: 'auth-callback',
  imports: [],
  templateUrl: './auth-callback.component.html',
  styleUrl: './auth-callback.component.scss'
})
export class AuthCallback {
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService,
    private userService: UserService
  ) {
  }

  ngOnInit() {
    console.log('JEDZEIMY');
    this.route.queryParams.subscribe(async (params) => {
      const provider = params['state'];
      const authCode = params['code'];

      try {
        switch (provider) {
          case 'microsoft':
            await this.handleMicrosoftLogin(authCode);
            break;
          case 'google':
            await this.handleGoogleLogin(authCode);
            break;
          default:
            throw new Error('Unknown provider');
        }
      } catch (e) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        console.error(e);
      }
    });
  }

  async handleGoogleLogin(code: string): Promise<void> {
    const tokens = await this.authService.getGoogleTokens(code);
    localStorage.setItem('token', tokens.accessToken);
    localStorage.setItem('refresh', tokens.refreshToken);
    await this.userService.createOrUpdateGoogleUser();
    await this.router.navigate(['/chat']);
  }

  async handleMicrosoftLogin(code: string): Promise<void> {
    const tokens = await this.authService.getMicrosoftTokens(code);
    localStorage.setItem('token', tokens.accessToken);
    localStorage.setItem('refresh', tokens.refreshToken);
    await this.userService.createOrUpdateMicrosoftUser();
    await this.router.navigate(['/chat']);
  }
}
