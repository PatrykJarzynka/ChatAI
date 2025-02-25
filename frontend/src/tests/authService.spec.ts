import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { AuthService } from '@services/AuthService';
import { ApiService } from '@services/ApiService';
import { Token } from '@models/Token';
import { UserRegisterData } from '@appTypes/UserRegisterData';
import { UserLoginData } from '@appTypes/UserLoginData';
import { jwtDecode } from 'jwt-decode';


jest.mock('jwt-decode', () => ( {
  jwtDecode: jest.fn(),
} ));


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

  test('should fetch refresh token', async () => {
    jest.spyOn(authService, 'fetchRefreshedAccessToken').mockResolvedValue(mockToken);

    const response = await authService.fetchRefreshedAccessToken();

    expect(response).toEqual(mockToken);
  });

  test('should set refresh token interval with delay bigger than 0', async () => {
    ( jwtDecode as jest.Mock ).mockReturnValueOnce({ exp: Math.floor(Date.now() / 1000) + 60 }); // token valid for 60s
    jest.useFakeTimers();
    jest.spyOn(authService as any, 'calculateIntervalDelay');
    const refreshTokenIntervalSpy = jest.spyOn(authService, 'setRefreshTokenInterval');
    const expectedExecutionTimeRange: number[] = [39000, 40000]; // 60000 ( token valid for 60s ) - 20000 (time taken before token is expired - 20s )

    authService.handleSettingRefreshTokenInterval(mockToken.accessToken);

    expect(authService.calculateIntervalDelay).toBeCalledWith(mockToken.accessToken, 20000);
    const executionTimeArg = refreshTokenIntervalSpy.mock.calls[0][0];

    expect(executionTimeArg).toBeGreaterThan(expectedExecutionTimeRange[0]);
    expect(executionTimeArg).toBeLessThan(expectedExecutionTimeRange[1]);
  });

  test('should set refresh token interval with delay equal to 0', async () => {
    ( jwtDecode as jest.Mock ).mockReturnValueOnce({ exp: Math.floor(Date.now() / 1000) - 60 }); // token already expired

    jest.spyOn(authService, 'calculateIntervalDelay');
    jest.spyOn(authService, 'setRefreshTokenInterval').mockImplementation(() => {
    });

    authService.handleSettingRefreshTokenInterval(mockToken.accessToken);

    expect(authService.calculateIntervalDelay).toBeCalledWith(mockToken.accessToken, 20000);
    expect(authService.setRefreshTokenInterval).toBeCalledWith(0);
  });

  test('should return 0', () => {
    ( jwtDecode as jest.Mock ).mockReturnValueOnce({ exp: Math.floor(Date.now() / 1000) - 60 }); // token already expired

    const delay = authService.calculateIntervalDelay(mockToken.accessToken, 20000);
    expect(jwtDecode).toBeCalled();
    expect(delay).toEqual(0);
  });

  test('should return value between 39000 and 40000', () => {
    ( jwtDecode as jest.Mock ).mockReturnValueOnce({ exp: Math.floor(Date.now() / 1000) + 60 }); // token valid for 60s.

    const delay = authService.calculateIntervalDelay(mockToken.accessToken, 20000);
    expect(jwtDecode).toBeCalled();
    expect(delay).toBeGreaterThan(39000);
    expect(delay).toBeLessThan(40000);
  });

  test('should set interval with delay equal to 20sec', async () => {
    jest.spyOn(authService, 'refreshToken').mockResolvedValue();
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue(mockToken.accessToken);
    jest.spyOn(authService, 'handleSettingRefreshTokenInterval').mockImplementation(() => {
    });

    jest.useFakeTimers();

    authService.setRefreshTokenInterval(20000);

    jest.advanceTimersByTime(20000);

    await Promise.resolve();

    expect(authService.refreshToken).toHaveBeenCalled();

    expect(authService.handleSettingRefreshTokenInterval).toHaveBeenCalledWith(mockToken.accessToken);

    jest.useRealTimers();
  });

  test('should display error in console on trying to set interval', async () => {
    jest.spyOn(authService, 'refreshToken').mockRejectedValue('Failed to refresh token');
    jest.spyOn(console, 'error');

    jest.useFakeTimers();

    authService.setRefreshTokenInterval(20000);

    jest.advanceTimersByTime(20000);

    await Promise.resolve();

    expect(authService.refreshToken).toHaveBeenCalled();
    expect(console.error).toHaveBeenCalledWith('Failed to refresh token');

    jest.useRealTimers();
  });

  test('should refresh token in local storage', async () => {
    jest.spyOn(authService, 'fetchRefreshedAccessToken').mockResolvedValue(mockToken);
    jest.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    });
    await authService.refreshToken();

    expect(authService.fetchRefreshedAccessToken).toHaveBeenCalled();
    expect(Storage.prototype.setItem).toHaveBeenCalledWith('token', mockToken.accessToken);

  });
});
