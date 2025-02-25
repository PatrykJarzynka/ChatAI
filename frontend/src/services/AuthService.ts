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

  public calculateIntervalDelay(accessToken: string, timeInMsBeforeTokenExpire: number): number {
    const decodedToken = jwtDecode(accessToken);

    let delay = 0;

    if (decodedToken.exp) {
      const expireTimeInMs = decodedToken.exp * 1000;
      const executionTime = expireTimeInMs - timeInMsBeforeTokenExpire;
      const calculatedDelay = executionTime - Date.now();

      if (calculatedDelay >= 0) {
        delay = calculatedDelay;
      }
    }

    return delay;
  }

  public async register(data: UserRegisterData): Promise<Token> {
    return await this.apiService.post<Token, UserRegisterData>(`${ ENDPOINT }/register`, data);
  }

  public async login(data: UserLoginData): Promise<Token> {
    const loginData = new URLSearchParams();
    loginData.append('username', data.email);
    loginData.append('password', data.password);

    return await this.apiService.post<Token, URLSearchParams>(`${ ENDPOINT }/login`, loginData, false, true);
  }

  public async fetchRefreshedAccessToken(): Promise<Token> {
    return await this.apiService.get<Token>(`${ ENDPOINT }/refresh`);
  }

  public async verifyToken(): Promise<Token> {
    return await this.apiService.get<Token>(`${ ENDPOINT }/verify`);
  }

  public handleSettingRefreshTokenInterval(token: string): void {
    if (this.refreshTokenCallInterval) {
      clearInterval(this.refreshTokenCallInterval);
    }

    const delay = this.calculateIntervalDelay(token, 20000);
    this.setRefreshTokenInterval(delay);
  }


  public setRefreshTokenInterval(delay: number): void {
    this.refreshTokenCallInterval = window.setInterval(async () => {
      try {
        await this.refreshToken();
        const newToken = localStorage.getItem('token');
        if (newToken) {
          this.handleSettingRefreshTokenInterval(newToken);
        }
      } catch (error) {
        console.error('Failed to refresh token');
      }

    }, delay);
  }

  public async refreshToken(): Promise<void> {
    const refreshedToken = await this.fetchRefreshedAccessToken();
    localStorage.setItem('token', refreshedToken.accessToken);
  }
}
