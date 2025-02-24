import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { UserService } from '@services/UserService';
import { ApiService } from '@services/ApiService';
import { MOCK_USER } from '@utils/mockedData';


jest.mock('@services/ApiService');

describe('userService', () => {
  let apiServiceMock: jest.Mocked<ApiService>;
  let userService: UserService;

  beforeEach(async () => {
    apiServiceMock = new ApiService() as jest.Mocked<ApiService>;
    userService = new UserService(apiServiceMock);
  });

  test('should fetch user', async () => {
    jest.spyOn(apiServiceMock, 'get').mockResolvedValue(MOCK_USER);

    await userService.fetchUser();
    expect(apiServiceMock.get).toHaveBeenCalledWith('user/me');
  });

  test('should set current user', async () => {
    userService.setCurrentUser(MOCK_USER);
    const currentUser = userService.getCurrentUser();
    expect(currentUser()).toEqual(MOCK_USER);
  });
});
