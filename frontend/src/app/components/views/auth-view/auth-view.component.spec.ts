import { ComponentFixture, TestBed } from '@angular/core/testing';
import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { AuthView } from './auth-view.component';
import { By } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthService } from '@services/AuthService';
import { Router } from '@angular/router';
import { UserLoginData } from '@appTypes/UserLoginData';
import { Token } from '@models/Token';
import { ErrorMessage } from '@enums/ErrorMessage';
import { AxiosError } from 'axios';
import { UserRegisterData } from '@appTypes/UserRegisterData';
import { AuthProvider } from '@appTypes/AuthProvider';


describe('AuthView', () => {
  let component: AuthView;
  let fixture: ComponentFixture<AuthView>;
  let authService: AuthService;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuthView, BrowserAnimationsModule],
      providers: [
        { provide: Router, useValue: { navigate: jest.fn() } },
      ]
    })
      .compileComponents();

    authService = TestBed.inject(AuthService);
    router = TestBed.inject(Router);

    fixture = TestBed.createComponent(AuthView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  test('should change tab to register form', () => {
    const loginForm = fixture.debugElement.query(By.css('.login-form-container'));
    loginForm.componentInstance.newAccountClick.emit(loginForm);

    expect(component.selectedTabIndex()).toBe(1);
  });

  test('should call onLoginFormSubmit function', () => {
    const mockFormData: UserLoginData = {
      email: 'test@test.com',
      password: 'MockPassword',
    };

    jest.spyOn(component, 'onLoginFormSubmit');
    const loginForm = fixture.debugElement.query(By.css('.login-form-container'));
    loginForm.componentInstance.loginSubmit.emit(mockFormData);

    expect(component.onLoginFormSubmit).toBeCalledWith(mockFormData);
  });

  test('should change tab to login form', () => {
    jest.spyOn(component, 'onIconBackClick');
    component.selectedTabIndex.set(1);

    fixture.detectChanges();

    const goBackButton = fixture.nativeElement.querySelector('.back-button');

    goBackButton.click();
    fixture.detectChanges();

    expect(component.onIconBackClick).toHaveBeenCalled();
    expect(component.selectedTabIndex()).toBe(0);
  });

  test('should clear registerErrors, set token in localStorage and redirect to chat view ', async () => {
    component.loginFormError.set(ErrorMessage.EmailRegistered);

    const mockFormData: UserRegisterData = {
      email: 'test@test.com',
      password: 'MockPassword',
      fullName: 'Harry Angel',
      tenant: AuthProvider.LOCAL,
    };

    const mockResponseToken: Token = { accessToken: 'mockToken', tokenType: 'bearer' };

    jest.spyOn(authService, 'register').mockResolvedValue(mockResponseToken);
    jest.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    });

    fixture.detectChanges();

    await component.onRegisterFormSubmit(mockFormData);

    expect(authService.register).toHaveBeenCalledWith(mockFormData);
    expect(localStorage.setItem).toHaveBeenCalledWith('token', mockResponseToken.accessToken);
    expect(router.navigate).toHaveBeenCalledWith(['/chat']);
    expect(component.registerFormError()).toEqual(null);
  });

  test('should set registerFormError to EmailRegistered', async () => {
    const mockFormData: UserRegisterData = {
      email: 'test@test.com',
      password: 'MockPassword',
      fullName: 'Harry Angel',
      provider: AuthProvider.LOCAL,
    };

    const axiosError = new AxiosError('Request failed');
    ( axiosError as any ).response = { data: { detail: ErrorMessage.EmailRegistered } };

    jest.spyOn(authService, 'register').mockRejectedValue(axiosError);

    fixture.detectChanges();

    await component.onRegisterFormSubmit(mockFormData);

    expect(authService.register).toHaveBeenCalledWith(mockFormData);
    await expect(authService.register).rejects.toThrowError();
  });

  test('should clear loginErrors, set token in localStorage and redirect to chat view ', async () => {
    component.loginFormError.set(ErrorMessage.WrongCredentials);

    const mockFormData: UserLoginData = {
      email: 'test@test.com',
      password: 'MockPassword',
    };

    const mockResponseToken: Token = { accessToken: 'mockToken', tokenType: 'bearer' };

    jest.spyOn(authService, 'login').mockResolvedValue(mockResponseToken);
    jest.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    });

    fixture.detectChanges();

    await component.onLoginFormSubmit(mockFormData);

    expect(authService.login).toHaveBeenCalledWith(mockFormData);
    expect(localStorage.setItem).toHaveBeenCalledWith('token', mockResponseToken.accessToken);
    expect(router.navigate).toHaveBeenCalledWith(['/chat']);
    expect(component.loginFormError()).toEqual(null);
  });

  test('should set loginFormError to WrongCredentials', async () => {
    const mockFormData: UserLoginData = {
      email: 'test@test.com',
      password: 'MockPassword',
    };

    const axiosError = new AxiosError('Request failed');
    ( axiosError as any ).response = { data: { detail: ErrorMessage.WrongCredentials } };

    jest.spyOn(authService, 'login').mockRejectedValue(axiosError);

    fixture.detectChanges();

    await component.onLoginFormSubmit(mockFormData);

    expect(authService.login).toHaveBeenCalledWith(mockFormData);
    await expect(authService.login).rejects.toThrowError();
  });
});
