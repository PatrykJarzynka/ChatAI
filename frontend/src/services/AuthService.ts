import { Injectable } from '@angular/core';
import { ApiService } from '@services/ApiService';
import { UserRegisterData } from '@appTypes/UserRegisterData';
import { Token } from '@models/Token';
import { UserLoginData } from '@appTypes/UserLoginData';
import { jwtDecode } from 'jwt-decode';


const ENDPOINT = 'auth';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  refreshTokenCallInterval: number | null = null;

  constructor(
    private apiService: ApiService,
  ) {
  }

  async register(data: UserRegisterData): Promise<Token> {
    return await this.apiService.post<Token, UserRegisterData>(`${ ENDPOINT }/register`, data);
  }

  async login(data: UserLoginData): Promise<Token> {
    const loginData = new URLSearchParams();
    loginData.append('username', data.email);
    loginData.append('password', data.password);

    return await this.apiService.post<Token, URLSearchParams>(`${ ENDPOINT }/login`, loginData, false, true);
  }

  async getRefreshedAccessToken(): Promise<Token> {
    return await this.apiService.get<Token>(`${ ENDPOINT }/refresh`);
  }

  setRefreshTokenInterval(token: string): void {
    if (this.refreshTokenCallInterval) {
      this.removeRefreshTokenInterval();
    }

    const decodedToken = jwtDecode(token);

    if (decodedToken.exp) {
      const expireTimeInMs = decodedToken.exp * 1000;

      const executionTime = expireTimeInMs - 20 * 1000;
      const delay = executionTime - Date.now();

      const finalDelay = Math.max(delay, 0); // finalDelay set to 0 if token is already expired

      this.refreshTokenCallInterval = window.setInterval(async () => {
        try {
          const refreshedToken = await this.getRefreshedAccessToken();
          localStorage.setItem('token', refreshedToken.accessToken);
          this.setRefreshTokenInterval(refreshedToken.accessToken);
        } catch (error) {
          console.error('Failed to refresh token');
        }

      }, finalDelay);
    }
  }

  removeRefreshTokenInterval(): void {
    if (this.refreshTokenCallInterval) {
      clearInterval(this.refreshTokenCallInterval);
    }
  }
}
