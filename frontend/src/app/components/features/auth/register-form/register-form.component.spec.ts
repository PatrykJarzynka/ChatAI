import { ComponentFixture, TestBed } from '@angular/core/testing';
import { describe, test, beforeEach, expect, jest } from '@jest/globals';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { RegisterForm } from './register-form.component';
import { ErrorMessage } from '@enums/ErrorMessage';
import { UserRegisterData } from 'appTypes/UserRegisterData';
import { AuthProvider } from '@appTypes/AuthProvider';


describe('RegisterForm', () => {
  let component: RegisterForm;
  let fixture: ComponentFixture<RegisterForm>;
  let submitButton: HTMLButtonElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegisterForm, BrowserAnimationsModule, NoopAnimationsModule],
    })
      .compileComponents();

    fixture = TestBed.createComponent(RegisterForm);
    component = fixture.componentInstance;

    submitButton = fixture.nativeElement.querySelector('[type="submit"]');

    fixture.detectChanges();
  });

  test('should call onSubmit function after button click', () => {
    jest.spyOn(component, 'onSubmit');
    submitButton.click();

    expect(component.onSubmit).toHaveBeenCalled();
  });

  test('should emit registerSubmit event with user\'s provided data', () => {
    const mockData: UserRegisterData = {
      email: 'test@test.pl',
      password: 'TestPassword123.',
      fullName: 'Harry Angel',
      provider: AuthProvider.LOCAL,
    };

    jest.spyOn(component.registerSubmit, 'emit');

    component.form.controls['email'].setValue(mockData.email);
    component.form.controls['password'].setValue(mockData.password);
    component.form.controls['confirmPassword'].setValue(mockData.password);
    component.form.controls['fullName'].setValue(mockData.fullName);

    fixture.detectChanges();

    component.onSubmit();

    expect(component.registerSubmit.emit).toHaveBeenCalledWith(mockData);
  });

  test('should not emit registerSubmit when form is invalid', () => {
    const invalidMockData: UserRegisterData = {
      email: 'test@test',
      password: '',
      fullName: 'Harry Angel.',
      provider: AuthProvider.LOCAL,
    };

    jest.spyOn(component.registerSubmit, 'emit');

    component.form.controls['email'].setValue(invalidMockData.email);
    component.form.controls['password'].setValue(invalidMockData.password);
    component.form.controls['fullName'].setValue(invalidMockData.fullName);

    fixture.detectChanges();

    component.onSubmit();

    expect(component.registerSubmit.emit).not.toHaveBeenCalled();
  });

  test('should set error "required" on each field', async () => {
    const expectedError = { required: true };
    jest.spyOn(component.registerSubmit, 'emit');
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
  });

  test('should set error "comparePassword" on confirmPassword field', () => {
    const mockPassword = 'password';
    const expectedError = { comparePassword: true };
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
  });

  test('should set error "email" on email field', () => {
    const expectedError = { email: true };
    const wrongEmails = ['test.com', 'test@.com', 'test', '@test.com'];
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
    });
  });

  test('should set error "emailExist" on email field', async () => {
    const expectedError = { emailExists: true };
    // const mockFormData: UserRegisterData = {
    //   fullName: 'Mock name',
    //   email: 'test@test.com',
    //   password: 'MockPassword',
    // };
    jest.spyOn(component, 'setErrors');
    jest.spyOn(component, 'parseErrors');

    component.setErrors(ErrorMessage.EmailRegistered);

    fixture.detectChanges();

    expect(component.form.controls['email'].errors).toEqual(expectedError);
    expect(component.parseErrors).toHaveBeenCalledWith(expectedError);
    expect(component.form.invalid).toBe(true);
  });

  test('should set errors based on authErrors input', () => {
    fixture.componentRef.setInput('authErrors', ErrorMessage.EmailRegistered);
    jest.spyOn(component, 'setErrors');

    fixture.detectChanges();

    expect(component.setErrors).toHaveBeenCalledWith(ErrorMessage.EmailRegistered);
  });

  test('should clear email errors', () => {
    fixture.componentRef.setInput('authErrors', ErrorMessage.EmailRegistered);
    const expectedError = null;
    jest.spyOn(component, 'setErrors');

    fixture.detectChanges();

    component.setErrors(null);

    expect(component.form.controls['email'].errors).toEqual(expectedError);
  });
});
