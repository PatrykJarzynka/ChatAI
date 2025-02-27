import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginForm } from './login-form.component';
import { expect, jest, test, describe, beforeEach } from '@jest/globals';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ErrorMessage } from '@enums/ErrorMessage';
import { UserLoginData } from 'appTypes/UserLoginData';


describe('LoginForm', () => {
  let component: LoginForm;
  let fixture: ComponentFixture<LoginForm>;
  let submitButton: HTMLButtonElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginForm, BrowserAnimationsModule, NoopAnimationsModule],
    })
      .compileComponents();

    fixture = TestBed.createComponent(LoginForm);
    component = fixture.componentInstance;

    submitButton = fixture.nativeElement.querySelector('[type="submit"]');

    fixture.detectChanges();
  });

  test('should call onSubmit function after button click', () => {
    jest.spyOn(component, 'onSubmit');
    submitButton.click();

    expect(component.onSubmit).toHaveBeenCalled();
  });

  test('\'should emit loginSubmit event with user\'s provided data\'', () => {
    const mockData: UserLoginData = {
      email: 'test@test.pl',
      password: 'TestPassword123.'
    };

    jest.spyOn(component.loginSubmit, 'emit');

    component.form.controls['email'].setValue(mockData.email);
    component.form.controls['password'].setValue(mockData.password);

    fixture.detectChanges();

    component.onSubmit();

    expect(component.loginSubmit.emit).toHaveBeenCalledWith(mockData);
  });

  test('should not emit loginSubmit when form is invalid', () => {
    const invalidMockData: UserLoginData = {
      email: 'test@test',
      password: ''
    };

    jest.spyOn(component.loginSubmit, 'emit');

    component.form.controls['email'].setValue(invalidMockData.email);
    component.form.controls['password'].setValue(invalidMockData.password);

    fixture.detectChanges();

    component.onSubmit();

    expect(component.loginSubmit.emit).not.toHaveBeenCalled();
  });

  test('should set error "required" on each field', () => {
    const expectedError = { required: true };
    jest.spyOn(component.loginSubmit, 'emit');
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


    expect(component.loginSubmit.emit).not.toHaveBeenCalled();
  });

  test('should set error "credentials" on each field', async () => {
    const expectedError = { credentials: true };
    jest.spyOn(component, 'setErrors');
    jest.spyOn(component, 'parseErrors');

    component.setErrors(ErrorMessage.WrongCredentials);

    fixture.detectChanges();

    for (let controlsKey in component.form.controls) {
      expect(component.form.controls[controlsKey].errors).toEqual(expectedError);
      expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    }

    expect(component.form.invalid).toBe(true);
  });

  test('should set errors based on authErrors input', () => {
    fixture.componentRef.setInput('authErrors', ErrorMessage.WrongCredentials);
    jest.spyOn(component, 'setErrors');

    fixture.detectChanges();

    expect(component.setErrors).toHaveBeenCalledWith(ErrorMessage.WrongCredentials);
  });

  test('should clear all errors', () => {
    fixture.componentRef.setInput('authErrors', ErrorMessage.WrongCredentials);
    const expectedError = null;
    jest.spyOn(component, 'setErrors');

    fixture.detectChanges();

    component.setErrors(null);

    for (let controlsKey in component.form.controls) {
      expect(component.form.controls[controlsKey].errors).toEqual(expectedError);
    }

    expect(component.form.invalid).toBe(false);
  });

  test('should emit newAccountClick event', () => {
    const newAccountButton = fixture.nativeElement.querySelector('[type="button"]');
    jest.spyOn(component, 'onNewAccountClick');
    jest.spyOn(component.newAccountClick, 'emit');

    newAccountButton.click();

    expect(component.onNewAccountClick).toHaveBeenCalled();
    expect(component.newAccountClick.emit).toHaveBeenCalled();
  });
});
