import { ComponentFixture, TestBed } from '@angular/core/testing';
import { describe, test, beforeEach, expect, jest } from '@jest/globals';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { RegisterForm } from './register-form.component';
import { AuthService } from '@services/AuthService';
import { AxiosError } from 'axios';
import { ErrorMessage } from '@enums/ErrorMessage';
import { UserRegisterData } from 'appTypes/UserRegisterData';
import { Token } from '@models/Token';
import { Router } from '@angular/router';


describe('RegisterForm', () => {
  let component: RegisterForm;
  let fixture: ComponentFixture<RegisterForm>;
  let authService: AuthService;
  let submitButton: HTMLButtonElement;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegisterForm, BrowserAnimationsModule, NoopAnimationsModule],
      providers: [
        { provide: Router, useValue: { navigate: jest.fn() } },
      ]
    })
      .compileComponents();

    router = TestBed.inject(Router);
    authService = TestBed.inject(AuthService);

    fixture = TestBed.createComponent(RegisterForm);
    component = fixture.componentInstance;

    submitButton = fixture.nativeElement.querySelector('[type="submit"]');

    fixture.detectChanges();
  });

  test('should submit form after button click', () => {
    jest.spyOn(component, 'onSubmit');
    submitButton.click();

    expect(component.onSubmit).toHaveBeenCalled();
  });

  test('should set error "required" on each field', async () => {
    const expectedError = { required: true };
    jest.spyOn(authService, 'register');
    jest.spyOn(component, 'onSubmit');
    jest.spyOn(component, 'parseErrors');

    submitButton.click();
    fixture.detectChanges();

    for (let controlsKey in component.form.controls) {
      expect(component.form.controls[controlsKey].errors).toEqual(expectedError);
    }

    expect(component.onSubmit).toHaveBeenCalled();
    expect(component.form.invalid).toBe(true);

    expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    expect(authService.register).not.toHaveBeenCalled();
  });

  test('should set error "comparePassword" on confirmPassword field', () => {
    const mockPassword = 'password';
    const expectedError = { comparePassword: true };
    jest.spyOn(authService, 'register');
    jest.spyOn(component, 'onSubmit');
    jest.spyOn(component, 'parseErrors');

    component.form.controls['password'].setValue(mockPassword);
    component.form.controls['confirmPassword'].setValue(mockPassword + '123');

    submitButton.click();
    fixture.detectChanges();

    expect(component.onSubmit).toHaveBeenCalled();
    expect(component.form.controls['confirmPassword'].errors).toEqual(expectedError);

    expect(component.form.invalid).toBe(true);
    expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    expect(authService.register).not.toHaveBeenCalled();
  });

  test('should set error "email" on email field', () => {
    const expectedError = { email: true };
    const wrongEmails = ['test.com', 'test@.com', 'test', '@test.com'];
    jest.spyOn(authService, 'register');
    jest.spyOn(component, 'onSubmit');
    jest.spyOn(component, 'parseErrors');

    wrongEmails.forEach((email) => {
      component.form.controls['email'].setValue(email);
      submitButton.click();
      fixture.detectChanges();

      expect(component.onSubmit).toHaveBeenCalled();
      expect(component.form.controls['email'].errors).toEqual(expectedError);

      expect(component.form.invalid).toBe(true);
      expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
      expect(authService.register).not.toHaveBeenCalled();
    });
  });

  test('should set error "emailExist" on email field', async () => {
    const expectedError = { emailExists: true };
    const mockFormData: UserRegisterData = {
      fullName: 'Mock name',
      email: 'test@test.com',
      password: 'MockPassword',
    };

    const axiosError = new AxiosError('Request failed');
    ( axiosError as any ).response = { data: { detail: ErrorMessage.EmailRegistered } };

    jest.spyOn(authService, 'register').mockRejectedValue(axiosError);
    jest.spyOn(component, 'onSubmit');
    jest.spyOn(component, 'parseErrors');

    component.form.setValue({
      fullName: mockFormData.fullName,
      email: mockFormData.email,
      password: mockFormData.password,
      confirmPassword: mockFormData.password
    });

    fixture.detectChanges();

    submitButton.click();

    expect(component.onSubmit).toHaveBeenCalled();

    expect(authService.register).toHaveBeenCalledWith(mockFormData);
    await expect(authService.register).rejects.toThrowError();

    fixture.detectChanges();

    expect(component.form.controls['email'].errors).toEqual(expectedError);
    expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    expect(component.form.invalid).toBe(true);
  });

  test('should save token in local storage and redirect to chat view', async () => {
    const mockFormData: UserRegisterData = {
      fullName: 'Mock name',
      email: 'test@test.com',
      password: 'MockPassword',
    };
    const mockResponse: Token = { accessToken: 'mockToken', tokenType: 'bearer' };

    component.form.setValue({
      fullName: mockFormData.fullName,
      email: mockFormData.email,
      password: mockFormData.password,
      confirmPassword: mockFormData.password
    });

    jest.spyOn(authService, 'register').mockResolvedValue(mockResponse);
    jest.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    });

    await component.onSubmit();

    expect(authService.register).toHaveBeenCalledWith(mockFormData);
    expect(localStorage.setItem).toHaveBeenCalledWith('token', mockResponse.accessToken);
    expect(router.navigate).toHaveBeenCalledWith(['/chat']);
  });
});
