import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginForm } from './login-form.component';
import { expect, jest, test, describe, beforeEach } from '@jest/globals';
import { AuthService } from '@services/AuthService';
import { Router } from '@angular/router';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { AxiosError } from 'axios';
import { ErrorMessage } from '@enums/ErrorMessage';
import { UserLoginData } from 'appTypes/UserLoginData';
import { Token } from '@models/Token';


describe('LoginForm', () => {
  let component: LoginForm;
  let fixture: ComponentFixture<LoginForm>;
  let authService: AuthService;
  let submitButton: HTMLButtonElement;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginForm, BrowserAnimationsModule, NoopAnimationsModule],
      providers: [
        { provide: Router, useValue: { navigate: jest.fn() } },
      ]
    })
      .compileComponents();

    router = TestBed.inject(Router);
    authService = TestBed.inject(AuthService);

    fixture = TestBed.createComponent(LoginForm);
    component = fixture.componentInstance;

    submitButton = fixture.nativeElement.querySelector('[type="submit"]');

    fixture.detectChanges();
  });

  test('should submit form after button click', () => {
    jest.spyOn(component, 'onSubmit');
    submitButton.click();

    expect(component.onSubmit).toHaveBeenCalled();
  });

  test('should set error "required" on each field', () => {
    const expectedError = { required: true };
    jest.spyOn(authService, 'login');
    jest.spyOn(component, 'onSubmit');
    jest.spyOn(component, 'parseErrors');

    submitButton.click();
    fixture.detectChanges();

    for (let controlsKey in component.form.controls) {
      expect(component.form.controls[controlsKey].errors).toEqual(expectedError);
      expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    }

    expect(component.onSubmit).toHaveBeenCalled();
    expect(component.form.invalid).toBe(true);


    expect(authService.login).not.toHaveBeenCalled();
  });

  test('should set error "credentials" on each field', async () => {
    const expectedError = { credentials: true };
    const mockFormData: UserLoginData = {
      email: 'test@test.com',
      password: 'MockPassword',
    };

    const axiosError = new AxiosError('Request failed');
    ( axiosError as any ).response = { data: { detail: ErrorMessage.WrongCredentials } };

    jest.spyOn(authService, 'login').mockRejectedValue(axiosError);
    jest.spyOn(component, 'onSubmit');
    jest.spyOn(component, 'parseErrors');

    component.form.setValue({
      email: mockFormData.email,
      password: mockFormData.password,
    });

    fixture.detectChanges();

    submitButton.click();

    expect(component.onSubmit).toHaveBeenCalled();

    expect(authService.login).toHaveBeenCalledWith(mockFormData);
    await expect(authService.login).rejects.toThrowError();

    fixture.detectChanges();

    for (let controlsKey in component.form.controls) {
      expect(component.form.controls[controlsKey].errors).toEqual(expectedError);
      expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    }

    expect(component.form.invalid).toBe(true);
  });

  test('should emit newAccountClick event', () => {
    const newAccountButton = fixture.nativeElement.querySelector('[type="button"]');
    jest.spyOn(component, 'onNewAccountClick');
    jest.spyOn(component.newAccountClick, 'emit');

    newAccountButton.click();

    expect(component.onNewAccountClick).toHaveBeenCalled();
    expect(component.newAccountClick.emit).toHaveBeenCalled();
  });

  test('should save token in local storage and redirect to chat view', async () => {
    const mockFormData: UserLoginData = {
      email: 'test@test.com',
      password: 'MockPassword',
    };
    const mockResponse: Token = { accessToken: 'mockToken', tokenType: 'bearer' };

    jest.spyOn(authService, 'login').mockResolvedValue(mockResponse);
    jest.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    });

    component.form.setValue({
      email: mockFormData.email,
      password: mockFormData.password,
    });

    await component.onSubmit();

    expect(authService.login).toHaveBeenCalledWith(mockFormData);
    expect(localStorage.setItem).toHaveBeenCalledWith('token', mockResponse.accessToken);
    expect(router.navigate).toHaveBeenCalledWith(['/chat']);
  });
});
