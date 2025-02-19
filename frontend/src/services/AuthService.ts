import { Injectable } from '@angular/core';
import { ApiService } from '../services/ApiService';
import { UserRegisterData } from '../types/UserRegisterData';
import { Token } from '../models/Token';
import { UserLoginData } from '../types/UserLoginData';


const ENDPOINT = 'auth';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
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
}
