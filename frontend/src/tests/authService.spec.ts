import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { AuthService } from '../services/AuthService';
import { ApiService } from '../services/ApiService';
import { Token } from '../models/Token';
import { UserRegisterData } from '../types/UserRegisterData';
import { UserLoginData } from '../types/UserLoginData';


describe('authService', () => {
  let apiService: ApiService;
  let authService: AuthService;
  let mockToken: Token;

  beforeEach(() => {
    apiService = new ApiService();
    authService = new AuthService(apiService);

    mockToken = {
      tokenType: 'bearer',
      accessToken: 'mockToken'
    };
  });

  test('should return token on register', async () => {
    jest.spyOn(authService, 'register').mockResolvedValue(mockToken);
    const registerData: UserRegisterData = {
      email: 'test@test.com',
      fullName: 'XYZ',
      password: 'mockPassword'
    };

    const response = await authService.register(registerData);
    expect(response).toEqual(mockToken);
  });

  test('should return token on login', async () => {
    jest.spyOn(authService, 'login').mockResolvedValue(mockToken);
    const loginData: UserLoginData = {
      email: 'test@test.com',
      password: 'mockPassword'
    };

    const response = await authService.login(loginData);
    expect(response).toEqual(mockToken);
  });
});
